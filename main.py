import uvicorn
from fastapi import FastAPI

from config import settings
from common.events import startup, shutdown
from api import ut

app = FastAPI(
    debug=settings.APP_DEBUG
)


app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", shutdown(app))


app.include_router(ut, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(app="main:app")
