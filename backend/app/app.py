from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse, RedirectResponse

from backend.logging import log_info
import hashlib

from backend.database.database import get_db
import backend.database.models


app = FastAPI()


#----For Web----
@app.get("/", response_class=JSONResponse)
async def user_login_request():
    return {"Hello":"Hello Worls"}
#----End For Web----

@app.post("/login_request", response_class=JSONResponse)
async def user_login_request():
    raise NotImplementedError

@app.get("/login_credentials", response_class=JSONResponse)
async def user_login_approval():
    raise NotImplementedError

@app.post("/register", response_class=JSONResponse)
async def user_register_request():
    raise NotImplementedError

@app.post("/logout_request", response_class=JSONResponse)
async def logout_request():
    raise NotImplementedError

@app.get("/user_profile", response_class=JSONResponse)
async def get_user_data():
    raise NotImplementedError

@app.put("/calendar_update_request", response_class=JSONResponse)
async def changes_to_calendar():
    raise NotImplementedError

@app.get("/calendar_update_retrival", response_class=JSONResponse)
async def changes_from_calendars():
    raise NotImplementedError

@app.get("/weekly_schedule", response_class=JSONResponse)
async def weekly_schedule():
    raise NotImplementedError

@app.post("/qr_code_request", response_class=JSONResponse)
async def qr_code_request():
    raise NotImplementedError

@app.get("/create_and_send_qr_code", response_class=JSONResponse)
async def creation_of_qr():
    raise NotImplementedError

@app.post("/add_to_group_request", response_class=JSONResponse)
async def add_to_calendar_request():
    raise NotImplementedError

@app.get("/send_push_notification", response_class=JSONResponse)
async def send_notification():
    raise NotImplementedError