from typing import Dict, Optional

import knime
from fastapi import FastAPI, Body

app = FastAPI()
knime.executable_path = r"/home/sphynx/projects/knime/knime"
workspace_path = r"/mnt/c/Users/king_/knime-workspace/"

@app.get( "/info" )
def read_root():
	return {
		"executable_path": knime.executable_path,
		"workspace_path": workspace_path
	}

@app.get( "/workflows/" )
def list_workflows():
	import os

	def is_workflow( in_path ):
		return True if "workflow.knime" in os.listdir( os.path.join( workspace_path, in_path ) ) else False

	return {
		p: { "is_workflow": is_workflow( p ) }
		for p in os.listdir( workspace_path )
		if not p.startswith( "." )
	}

@app.get( "/workflows/{workflow}" )
def get_workflows( workflow: str ):
	import os
	return os.listdir( os.path.join( workspace_path, workflow ) )

@app.post( "/workflows/{workflow}/run" )
def run_workflow(
	workflow: str,
	data = Body(
		...,
		example = {
			"1": {
				"sepal length": 6.7,
				"sepal width": 3,
				"petal length": 6,
				"petal width": 2
			},
			"2": {
				"sepal length": 5.5,
				"sepal width": 4.2,
				"petal length": 1,
				"petal width": 0.3
			},
		}
	)
):

	from pandas import DataFrame

	with knime.Workflow( workspace_path = workspace_path, workflow_path = workflow ) as wf:
		wf.data_table_inputs[0] = DataFrame.from_dict( data, orient = "index" )
		wf.execute()

		return wf.data_table_outputs[0]
