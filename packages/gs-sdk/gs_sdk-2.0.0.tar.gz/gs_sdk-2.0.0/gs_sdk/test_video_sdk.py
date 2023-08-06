import sys
import uuid
from pydantic import BaseModel, Field
sys.path.append("../..")
from Core.HGHttpServer.HttpServer import HttpServer
from Core.HGPythonWorker import HGPythonWorker
from Core.MqttClient import MQTT

RPC_PORT_MAIN = 10000
TOPIC_QUERY = r"gs/record/start/req"
TOPIC_REPLY = r"gs/record/start/res"

some_things = []


def get_uuid():
    return uuid.uuid1().hex


class Event(BaseModel):
    '''
    {"things_id": 1, "card_id": 100, "position": "1.0,2.5,0",
    "metadata": {"alarm_record_id": 1, "process_node_id": "bd0024a8-b503-484d-b9eb-fdea9a17761c}
    '''
    things_id: int = Field(..., description='事物id')
    card_id: int = Field(..., description='定位卡id')
    position: str = Field(..., description='位置以逗号分隔')
    metadata: dict = Field(..., description='节点信息')
    task_uuid: str = Field(default_factory=get_uuid, description='任务uuid用于查询文件')
    camera_id: int = Field(0, description='返回摄像机id，空为不存在')
    status: int = Field(0, description='返回录像状态，负值为失败')


def start(data: Event, _topic) -> Event:
    global some_things
    data = Event(**data)
    if data.metadata in some_things:
        return None

    print('start', data)
    some_things.append(data.metadata)
    data.camera_id = 1
    data.status = 1
    data = data.dict()
    MQTT.publish(TOPIC_REPLY, data)
    print('reply', data)
    return data


MQTT.addTopicHandler(TOPIC_QUERY, start)


class HttpAPIServer(object):
    def start(self, data):
        try:
            return start(data, False)
        except Exception as err:
            return None


server = HttpServer(RPC_PORT_MAIN)
testServer = HttpAPIServer()
server.addClass({"gs_camera_record": testServer})
# register_service(Config.RPC_NAME_MAIN, Config.RPC_PORT_MAIN)
HGPythonWorker.run([server], mq=MQTT)
