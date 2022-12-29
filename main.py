from asyncua import Client
from asyncio import get_event_loop, sleep
from config import Config
from factory import Factory
from device import Device
from agent import Agent

async def main():
  config = Config()

  url = config.getUrl

  async with Client(url=url) as client:
    factory = Factory(client)
    await factory.create(client)

    agentList = []

    for device in factory.devices:
      agent = Agent(device, config.get_device_connection_string('devices', device.name))
      agentList.append(agent)

    while True:
      for agent in agentList:
        await agent.telemetry()
      await sleep(5)

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())