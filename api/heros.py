from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from common.deps import Pager
from db_fast.db import get_session
from common.resp import RespSingle, RespMulti
from db_fast.heros import Heros, HerosCreate, HerosUpdate, heros_filters

app = APIRouter(prefix="/heros")


@app.get("/", response_model=RespMulti[Heros])
def get_items(filters=Depends(heros_filters), pg: Pager = Depends(Pager()), session: Session = Depends(get_session)):
    print(pg)
    print(filters)
    select(Heros).where(Heros.name.in_ == "szz")
    statement = select(Heros).filter_by(**filters).order_by("id")
    statement = select(Heros).filter()
    data = session.exec(statement).all()
    # statement = select(Hero).where(Hero.name == "szz").where(Hero.age == 16).limit(2).offset(3)
    # hero = session.exec(statement).all()
    # session.query()
    # data = pg.output()
    return RespMulti[Heros](data=data)


@app.post("/", response_model=RespSingle[Heros])
def create_item(body: HerosCreate, session: Session = Depends(get_session)):
    item = Heros(**body.dict())
    session.add(item)
    session.commit()
    session.refresh(item)
    return RespSingle[Heros](data=item)


@app.get("/{pk}", response_model=RespSingle[Heros])
async def get_item(pk: int, session: Session = Depends(get_session)):
    statement = select(Heros).where(Heros.id == pk)
    item = session.exec(statement=statement).one()
    return RespSingle[Heros](data=item)


@app.patch("/{pk}", response_model=RespSingle[Heros])
async def modify_item(pk: int, info: HerosUpdate, session: Session = Depends(get_session)):
    statement = select(Heros).where(Heros.id == pk)
    item = session.exec(statement=statement).one()
    for key, val in info.dict().items():
        setattr(item, key, val)
    session.commit()
    session.refresh(item)
    return RespSingle[Heros](data=item)


@app.delete("/{pk}", response_model=RespSingle[Heros])
async def delete_item(pk: int, session: Session = Depends(get_session)):
    item = session.get(Heros, pk)
    session.delete(item)
    session.commit()
    return RespSingle[Heros](data=item)
