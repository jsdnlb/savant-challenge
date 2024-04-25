from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routers import users, auth
import uvicorn


app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
def not_found(request, exc):
    return JSONResponse(status_code=404, content={"message": "Not Found"})


app.include_router(users.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
