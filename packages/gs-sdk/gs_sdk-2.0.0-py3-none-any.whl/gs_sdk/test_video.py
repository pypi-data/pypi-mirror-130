import sys
from . import camera

data = {
    "things_id": 3, "card_id": 100001, "position": "3.0,4.0,0",
    "metadata": {"alarm_record_id": 1, "process_node_id": "bd0024a8-b503-484d-b9eb-fdea9a17761c"}
}

def call(*args):
    print(*args)
    print(args[2].topic, args[2].payload)
    sys.exit(1)

# sdk.SdkInterface.login(
#     username='admin', password='c93ccd78b2076528346216b3b2f701e6', http_api_version='4.7.1'
# )

# mqtt
# sdk.SdkInterface.query_start(data)
# sdk.SdkInterface.test_subscribe(call)

# rpc
res = camera.start(data)
print(res)
