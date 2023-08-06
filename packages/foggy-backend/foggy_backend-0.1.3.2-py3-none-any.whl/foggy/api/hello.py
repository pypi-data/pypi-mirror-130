import json
import logging

import falcon

from foggy.filedb import FileDB, DeviceNotRegisteredError

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Hello:
    def on_get(self, req, resp, device_id):
        logging.info(
            f"received Hello from {device_id}"
        )
        try:
            db = FileDB(device_id=device_id)

        except DeviceNotRegisteredError:
            logging.warning(f"{device_id} is not registered => 404")
            raise falcon.HTTPNotFound

        except Exception as exc:
            logging.error(exc)
            raise falcon.HTTPInternalServerError(description=str(exc))

    def on_put(self, req, resp, device_id):
        try:
            device_user = req.media["user"]
            device_name = req.media["device_name"]
            logging.debug(f"registering user {device_user} device {device_id}")

            FileDB.register(user=device_user, device_name=device_name, device_id=device_id)
            db = FileDB(device_id)
            db.create_files_table()
            logging.info(f"New db created: {db.db_path}")

            resp.media = {"password": "no_password_handling_yet"}

        except Exception as exc:
            logging.error(exc)
            raise falcon.HTTPInternalServerError(description=str(exc))
