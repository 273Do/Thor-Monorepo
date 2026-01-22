from fastapi import FastAPI

from src.core.load_env import envs
from src.routers import estimate_sleep, extract_steps

app = FastAPI()


app.include_router(extract_steps.router, prefix=envs.API_V1_PREFIX)
app.include_router(estimate_sleep.router, prefix=envs.API_V1_PREFIX)
