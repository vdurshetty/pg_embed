import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


# 1. Load pretrained ResNet50 and remove the classification head
class ResNet50Embedder(nn.Module):
    def __init__(self):
        super().__init__()
        base = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.feature_extractor = nn.Sequential(*list(base.children())[:-1])  # remove FC layer

    def forward(self, x):
        x = self.feature_extractor(x)
        return x.view(x.size(0), -1)  # flatten to (batch, 2048)

embedder = ResNet50Embedder()
embedder.eval()

# 2. Image preprocessing pipeline
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 3. Function to generate embedding
def get_embedding(image_path: str):
    img = Image.open(image_path).convert("RGB")
    x = preprocess(img).unsqueeze(0)  # add batch dimension

    with torch.no_grad():
        vec = embedder(x)

    return vec.squeeze().numpy()  # shape: (2048,)


# Example usage
image_path = "/Users/venu/venus/ai_samples/pg_embed/uploads/images/Sridevi_dl.jpeg"
print("starting")
embedding = get_embedding(image_path)
print("Embedding shape:", embedding.shape)
print(embedding[:10])
