from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)):
    code = await file.read()
    filename = file.filename

    print(f"Received file: {filename}")

    if filename.endswith((".js", ".jsx")):
        print("Analyzing JavaScript file...")
        result = analysis.analyze_js(code)  # Now uses ESLint dynamically
    elif filename.endswith(".py"):
        print("Analyzing Python file...")
        result = analysis.analyze_python(code)  # Now calculates real score
    else:
        return {"error": "Unsupported file type"}

    return result
