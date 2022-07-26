import json
from datetime import datetime

import pandas as pd
import requests
from fastapi import FastAPI, APIRouter, Form, HTTPException
from sqlalchemy import and_, func
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from categorizer.categorizer import get_message_categories
from models import Reviews, engine

app = FastAPI()
router = APIRouter(prefix="/api/v1")
Session = sessionmaker(bind=engine, autoflush=True, autocommit=True)()

# Добавляю CORS миддлварь, для удачной связи с фронтом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@router.get("/getreviews/")
async def get_all_reviews(request: Request, offset: int, limit: int):
    # Rating, Bank, Category, Date
    date_to = datetime(1970, 1, 1)
    date_from = datetime.now()
    data = dict(request.query_params.multi_items())
    pre_where = {"rating", "bank", "category_name"}

    where = {k: v for k, v in data.items() if k in pre_where}

    date_to = datetime.strptime(data.get("to-date"), "%Y-%m-%d") if data.get("to-date") else date_to
    date_from = datetime.strptime(data.get("from-date"), "%Y-%m-%d") if data.get("from-date") else date_from

    reviews = Session.query(Reviews).filter(
        and_(Reviews.publication_date >= date_to, Reviews.publication_date <= date_from)).filter_by(**where).order_by(
        func.random())[offset:limit]
    return {"response": reviews}


@router.get("/getstats")
async def get_stats():
    grouped = engine.execute(
        "SELECT count(publication_date), date_trunc('month', publication_date) as publication_date_, bank FROM reviews where publication_date >= '2013-01-01' and bank IS NOT NULL group by reviews.bank, publication_date_ order by bank, publication_date_;")
    grouped = json.loads(
        json.dumps([{z[0]: z[1] for z in i.items()} for i in grouped.all()], indent=4, sort_keys=True, default=str))
    df = pd.DataFrame(grouped)
    dtr = pd.DataFrame({"publication_date_": pd.date_range('01.01.2013', '01.07.2022', freq='MS')})
    list_banks = {}

    for i in ["gpb", "alfa", "pochtabank", "raif", "sberbank", "tinkoff", "vtb"]:
        bank = pd.concat(
            [df.loc[df["bank"] == i], dtr[~dtr.publication_date_.isin(df.loc[df["bank"] == i].publication_date_)]])
        bank["count"].fillna(0, inplace=True)
        bank["bank"].fillna(i, inplace=True)
        bank["publication_date_"] = pd.to_datetime(bank['publication_date_'])
        bank = bank.sort_values(by=["publication_date_"]).reset_index(drop=True)
        bank = bank.groupby('bank').apply(lambda x: x[['count', 'publication_date_']].to_dict("records")).to_dict()
        list_banks[list(bank.keys())[0]] = list(bank.values())[0]

    return list_banks


@router.post("/")
async def send_info(review: str = Form(...)):
    if len(review.split()) < 4:
        return {"error": "Текст не может быть меньше 4 слов."}

    if len(review.replace(" ", "")) < 12:
        return {"error": "Текст не может быть меньше 12 символов."}

    rating = requests.post("http://docker_container_model-rating_1:8641/", data={"review": review}).json()["response"]
    categories = requests.post("http://docker_container_model-categories_1:8642/", data={"review": review})

    custom_categories = get_message_categories(review)

    if rating < 0 or rating > 1:
        raise HTTPException(status_code=400, detail={"error": "Рейтинг не может быть меньше 0 и больше 1"})

    review = Reviews(publication_date=datetime.now(), review=review, category_name=categories.json()[0][0],
                     category_percent=categories.json()[0][1], rating=rating, custom_categories=custom_categories)
    Session.add(review)
    return {"response": {"rating": rating, "categories": categories.json()}}


app.include_router(router)
