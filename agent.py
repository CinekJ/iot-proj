import json
from azure.iot.device import IoTHubDeviceClient, Message

class Agent:
  def __init__(self, device, connection_string):
    self.device = device
    self.connection_string = connection_string
    self.iotClient= IoTHubDeviceClient.create_from_connection_string(self.connection_string)
    self.iotClient.connect()


  async def telemetry(self):
    data = {
      "ProductionStatus": await self.device.get("ProductionStatus"),
      "WorkorderId": await self.device.get("WorkorderId"),
      "GoodCount":await self.device.get("GoodCount"),
      "BadCount":await self.device.get("BadCount"),
      "Temperature":  await self.device.get("Temperature"),
    }
    print(data)
    msg = Message(json.dumps(data), "UTF-8", "JSON")
    self.iotClient.send_message(msg)