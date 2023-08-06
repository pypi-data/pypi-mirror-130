from pydantic import BaseModel

class MqttMessageMiddlewareClientConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int= 1884
    password: str = 'eHIGH2014'
    username: str = 'admin'


class HttpClientConfig(BaseModel):
    host: str = "http://127.0.0.1"
    port: str = "80"


class RpcClientConfig(BaseModel):
    ip: str = "127.0.0.1"
    port: str = "1884"
    service_name: str = None


