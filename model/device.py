from typing import Union

from pydantic import BaseModel


class device(BaseModel):
    device_id: str
    remote_mac: Union[str, None] = None
    device_ip: str
    ip_segment: Union[str, None] = None

    class config:
        schema_extra = {
            "device_id": "0f010f00020004000001",
            "remote_mac": "00-0c-29-74-d3-21",
            "device_ip": "192.1·68.10.119",
            "ip_segment": "192.168.10.0/24"
        }
