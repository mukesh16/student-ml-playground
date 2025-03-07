from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import shutil
import os
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Database Configuration
DB_URL = "postgresql://demo:password@localhost/tabtognn"
engine = create_engine(DB_URL)

# Initialize FastAPI
app = FastAPI()

# File Upload Directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Insert file metadata into PostgreSQL
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO file_uploads (filename) VALUES (:filename)"), {"filename": file.filename})
        conn.commit()

    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.get("/files/")
def list_files():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM file_uploads")).fetchall()
    
    files = [{"id": row[0], "filename": row[1], "upload_time": row[2]} for row in result]
    return {"files": files}

@app.get("/preview/")
def preview_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    df = pd.read_csv(file_path)
    return JSONResponse(content=df.head().to_dict(orient="records"))

@app.post("/train/")
def train_model(filename: str, target_column: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    df = pd.read_csv(file_path)
    
    if target_column not in df.columns:
        raise HTTPException(status_code=400, detail="Target column not found")
    
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    model_path = os.path.join(UPLOAD_DIR, "trained_model.pkl")
    joblib.dump(model, model_path)

    return {"message": "Model trained successfully", "accuracy": accuracy, "model_path": model_path}
