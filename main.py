from fastapi import FastAPI

import workflows

app = FastAPI()
app.include_router( workflows.router )

if __name__ == "__main__":
	import uvicorn
	uvicorn.run( "main:app" )
