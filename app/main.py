from datetime import datetime

import pandas
from fastapi import FastAPI, APIRouter, Form, HTTPException, UploadFile
from fastapi.params import File
from sqlalchemy import and_
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from categorizer.categorizer import get_message_categories
from models import Reviews, engine

app = FastAPI()
router = APIRouter(prefix="/api/v1")
Session = sessionmaker(bind=engine)()

# обычные категории, кастомные, даты, банки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

token = "2f4a309a-e53d-44fb-8041-f7cf0912e35d"


@router.get("/getreviews")
async def get_all_reviews(request: Request, offset: int, limit: int):
    # Rating, Bank, Category, Date
    date = {"to": datetime(1970, 1, 1), "from": datetime.now()}
    data = await request.json()
    where = {}

    if data.get("rating"):
        where["rating"] = data.get("rating")

    if data.get("bank"):
        where["bank"] = data.get("bank")

    if data.get("category"):
        where["category_name"] = data.get("category")

    if data.get("to-date"):
        date["to"] = datetime.strptime(data.get("to-date"), "%Y-%m-%d")

    if data.get("from-date"):
        date["from"] = datetime.strptime(data.get("from-date"), "%Y-%m-%d")

    reviews = Session.query(Reviews).filter(and_(Reviews.publication_date >= date["to"], Reviews.publication_date <= date["from"])).filter_by(**where).order_by(Reviews.id)[offset:limit]
    return {"response": reviews}


@router.post("/")
async def send_info(review: str = Form(...)):
    if len(review.split()) < 4:
        return {"error": "Текст не может быть меньше 4 слов."}

    if len(review.replace(" ", "")) < 12:
        return {"error": "Текст не может быть меньше 12 символов."}

    # rating = requests.post("http://pycharmprojects_model-rating_1:8641/", data={"review": review}).json()["response"]
    # categories = requests.post("http://pycharmprojects_model-categories_1:8642/", data={"review": review})

    custom_categories = get_message_categories(review)

    print(custom_categories)
    if rating < 0 or rating > 1:
        raise HTTPException(status_code=400, detail={"error": "Рейтинг не может быть меньше 0 и больше 1"})

    review = Reviews(publication_date=datetime.now(), review=review, category_id=category[0].id, rating=rating)
    Session.add(review)
    return {"response": {"rating": rating, "categories": categories.json()}}


app.include_router(router)
