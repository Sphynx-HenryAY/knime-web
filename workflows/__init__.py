from fastapi import APIRouter, Body, Response
from dotenv import dotenv_values

import knime

settings = dotenv_values( ".env" )

env = {
	"executable_path": settings[ "EXECUTABLE_PATH" ],
	"workspace_path": settings[ "WORKSPACE_PATH" ]
}

knime.executable_path = env[ "executable_path" ]


router = APIRouter(
	prefix = "/workflows",
	tags = [ "workflows" ]
)

@router.get( "/" )
def list_workflows():
	import os

	workspace_path = env[ "workspace_path" ]

	def is_workflow( in_path ):
		return True if "workflow.knime" in os.listdir( os.path.join( workspace_path, in_path ) ) else False

	return {
		p: { "is_workflow": is_workflow( p ) }
		for p in os.listdir( workspace_path )
		if "." in p
	}

@router.get( "/show/{workflow:path}" )
def get_workflow( workflow: str ):
	with knime.Workflow( workspace_path = env[ "workspace_path" ], workflow_path = workflow ) as wf:
		return Response( wf._adjust_svg() )

@router.post( "/run/{workflow:path}" )
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

	with knime.Workflow( workspace_path = env[ "workspace_path" ], workflow_path = workflow ) as wf:
		wf.data_table_inputs[0] = DataFrame.from_dict( data, orient = "index" )
		wf.execute()

		return wf.data_table_outputs[0]
