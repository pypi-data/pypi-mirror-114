from typing import Any, Callable
from .cherrypie_config import CherryPieConfig
import time
from flask.app import Flask
import requests
from flask import request, Response

class CherryPie:
    def __init__(
        self,
        api_key: str,
        identity_function: Callable[[Any], None] = lambda req: None,
        debug_mode: bool = False,
        cherrypie_api_url = CherryPieConfig.CHERRYPIE_API_URL,
        timeout: int = 3,
    ):
        self.config = CherryPieConfig(
            api_key=api_key,
            cherrypie_api_url=cherrypie_api_url,
            identity_function=identity_function,
            debug_mode=debug_mode,
            timeout=timeout,
        )

    def init_app(self, app: Flask):
        self.config.LOGGER.info(
            "Initializing hooks for CherryPie",
        )
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def before_request(self):
        try:
            request.cp_start_ts = time.time()
            request.cp_body = None
            if request.data:
                request.cp_body = request.data or ""
        except Exception as e:
            self.config.LOGGER.exception(e)

    def after_request(self, response: Response):
        try:
            if not self.config.DEBUG_MODE:
                # Only send logs if not in development
                diff = time.time() - request.cp_start_ts
                payload = {
                    "logEntry": {
                        "account": self.config.IDENTITY_FUNCTION(request),
                        "clientIP": request.environ.get("REMOTE_ADDR"),
                        "request": self.build_request_payload(request),
                        "response": self.build_response_payload(response),
                        "responseTime": diff * 1000, # ms
                    }
                }
                url = '{}/v1/logs'.format(self.config.CHERRYPIE_API_URL)
                r = requests.post(
                    url,
                    headers=self.build_headers(),
                    json=payload,
                    timeout=self.config.TIMEOUT,
                )
                if r.status_code != 200:
                    self.config.LOGGER.warning('Cherrypie log status_code {}'.format(r.status_code))
        except Exception as e:
            self.config.LOGGER.exception(e)
        finally:
            return response

    def build_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.config.CHERRYPIE_API_KEY),
        }

    def build_request_payload(self, request: request):
        body = None
        if request.cp_body:
            body = request.cp_body.decode('utf-8')
        return {
            "path": request.full_path,
            "method": request.method,
            "headers": dict(request.headers),
            "body": body,
        }

    def build_response_payload(self, response: Response):
        body = None
        if response.data:
            body = response.data.decode('utf-8')
        return {
            "headers": dict(response.headers),
            "body": body,
            "statusCode": response.status_code,
        }
