from fastapi import APIRouter, Depends
from tortoise.exceptions import DoesNotExist

from common.deps import Pager
from common.resp import RespSucc, RespPage
from models.base import UtTasks, UtHistories, UtDetails
from schemas.ut import (TaskCreate, TaskUpdate, TaskInfo, HistoryInfo, DetailInfo,
                        task_filter, history_filter, detail_filter)

app = APIRouter(prefix="/ut")


@app.get("/task", response_model=RespPage[TaskInfo], summary="任务列表")
async def get_items(filters: dict = Depends(task_filter), pg: Pager = Depends(Pager)):
    queryset = UtTasks.all()
    data = await pg.output(queryset, filters)
    return RespPage[TaskInfo](data=data)


@app.get("/history", response_model=RespPage[HistoryInfo], summary="历史列表")
async def get_items(filters: dict = Depends(history_filter), pg: Pager = Depends(Pager)):
    queryset = UtHistories.all()
    data = await pg.output(queryset, filters)
    return RespPage[HistoryInfo](data=data)


@app.get("/detail", response_model=RespPage[DetailInfo], summary="详情列表")
async def get_items(filters: dict = Depends(detail_filter), pg: Pager = Depends(Pager)):
    queryset = UtDetails.all()
    data = await pg.output(queryset, filters)
    return RespPage[DetailInfo](data=data)


@app.post("/task", response_model=RespSucc[TaskInfo], summary="创建任务")
async def create_item(info: TaskCreate):
    data = await UtTasks.create(**info.dict())
    return RespSucc(data=data)


@app.get("/task/{pk}", response_model=RespSucc[TaskInfo], summary="获取任务详情")
async def get_item(pk: int):
    data = await UtTasks.filter(id=pk).first()
    return RespSucc(data=data)


@app.patch("/task/{pk}", response_model=RespSucc[TaskInfo], summary="修改任务")
async def get_item(pk: int, info: TaskUpdate):
    await UtTasks.filter(id=pk).update(**info.dict())
    data = await UtTasks.filter(id=pk).first()
    return RespSucc(data=data)


@app.delete("/task/{pk}", response_model=RespSucc, summary="删除任务")
async def get_item(pk: int):
    data = await UtTasks.filter(id=pk).delete()
    return RespSucc(data=data)
