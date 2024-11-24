from typing import Optional
import os

from pydantic import BaseModel

from .constants import MANIFEST_FILE_NAME
from .log_message import log_message


class Manifest(BaseModel):
    class Host(BaseModel):
        domain_name: str = ''
        ip: str = ''
        ssh_key_file: str = ''
        username: str = ''

    container_port: Optional[int] = None
    env_file: Optional[str] = None
    host: Optional[Host] = Host()
    image: Optional[str] = None
    name: str


    def save(self, file_name=MANIFEST_FILE_NAME):
        does_file_already_exist = os.path.exists(file_name)

        with open(file_name, 'w') as file:
            file.write(self.model_dump_json(indent=2))
            log_message('COMPLETE', f"{'Updated' if does_file_already_exist else 'Created'} manifest: {MANIFEST_FILE_NAME}")

        return
