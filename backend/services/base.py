from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

class BaseService:
    def __init__(self, model):
        self.model = model

    def create(self, db: Session, obj_data: dict):
        try:
            obj = self.model(**obj_data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating {self.model.__name__}: {str(e)}")

    def read(self, db: Session, obj_id: str):
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found.")
        return obj

    def update(self, db: Session, obj_id: str, update_data: dict):
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found.")
        try:
            for key, value in update_data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating {self.model.__name__}: {str(e)}")

    def delete(self, db: Session, obj_id: str):
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found.")
        try:
            db.delete(obj)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting {self.model.__name__}: {str(e)}")