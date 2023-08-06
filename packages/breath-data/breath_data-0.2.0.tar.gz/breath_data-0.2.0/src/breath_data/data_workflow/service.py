from breath_api_interface.proxy import ServiceProxy
from breath_api_interface.queue import Queue
from breath_api_interface.service_interface import Service
from breath_api_interface.request import Request, Response

import pandas as pd
from pandas.core import series

import breath_data.data_workflow.open_sus as open_sus
import breath_data.data_workflow.ibge as ibge


from .data_download import BDDownloader, ModelDownloader

workflows = {"BDDownloader": BDDownloader, "ModelDownloader": ModelDownloader}

class DataWorkflow(Service):
    def __init__(self, proxy:ServiceProxy, request_queue:Queue, global_response_queue:Queue):
        '''DataWorkflow constructor.
        '''
        super().__init__(proxy, request_queue, global_response_queue, "DataWorkflow")

    def run(self) -> None:
        '''Run the service, handling requests.
        '''

        request = self._get_request()

        if request is None:
            return

        response : Response = request.create_response(sucess=False, response_data={"message": "Operation not available"})

        if request.operation_name == "run_workflow":
            response = self._run_workflow(request)

        self._send_response(response)

    def _run_workflow(self, request:Request) -> Response:
        '''
            Execute some workflow

            Parameters:
                request:Request - BReATH request. Must have "workflow_name" field with the name of the workflow.

            Return:
                response - operation response.
        '''
        
        if "workflow_name" not in request.request_info:
            return request.create_response(sucess=False, response_data={"message": "Request info don't have workflow name"})

        workflow_name = request.request_info["workflow_name"]

        if workflow_name not in workflows:
            return request.create_response(sucess=False, response_data={"message": "Workflow not recognised"})

        workflow = workflows[workflow_name](self)
        
        try:
            workflow.run()
        except Exception as e:
            return request.create_response(sucess=False, response_data={"message": "Exception at workflow run: "+str(e)})

        return request.create_response(sucess=True)