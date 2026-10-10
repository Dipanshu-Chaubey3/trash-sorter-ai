import torch
import torchvision.models as models
from PIL import Image, UnidentifiedImageError

# This is an ImageNet-pretrained general-purpose model, not a model trained
# specifically on household waste. Treat the result as a suggestion only.
weights = models.ResNet18_Weights.DEFAULT
model = models.resnet18(weights=weights)
model.eval()
transform = weights.transforms()

BIN_RULES = {
    "bottle": "Check local rules: plastic/glass collection",
    "can": "Check local rules: metal recycling",
    "paper": "Paper recycling, if clean and accepted locally",
    "envelope": "Paper recycling, if accepted locally",
    "banana": "Organic/compost collection, where available",
    "apple": "Organic/compost collection, where available",
    "carton": "Check local rules for cartons",
    "tin": "Check local rules: metal recycling",
}

def identify_waste(image_path):
    try:
        with Image.open(image_path) as source:
            image = source.convert("RGB")
        batch = transform(image).unsqueeze(0)
        with torch.inference_mode():
            probabilities = torch.nn.functional.softmax(model(batch)[0], dim=0)
        confidence, index = torch.max(probabilities, dim=0)
        object_name = weights.meta["categories"][index.item()]
        lower_name = object_name.lower()
        assigned_bin = "General waste or verify manually"
        for key, bin_name in BIN_RULES.items():
            if key in lower_name:
                assigned_bin = bin_name
                break
        return {
            "item": object_name.replace("_", " ").title(),
            "bin": assigned_bin,
            "confidence": f"{confidence.item():.2%}",
            "note": "General ImageNet prediction; verify the item and your local recycling rules."
        }
    except (OSError, UnidentifiedImageError) as exc:
        return {"error": "Could not read that image. Upload a valid image file."}
    except Exception:
        return {"error": "Image classification failed. Check dependencies and model download, then try again."}
