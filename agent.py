import json
from azure.iot.device import IoTHubDeviceClient, Message
import asyncio
from asyncua import ua
class Agent:
  def __init__(self, device, connection_string):
    self.device = device
    self.connection_string = connection_string
    self.iotClient= IoTHubDeviceClient.create_from_connection_string(self.connection_string)
    self.iotClient.connect()
    self.iotClient.on_twin_desired_properties_patch_received = self.desiredPropertiesPatchReceived
    self.tasks=[]

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

  async def patchTwinReportedProperties(self, prop):
    self.iotClient.patch_twin_reported_properties(prop)

  async def createTasks(self):
    tasks = [asyncio.create_task(task) for task in self.tasks]

    tasks.append(
      asyncio.create_task(self.patchTwinReportedProperties({'DeviceError': await self.device.get("DeviceError")}))
    )

    tasks.append(
      asyncio.create_task(self.patchTwinReportedProperties({'ProductionRate': await self.device.get("ProductionRate")}))
    )

    tasks.append(
      asyncio.create_task(self.telemetry())
    )

    self.tasks = []
    return tasks

  def desiredPropertiesPatchReceived(self, patch):
    if "ProductionRate" in patch:
      self.tasks.append(self.device.set("ProductionRate", ua.Variant(patch["ProductionRate"], ua.VariantType.Int32)))
    if "DeviceError" in patch:
      self.tasks.append(self.device.set("DeviceError", ua.Variant(patch["DeviceError"], ua.VariantType.Int32)))