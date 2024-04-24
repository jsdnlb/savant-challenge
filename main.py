from dotenv import load_dotenv
from fastapi import FastAPI
from api.routers import users, auth


app = FastAPI()
load_dotenv()

app.include_router(users.router)
app.include_router(auth.router)
