import asyncio

from aioimgbb.client import Client
from aioimgbb.image import Image

api_key = 'ade393986cbcbc88145bd537cd7b2987'

async def main():
    client = Client(api_key)
    image: Image = await client.upload('img1.jpg')
    image2: Image = await client.upload('img2.jpg', name='cat', expiration=10)


asyncio.run(main())