from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, UnidentifiedImageError

from .logic import identify_waste

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Trash Sorter AI")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
MAX_UPLOAD_BYTES = 8 * 1024 * 1024
ALLOWED_FORMATS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/sort", response_class=HTMLResponse)
async def sort_trash(request: Request, file: UploadFile = File(...)):
    contents = await file.read(MAX_UPLOAD_BYTES + 1)
    await file.close()
    if not contents:
        raise HTTPException(status_code=400, detail="Choose an image first.")
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 8 MB or smaller.")

    try:
        from io import BytesIO
        with Image.open(BytesIO(contents)) as image:
            image.verify()
            image_format = image.format
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Upload a valid JPG, PNG, or WEBP image.")

    if image_format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, and WEBP images are supported.")

    filename = f"{uuid4().hex}{ALLOWED_FORMATS[image_format]}"
    file_path = STATIC_DIR / filename
    file_path.write_bytes(contents)
    result = identify_waste(str(file_path))
    return templates.TemplateResponse("index.html", {
        "request": request, "result": result, "image": filename
    })
