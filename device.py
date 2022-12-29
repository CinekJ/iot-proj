
class Device:
  def __init__(self, client, id):
    self.client = client
    self.id = id
    self.nodes = {}

  async def create(self, client, id):

    self.client = client
    node = client.get_node(id)
    self.name = (await node.read_browse_name()).Name
    node_children = await node.get_children()
    for child in node_children:
      node_name = (await client.get_node(child).read_browse_name()).Name
      self.nodes[node_name] = child
    return self

  async def get(self, nodes):
    n = self.client.get_node(self.nodes[nodes])
    return await n.read_value()

  async def set(self, nodes, value):
    n = self.client.get_node(self.nodes[nodes])
    await n.write_value(value)