from device import Device

class Factory:
    def __init__(self, client):
      self.devices = []
      self.client = client

    async def create(self, client):
      self.client = client
      objects = self.client.get_node("i=85") 
      nodes = await objects.get_children()
      for node in nodes:
          name = (await node.read_browse_name()).Name
          if name != "Server":
              device = Device(self.client, node)
              self.devices.append(await device.create(self.client, node))
      return self
