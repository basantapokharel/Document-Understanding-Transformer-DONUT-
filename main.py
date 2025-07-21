# from fastapi import FastAPI, File, UploadFile, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from PIL import Image
# import io
# from inference import process_document

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def upload_form(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/upload/")
# async def upload_image(request: Request, file: UploadFile = File(...)):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents)).convert("RGB")
#     result = process_document(image)
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "result": result
#     })


from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
from inference import process_document

app = FastAPI(title="Invoice to JSON Converter", version="1.0.0")

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    """Render the main upload form page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    """Process uploaded invoice and return results"""
    try:
        # Read the uploaded file
        contents = await file.read()
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Process the document using your inference function
        result = process_document(image)
        
        # Return the template with results
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result,
            "filename": file.filename
        })
        
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Error processing file: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": error_message
        })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Invoice to JSON Converter"}

