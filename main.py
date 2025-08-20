from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import subprocess
import tempfile

app = FastAPI()

# Mount static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(
    request: Request,
    file: UploadFile = File(...),
    tool: str = Form(...)
):
    # Save file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Run oletools based on selection
    cmd = []
    if tool == "oleid":
        cmd = ["oleid", tmp_path]
    elif tool == "olevba":
        cmd = ["olevba", tmp_path]
    elif tool == "mraptor":
        cmd = ["mraptor", tmp_path]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "output": result.stdout,
        "error": result.stderr,
        "tool": tool
    })
