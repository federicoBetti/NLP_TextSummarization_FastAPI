from sqlalchemy.orm import Session

import models, schemas


def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def delete_document(db: Session, document_id: int):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if doc is None:  # no item found
        return None
    else:
        db.delete(doc)
        db.commit()
        return doc


def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()


def get_document_by_text(db: Session, text: str):
    return db.query(models.Document).filter(models.Document.text == text).first()


def create_document(db: Session, document: schemas.DocumentCreateComplete):
    db_item = models.Document(**document.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
