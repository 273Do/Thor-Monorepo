from fastapi import FastAPI

from load_env import get_envs
from src.routers import extract_steps

app = FastAPI()

envs = get_envs()

app.include_router(extract_steps.router, prefix=envs.API_V1_PREFIX)
