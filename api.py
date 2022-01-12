from typing import List
import uvicorn as uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from ai_nlp import Models, SummaryModel
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

model_name = config['SummaryModel']['ModelType']
model_params = config['SummaryModelParams'] if 'SummaryModelParams' in config else {}  # no params to the model


def get_summary_model(model_type, **kwargs):
    # function that returns the AI Model used for summarization.
    try:
        return SummaryModel(model_type, **kwargs)
    except Exception:
        print(f"There were problems in loading model {model_type}, default to 'TEST' type!")
        return SummaryModel("TEST")


app = FastAPI()
ai_model = get_summary_model(model_name, **model_params)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/documents/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    db_user = crud.get_document_by_text(db, text=document.text)
    if db_user:
        raise HTTPException(status_code=400, detail="Document with the same text already present in the db!")
    summary = ai_model.get_summary(document.text)
    document_complete = schemas.DocumentCreateComplete(text=document.text, summary=summary)
    return crud.create_document(db=db, document=document_complete)


@app.get("/documents/", response_model=List[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents


@app.get("/documents/{document_id}", response_model=schemas.Document)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document


@app.delete("/documents/{document_id}", response_model=schemas.Document)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.delete_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")
