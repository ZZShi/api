from aioredis import Redis
from fastapi import APIRouter, Request


app = APIRouter(prefix="/common")


@app.get("/redis/info")
def redis_info():
    return {}


@app.get("/redis/set")
async def redis_set(req: Request):
    redis: Redis = await req.app.state.cache
    rst = redis.set(name="szz", value="100")
    return {"aaa": 111}
