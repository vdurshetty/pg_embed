import os
from pathlib import Path
from . import pg_vector_util
from . import image_embed_1

# Enable vector in postgres
enable_vector = "CREATE EXTENSION IF NOT EXISTS vector"

# Image Table
image_table = """
        CREATE TABLE IF NOT EXISTS image_embeddings (
            id          SERIAL PRIMARY KEY,
            filename    TEXT NOT NULL,
            filepath    TEXT NOT NULL,
            embedding   vector(512),
            created_at  TIMESTAMPTZ DEFAULT NOW()
        )
    """

image_index = """
        CREATE INDEX IF NOT EXISTS idx_image_embedding
        ON image_embeddings
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """


# ── DB Setup ─────────────────────────────────────────────────────
def setup_db():
    # Create image table if not exists
    pg_vector_util.pg_create_table_index(image_table)
    # create index if not exists
    pg_vector_util.pg_create_table_index(image_index)
    print("✅ DB ready")


# ── Store Embedding ───────────────────────────────────────────────
def store_embedding(filename: str, filepath: str, embedding: list[float]):
    setup_db()
    insert_sql = """
        INSERT INTO image_embeddings (filename, filepath, embedding)
        VALUES (%s, %s, %s)
        RETURNING id
    """
    pg_vector_util.pg_insert_image(insert_sql, filename, filepath, embedding)
    print(" insert committed...")
    # row_id = cursor.fetchone()[0]
    # print(f"✅ Stored: {filename} → id={row_id}")
    return "inserted"


# ── Search Similar Images ─────────────────────────────────────────
def find_similar(cursor, embedding: list[float], top_k: int = 5):
    cursor.execute("""
        SELECT id, filename, filepath,
               1 - (embedding <=> %s::vector) AS similarity
        FROM image_embeddings
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (embedding, embedding, top_k))
    return cursor.fetchall()


def pg_store_image(image_path):
    print(" in pg_store image method...")
    if not os.path.exists(image_path):
        print("Image file not exists")
        return "Image file not exists"
    embeddings = image_embed_1.get_image_embedding(image_path)
    print("embedding is :", embeddings)

    row_id = store_embedding(Path(image_path).name, image_path, embeddings)
    print(f"✅ {Path(image_path).name}: 512-dim → id={row_id}")
    print("Image stored to PG Vector database")


#def query_image():
    # --- Search similar to query image ---
    # query_path = "images/cat2.jpg"
    # model = load_model()
    # cursor = pg_vector_util.pg_get_cursor()
    # if Path(query_path).exists():
    #     query_embedding = image_embed_1.get_image_embedding(query_path, model)
    #     results = find_similar(cursor, query_embedding, top_k=3)
    #
    #     print("\n🔍 Similar images:")
    #     for row in results:
    #         print(f"  id={row[0]} | {row[1]} | similarity={row[3]:.4f}")


# image_path = "/Users/venu/venus/ai_samples/pg_embed/uploads/images/Sridevi_dl.jpeg"
# print("starting")
# pg_store_image(image_path)
