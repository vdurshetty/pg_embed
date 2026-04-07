# This sample is to insert the image clip in pinecone database and also query based on the matching image clip

import io
from sentence_transformers import SentenceTransformer
from PIL import Image
# from transformers import AutoTokenizer


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


# Example usage
# image_path = "/Users/venu/venus/ai_samples/pg_embed/uploads/images/Sridevi_dl.jpeg"
# print("starting")
# embedding = get_image_embedding(image_path)
# print("Embedding shape:", len(embedding))