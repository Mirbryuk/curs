from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from .schemas import Application, Message
from fastapi.staticfiles import StaticFiles
import os
import uuid
import base64

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Функция для конвертации изображения
async def Image_Converter(Hax_Value):
    # Добавляем символы заполнения, если необходимо
    while len(Hax_Value) % 4 != 0:
        Hax_Value += '='
    random_name = str(uuid.uuid4())  # Генерируем уникальное имя файла
    img_path = f"./static/{random_name}.jpg"  # Формируем путь к файлу
    os.makedirs("static", exist_ok=True)  # Убеждаемся, что директория для сохранения существует
    with open(img_path, 'wb') as decodeit:
        decodeit.write(base64.b64decode(Hax_Value))
    img_url = f"http://localhost:8000/static/{random_name}.jpg"  # Формируем URL изображения
    return img_url

# CORS settings
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/applications/")
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    print(application.dict())  # Логируем полученные данные
    db_application = models.Application(
        phone_number=application.phone_number,
        photo=application.photo,
        longitude=application.longitude,
        latitude=application.latitude,
        description=application.description
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@app.get("/applications/", response_model=list[schemas.Application])
def get_applications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    applications = db.query(models.Application).offset(skip).limit(limit).all()
    return applications

@app.get("/applications/{application_id}", response_model=schemas.Application)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return application

@app.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application:
        db.delete(db_application)
        db.commit()
        return {"message": "Заявка успешно удалена"}
    else:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

@app.post("/messages/")
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = models.Message(
        phone_number=message.phone_number,
        name=message.name,
        message=message.message
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/{message_id}", response_model=schemas.Message)
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")
    return message

@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        return {"message": "Сообщение успешно удалено"}
    else:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")

@app.get("/statistics/")
def read_statistics(db: Session = Depends(get_db)):
    statistics = db.query(models.Statistics).first()
    return statistics

@app.post("/convert_image", tags=["IMAGE"])
async def convert_image(Hax_Value: str):
    img_path = await Image_Converter(Hax_Value)
    return {"converted_image_url": img_path}

IMAGEDIR = os.getcwd()

app.mount("/Static", StaticFiles(directory="static"), name="Static")
