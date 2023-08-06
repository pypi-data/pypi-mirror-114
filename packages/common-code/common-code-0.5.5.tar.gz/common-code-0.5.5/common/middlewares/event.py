import json
from queue import Queue
from threading import Thread

from django.utils.deprecation import MiddlewareMixin

from common.logging_config import logger


class EventMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.q = Queue()
        Thread(target=self.send_event).start()

    def process_response(self, request, response):
        if response.status_code < 300 and request.method != 'GET':
            self.parsing(request, response)
        return response

    def parsing(self, request, response):
        data = json.loads(request.body)
        self.q.put(data)

    def send_event(self):
        while True:
            try:
                body = self.q.get()


            except Exception as e:
                logger.exception(e)
