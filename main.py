from fastapi import FastAPI, File, Form, UploadFile
import json
import os
import zipfile
import pandas as pd

app = FastAPI()

def load_answers():
    if os.path.exists("answers.json"):
        with open("answers.json", "r") as f:
            return json.load(f)
    return {}

answers_db = load_answers()

@app.post("/api/")
async def get_answer(question: str = Form(...), file: UploadFile = File(None)):
    if file:
        filepath = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(file.file.read())
        
        if file.filename.endswith(".zip"):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall("temp")
                extracted_files = zip_ref.namelist()
                for extracted_file in extracted_files:
                    if extracted_file.endswith(".csv"):
                        df = pd.read_csv(f"temp/{extracted_file}")
                        if "answer" in df.columns:
                            return {"answer": str(df["answer"].iloc[0])}
    
    answer = answers_db.get(question, "Answer not found. Please update database.")
    return {"answer": answer}