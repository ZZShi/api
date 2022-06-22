from fastapi import FastAPI
from fastapi.exception_handlers import HTTPException, RequestValidationError

from core.events import startup, shutdown
from core.exception import http_error_handler, http422_error_handler, unicorn_exception_handler, UnicornException

app = FastAPI()


app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", shutdown(app))

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
app.add_exception_handler(UnicornException, unicorn_exception_handler)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
