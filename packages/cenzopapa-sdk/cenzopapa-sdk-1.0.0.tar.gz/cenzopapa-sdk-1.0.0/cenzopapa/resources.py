from enum import Enum

from httpx import AsyncClient

from cenzopapa.mixins import ListMixin, RetrieveMixin, create_image
from cenzopapa.resource_client import ResourceClient


class ImageAction(str, Enum):
    FAVORITE = "favorite"
    UNVAFORITE = "unfavorite"
    LIKE = "like"
    UNLIKE = 'unlike'
    RANDOM = 'random'


class ImageResource(
    ResourceClient,
    RetrieveMixin,
    ListMixin,

):
    endpoint = "/images/"

    async def random(self):
        async with AsyncClient() as client:
            url = await self.generate_url(action=ImageAction.RANDOM.value)
            response = await client.get(url)
            return await create_image(response)

    async def __action_mixin(self, pk, action):
        async with AsyncClient() as client:

            url = await self.generate_url(pk=pk, action=action)
            response = client.post(url)
            response.raise_for_status()
            return response

    async def favorite(self, pk):
        return await self.__action_mixin(pk=pk, action=ImageAction.FAVORITE.value)

    async def unfavorite(self, pk):
        return await self.__action_mixin(pk=pk, action=ImageAction.UNVAFORITE.value)

    async def like(self, image_pk):
        return await self.__action_mixin(pk=image_pk, action=ImageAction.LIKE.value)

    async def unlike(self, image_pk):
        return await self.__action_mixin(pk=image_pk, action=ImageAction.UNLIKE.value)


class JWTResource(ResourceClient):
    endpoint = "/auth/jwt"

    def create(self, data):
        url = f"{self.generate_url()}/create"
        return self.session.post(url, data)

    def refresh(self, refresh_token):
        url = f"{self.generate_url()}/refresh"
        return self.session.post(url, {"refresh": refresh_token})
