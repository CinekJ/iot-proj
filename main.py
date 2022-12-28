from asyncua import Client
from asyncio import get_event_loop
from config import Config

async def main():
  config = Config()

  url = config.getUrl

  async with Client(url=url) as client:
    devices = await client.get_objects_node().get_children()

    for device in devices:
      name = (await device.read_browse_name()).Name

      if (name != 'Server'):
        connection_string = config.get_device_connection_string('devices', name)

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())