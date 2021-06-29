from fastapi import FastAPI

from . import workflows

app = FastAPI()
app.include_router( workflows.router )
