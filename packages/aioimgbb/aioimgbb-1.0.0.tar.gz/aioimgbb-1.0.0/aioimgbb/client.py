import aiohttp

from aioimgbb.image import Image

URL_UPLOAD = 'https://api.imgbb.com/1/upload'


class Client:

    def __init__(self, api_key: str):
        self._api_key = api_key

    async def upload(self, path_to_image: str, **kwargs) -> Image:
        name = kwargs.pop('name', None)
        expiration = kwargs.pop('expiration', None)
        payload = {}

        if name:
            payload.setdefault('name', str(name))
        if expiration:
            payload.setdefault('expiration', str(expiration))

        payload.setdefault('key', self._api_key)

        with open(path_to_image, 'rb') as file:
            payload.setdefault('image', file.read())

        async with aiohttp.ClientSession() as session:
            response = await session.post(URL_UPLOAD, data=payload, verify_ssl=False)
            response_json = await response.json()

        data = Image(
            id=response_json['data']['id'],
            title=response_json['data']['title'],
            url_viewer=response_json['data']['url_viewer'],
            url=response_json['data']['url'],
            display_url=response_json['data']['display_url'],
            size=response_json['data']['size'],
            time=response_json['data']['time'],
            expiration=response_json['data']['expiration'],
        )
        return data
