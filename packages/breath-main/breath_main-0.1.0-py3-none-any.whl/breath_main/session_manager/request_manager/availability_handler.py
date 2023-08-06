from breath_api_interface import Request
from breath_main.session_manager.request_manager.request_handler import RequestHandler

class AvailabilityHandler(RequestHandler):

    def __init__(self, session_manager, response_queue):
        super().__init__(response_queue)

        self._available_services = []
        self._session_manager = session_manager

    def register_service(self, service_name:str) -> None:
        self._available_services.append(service_name)

    def handle(self, request: Request) -> None:
        sucess = True
        if request.service_name not in self._available_services:
            sucess = self._session_manager.create_service(request.service_name)
        
        if not sucess:
            resp = request.create_response(False, response_data={"message":"Service no available"})
            self._reponse_queue.insert(resp)
        else:
            self._send_for_next(request)