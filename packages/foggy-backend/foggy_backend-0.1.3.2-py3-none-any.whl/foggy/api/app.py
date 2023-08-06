import os
from pathlib import Path

import falcon
from foggy.api import files, hello, index

def create_app():
    api = falcon.API()
    base_url = "/foggy/api/v0.1"

    url_to_handler = {
        "/hello/{device_id}": hello.Hello(),
        "/index/{device_id}": index.Index(),
        "/files/{device_id}/{identifier}": files.File(),
    }
    for url, handler in url_to_handler.items():
        api.add_route(base_url + url, handler)

    return api


def get_app():
    return create_app()
