from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
import os
import shutil

app = FastAPI()

BASE_DIR = "storage"
os.makedirs(BASE_DIR, exist_ok=True)


def list_items():
    items = []
    for name in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, name)
        items.append({
            "name": name,
            "is_dir": os.path.isdir(path)
        })
    return items


@app.get("/", response_class=HTMLResponse)
def home():
    items = list_items()

    items_html = ""
    for item in items:
        if item["is_dir"]:
            items_html += f"""
            <div class="flex items-center gap-2 text-gray-700">
                📁 <span>{item['name']}</span>
            </div>
            """
        else:
            items_html += f"""
            <a href="/download/{item['name']}"
               class="flex items-center gap-2 text-blue-600 hover:underline">
                📄 {item['name']}
            </a>
            """

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Storage Manager</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-100 min-h-screen flex items-center justify-center">

<div class="bg-white p-6 rounded-xl shadow-lg w-[420px] space-y-4">

    <h2 class="text-xl font-bold text-center">📦 Storage Manager</h2>

    <!-- Upload -->
    <form action="/upload" method="post" enctype="multipart/form-data"
          class="flex gap-2">
        <input type="file" name="file" required
               class="border rounded w-full px-2 py-1">
        <button class="bg-blue-600 text-white px-3 rounded">
            Upload
        </button>
    </form>

    <!-- Create Folder -->
    <form action="/mkdir" method="post" class="flex gap-2">
        <input type="text" name="folder" placeholder="New folder name" required
               class="border rounded w-full px-2 py-1">
        <button class="bg-green-600 text-white px-3 rounded">
            Create
        </button>
    </form>

    <hr>

    <!-- File List -->
    <div class="space-y-2 max-h-48 overflow-y-auto">
        {items_html if items_html else "<p class='text-gray-400'>No files yet</p>"}
    </div>

</div>

</body>
</html>
"""


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join(BASE_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse("/", status_code=303)


@app.post("/mkdir")
def make_dir(folder: str = Form(...)):
    safe_name = folder.replace("/", "").replace("..", "")
    os.makedirs(os.path.join(BASE_DIR, safe_name), exist_ok=True)
    return RedirectResponse("/", status_code=303)


@app.get("/download/{filename}")
def download(filename: str):
    path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(path):
        return FileResponse(path, filename=filename)
    return RedirectResponse("/")
