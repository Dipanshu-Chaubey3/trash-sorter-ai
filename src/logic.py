import torch
import torchvision.models as models
from PIL import Image

# 1. Load ResNet (The "Residual Network" is great for material texture)
weights = models.ResNet18_Weights.DEFAULT
model = models.resnet18(weights=weights)
model.eval()

# 2. Define the Sorting Rules
# This maps what the AI sees to the correct recycling bin
BIN_RULES = {
    "bottle": "Blue Bin (Plastic/Glass)",
    "can": "Red Bin (Metal)",
    "paper": "Green Bin (Paper)",
    "envelope": "Green Bin (Paper)",
    "banana": "Brown Bin (Organic)",
    "apple": "Brown Bin (Organic)",
    "cup": "Yellow Bin (Mixed Recyclables)"
}

def identify_waste(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        # Use the specific transforms required by ResNet18
        transform = weights.transforms()
        batch = transform(img).unsqueeze(0)

        with torch.no_grad():
            output = model(batch)
            prob = torch.nn.functional.softmax(output[0], dim=0)
            
        conf, index = torch.max(prob, 0)
        object_name = weights.meta["categories"][index.item()]
        
        # Determine the bin
        assigned_bin = "Black Bin (General Waste)" # Default
        for key in BIN_RULES:
            if key in object_name.lower():
                assigned_bin = BIN_RULES[key]
                break
                
        return {
            "item": object_name.replace("_", " ").title(),
            "bin": assigned_bin,
            "confidence": f"{conf.item():.2%}"
        }
    except Exception as e:
        return {"error": str(e)}