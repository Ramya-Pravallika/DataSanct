from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import shutil
import pandas as pd
import uuid
from typing import List
import logging
import zipfile
from agent import agent
from cleaning_ops import CleaningOps

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Intelligent Data Cleaning Agent")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
CLEANED_DIR = "cleaned"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)

# Mount uploads for serving images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/cleaned", StaticFiles(directory=CLEANED_DIR), name="cleaned")

@app.get("/")
def read_root():
    return {"message": "Agentic Data Cleaner API is running"}

@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    """
    1. Save file
    2. Analyze (Tabular/Image)
    3. Generate Cleaning Plan
    """
    file_id = str(uuid.uuid4())
    ext = file.filename.split('.')[-1].lower()
    file_path = f"{UPLOAD_DIR}/{file_id}.{ext}"
    
    logger.info(f"Received file upload: {file.filename} (ID: {file_id})")

    with open(file_path, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    response = {
        "file_id": file_id,
        "original_filename": file.filename,
        "type": "unknown",
        "analysis": {},
        "plan": {}
    }
    
    try:
        if ext in ['csv', 'xlsx', 'xls']:
            response["type"] = "tabular"
            logger.info(f"Analyzing tabular data: {file_id}")
            df = pd.read_csv(file_path) if ext == 'csv' else pd.read_excel(file_path)
            analysis = agent.analyze_tabular(df)
            plan = agent.generate_cleaning_plan(analysis, "tabular")
            response["analysis"] = analysis
            response["plan"] = plan
            
        elif ext == 'zip':
            # Extract and process first CSV/Excel file found
            response["type"] = "tabular"
            logger.info(f"Processing ZIP file: {file_id}")
            
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Find first CSV or Excel file
                    tabular_file = None
                    for filename in zip_ref.namelist():
                        # Skip directories and hidden files
                        if filename.endswith('/') or filename.startswith('__MACOSX'):
                            continue
                        file_ext = filename.split('.')[-1].lower()
                        if file_ext in ['csv', 'xlsx', 'xls']:
                            tabular_file = filename
                            break
                    
                    if not tabular_file:
                        raise HTTPException(status_code=400, detail="No CSV or Excel file found in ZIP archive")
                    
                    # Extract to temp location
                    extracted_ext = tabular_file.split('.')[-1].lower()
                    extracted_path = f"{UPLOAD_DIR}/{file_id}_extracted.{extracted_ext}"
                    with zip_ref.open(tabular_file) as source, open(extracted_path, 'wb') as target:
                        target.write(source.read())
                    
                    # Read and analyze
                    df = pd.read_csv(extracted_path) if extracted_ext == 'csv' else pd.read_excel(extracted_path)
                    analysis = agent.analyze_tabular(df)
                    plan = agent.generate_cleaning_plan(analysis, "tabular")
                    response["analysis"] = analysis
                    response["plan"] = plan
                    response["extracted_file"] = tabular_file
                    logger.info(f"Extracted and analyzed: {tabular_file}")
            except zipfile.BadZipFile:
                logger.error(f"Invalid ZIP file: {file_id}")
                raise HTTPException(status_code=400, detail="Invalid ZIP file")
            
        elif ext in ['jpg', 'jpeg', 'png']:
            response["type"] = "image"
            logger.info(f"Analyzing image data: {file_id}")
            analysis = agent.analyze_image(file_path)
            plan = agent.generate_cleaning_plan(analysis, "image")
            response["analysis"] = analysis
            response["plan"] = plan
            
    except Exception as e:
        logger.error(f"Error analyzing file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return response

@app.post("/clean/{file_id}")
async def clean_data(file_id: str, plan_override: dict = None):
    """
    Executes the cleaning plan.
    """
    # Find file
    files = os.listdir(UPLOAD_DIR)
    target_file = next((f for f in files if f.startswith(file_id)), None)
    if not target_file:
        logger.warning(f"File not found for cleaning: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
        
    input_path = f"{UPLOAD_DIR}/{target_file}"
    ext = target_file.split('.')[-1].lower()
    output_filename = f"cleaned_{target_file}"
    output_path = f"{CLEANED_DIR}/{output_filename}"
    
    logger.info(f"Starting cleaning process for: {target_file}")
    result = {"status": "success", "download_url": f"/download/{output_filename}"}
    
    try:
        # Handle different file types
        if ext == 'zip':
            # Find the extracted file
            extracted_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(f"{file_id}_extracted")]
            if extracted_files:
                extracted_path = f"{UPLOAD_DIR}/{extracted_files[0]}"
                extracted_ext = extracted_files[0].split('.')[-1].lower()
                df = pd.read_csv(extracted_path) if extracted_ext == 'csv' else pd.read_excel(extracted_path)
                logger.info(f"Processing extracted file from ZIP: {extracted_files[0]}")
            else:
                raise HTTPException(status_code=404, detail="Extracted file not found. Please re-upload the ZIP file.")
        elif ext in ['csv', 'xlsx', 'xls']:
            df = pd.read_csv(input_path) if ext == 'csv' else pd.read_excel(input_path)
            logger.info(f"Processing {ext.upper()} file")
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
        
        
        if ext in ['csv', 'xlsx', 'xls', 'zip']:
            # Re-generate plan if not provided (or retrieve from state - simplifying here)
            # ideally we pass the plan from frontend, but for now re-gen or use default
            analysis = agent.analyze_tabular(df)
            plan = plan_override if plan_override else agent.generate_cleaning_plan(analysis, "tabular")
            
            # Clean with detailed feedback
            cleaned_df, report = CleaningOps.clean_tabular(df, plan['plan'])
            
            # Save in appropriate format based on input type
            if ext == 'zip':
                # For ZIP files, save as CSV (simplest for download)
                cleaned_df.to_csv(output_path, index=False)
            elif ext in ['xlsx', 'xls']:
                # Save Excel files as Excel
                cleaned_df.to_excel(output_path, index=False)
            else:
                # Save CSV files as CSV
                cleaned_df.to_csv(output_path, index=False)
            
            result["stats"] = {
                "original_rows": len(df),
                "original_columns": len(df.columns),
                "cleaned_rows": len(cleaned_df),
                "cleaned_columns": len(cleaned_df.columns),
                "removed_rows": len(df) - len(cleaned_df),
                "removed_columns": len(df.columns) - len(cleaned_df.columns)
            }
            result["report"] = report
            result["plan"] = plan  # Include plan for frontend reasoning display
            logger.info(f"Tabular cleaning complete. Removed {result['stats']['removed_rows']} rows.")
            
        elif ext in ['jpg', 'jpeg', 'png']:
            # Re-gen plan logic same as above
            analysis = agent.analyze_image(input_path)
            plan = plan_override if plan_override else agent.generate_cleaning_plan(analysis, "image")
            
            CleaningOps.clean_image(input_path, output_path, plan['plan'])
            logger.info(f"Image cleaning complete.")
            
    except Exception as e:
        logger.error(f"Error cleaning file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return result

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"{CLEANED_DIR}/{filename}"
    if os.path.exists(file_path):
        logger.info(f"Downloading file: {filename}")
        return FileResponse(file_path)
    logger.warning(f"Download failed - file not found: {filename}")
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
