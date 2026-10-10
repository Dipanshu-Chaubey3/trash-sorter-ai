# Trash Sorter AI

A FastAPI demo that uses an ImageNet-pretrained ResNet-18 model to classify an uploaded image and show a cautious disposal suggestion.

## Important limitation
This is a learning prototype, **not a waste-specific trained model**. ImageNet labels do not reliably identify every waste material, and recycling rules vary by location. Always verify the item and local guidance before disposal. The confidence score is model confidence, not guaranteed real-world accuracy.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn src.app:app --reload
``
Open http://127.0.0.1:8000.

Supported uploads: JPG, PNG, WEBP up to 8 MB. Model weights may download on first run.
