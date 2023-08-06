class Connection:
    def __init__(self) -> None:
        pass

    def is_connected(self) -> bool:
        return False

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def send(self, data: bytes) -> bytes:
        raise NotImplementedError
  
    async def send_string(self, data: str) -> str:
        response = await self.send(data.encode('utf-8'))
        if response:
           return response.decode('utf-8')
        return ''
