from typing import Dict, Optional

from fastapi import FastAPI, Body
from dotenv import dotenv_values

import knime

from . import workflows

settings = dotenv_values( ".env" )

env = {
	"executable_path": settings[ "EXECUTABLE_PATH" ],
	"workspace_path": settings[ "WORKSPACE_PATH" ]
}

knime.executable_path = env[ "executable_path" ]

app = FastAPI()
app.include_router( workflows.router )

@app.get( "/env" )
def get_env():
	return env

@app.post( "/env" )
def set_env(
	data = Body(
		...,
		example = env
	),
):
	env.update( data )
	knime.executable_path = env[ "executable_path" ]
	return env

