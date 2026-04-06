import torch
import torchvision.transforms as transforms
from PIL import Image
import os
from pg_vector_util import pg_create_table_index, pg_insert


# Image Table
image_table = """CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    embedding VECTOR(512)  -- size depends on model
    );"""

image_index = """
    CREATE INDEX IF NOT EXISTS images_embed_idx
    ON images
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);"""

# Load pretrained model (ResNet)
model = torch.hub.load('pytorch/vision', 'resnet18', pretrained=True)
model.eval()

# Remove final classification layer → get embeddings
model = torch.nn.Sequential(*list(model.children())[:-1])

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


def get_image_embedding(image_path):
    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        embedding = model(img)

    return embedding.flatten().numpy().tolist()


# Create image table if not exists
pg_create_table_index(image_table)
# create index if not exists
pg_create_table_index(image_index)

# insert sql statement
insert_sql = "INSERT INTO images (file_name, embedding) VALUES (%s, %s)"


def pg_store_image(image_path):
    if not os.path.exists(image_path):
        print("Image file not exists")
        return "Image file not exists"
    # Generate embedding
    embedding = get_image_embedding(image_path)
    print("embedding is :", embedding)




