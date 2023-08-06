from breath_api_interface.queue import Queue
from breath_api_interface.request import Request
from breath_main.session_manager.request_manager.request_handler import RequestHandler


class ValidationHandler(RequestHandler):
    def __init__(self, response_queue:Queue):
        '''ValidationHandler Constructor.
        '''

        super().__init__(response_queue)

    def handle(self, request:Request) -> None:
        '''Validates the request, looking for inconsistencies.

            TODO Implementar validação
        '''
        self._send_for_next(request)