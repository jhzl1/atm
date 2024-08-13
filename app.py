from fastapi import FastAPI
from dotenv import dotenv_values
from domains.users.router import users_router
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")


app = FastAPI(root_path="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
