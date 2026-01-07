from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import shutil

app = FastAPI()


def get_storage():
    total, used, free = shutil.disk_usage("/")
    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    percent = (used / total) * 100

    return round(used_gb, 1), round(total_gb, 1), round(percent)


@app.get("/", response_class=HTMLResponse)
def home():
    used, total, percent = get_storage()

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Storage Status</title>

    <!-- Tailwind CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">

    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#6366f1'
                    }}
                }}
            }}
        }}
    </script>
</head>

<body class="bg-white min-h-screen flex items-center justify-center">

    <div class="mt-4 bg-[#101622] text-white p-5 rounded-xl relative overflow-hidden group w-80 shadow-xl">
        
        <div class="absolute right-0 top-0 opacity-10 -mr-4 -mt-4 transform rotate-12
                    group-hover:scale-110 transition-transform duration-500">
            <span class="material-symbols-outlined text-[120px]">
                cloud_queue
            </span>
        </div>

        <h3 class="font-bold text-lg relative z-10">Storage Status</h3>
        <p class="text-gray-400 text-sm mb-4 relative z-10">
            Media Library Usage
        </p>

        <div class="w-full bg-gray-700 rounded-full h-2 mb-2 relative z-10">
            <div class="bg-primary h-2 rounded-full transition-all duration-700"
                 style="width: {percent}%">
            </div>
        </div>

        <div class="flex justify-between text-xs text-gray-400 relative z-10">
            <span>{used} GB used</span>
            <span>{total} GB total</span>
        </div>

    </div>

</body>
</html>
"""
