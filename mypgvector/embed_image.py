from PIL import Image
from pathlib import Path
from sentence_transformers import SentenceTransformer
import os
import io
from . import pg_vector_util


# import ssl
# Disable SSL certifcate verification
# ssl._create_default_https_context = ssl._create_unverified_context

#
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


def get_image_embedding(image_path_or_bytes):
    # tokenizer = AutoTokenizer.from_pretrained("clip-ViT-B-32", use_fast=False)
    model = SentenceTransformer("clip-ViT-B-32")
    # model = SentenceTransformer(tokenizer)
    if isinstance(image_path_or_bytes, str):
        img = Image.open(image_path_or_bytes)
    else:
        img = Image.open(io.BytesIO(image_path_or_bytes))
    img_embed = model.encode(img)
    return img_embed.tolist()


# ── DB Setup ─────────────────────────────────────────────────────
def setup_db():
    # Create image table if not exists
    pg_vector_util.pg_create_table_index(image_table)
    # create index if not exists
    pg_vector_util.pg_create_table_index(image_index)
    print("✅ DB ready")


# ── Store Embedding ───────────────────────────────────────────────
def store_embedding(filename: str, filepath: str, embedding: list[float]):
    print("In Store Embedding method....")
    setup_db()
    print("DB Setup done!!!")
    cursor = pg_vector_util.pg_get_cursor()
    cursor.execute("""
        INSERT INTO image_embeddings (filename, filepath, embedding)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (filename, filepath, embedding))
    pg_vector_util.pg_get_connection().commit()
    row_id = cursor.fetchone()[0]
    print(f"✅ Stored: {filename} → id={row_id}")
    return row_id


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
    # Generate embedding
    #model = load_model()
    #embedding = image_to_embedding(image_path, model)

    embeddings = get_image_embedding(image_path)
    print("embedding is :", embeddings)

    row_id = store_embedding(Path(image_path).name, image_path, embeddings)
    print(f"✅ {Path(image_path).name}: 512-dim → id={row_id}")
    print("Image stored to PG Vector database")


def query_image():
    # --- Search similar to query image ---
    query_path = "images/cat2.jpg"
    model = load_model()
    cursor = pg_vector_util.pg_get_cursor()
    if Path(query_path).exists():
        query_embedding = image_to_embedding(query_path, model)
        results = find_similar(cursor, query_embedding, top_k=3)

        print("\n🔍 Similar images:")
        for row in results:
            print(f"  id={row[0]} | {row[1]} | similarity={row[3]:.4f}")



