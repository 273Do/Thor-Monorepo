import os
import sys

from fastapi import FastAPI

from src.core.load_env import envs
from src.routers import estimate_sleep, extract_steps

app = FastAPI()

# デバッグ時は print を無効化しない
if not envs.IS_DEBUG:
    sys.stdout = open(os.devnull, "w")

app.include_router(extract_steps.router, prefix=envs.API_V1_PREFIX)
app.include_router(estimate_sleep.router, prefix=envs.API_V1_PREFIX)
