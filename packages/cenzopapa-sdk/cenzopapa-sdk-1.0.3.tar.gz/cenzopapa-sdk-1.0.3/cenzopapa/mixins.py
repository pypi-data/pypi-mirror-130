import json

from httpx import AsyncClient

from cenzopapa.schemas import Image, ImageList


async def create_result_images(data):
    for i, result in enumerate(data.results):
        data.results[i] = Image(**result)
    return data


async def create_image(response, images_list=False):
    response.raise_for_status()
    data = response.json()
    if images_list:
        data = ImageList(**data)
        data = create_result_images(data)
    else:
        data = Image(**data)
    return data, response


class ListMixin:
    async def list(self, page=None):
        async with AsyncClient() as client:
            url = await self.generate_url(page=page)
            response = await client.get(url)
            return await create_image(response, True)


class CreateMixin:
    async def create(self, data):
        async with AsyncClient() as client:
            url = await self.generate_url()
            response = client.post(url, data=json.dumps(data))
            return await create_image(response)


class RetrieveMixin:
    async def retrieve(self, pk):
        async with AsyncClient() as client:
            url = await self.generate_url(pk=pk)
            response = await client.get(url)
            return create_image(response)


class UpdateMixin:
    async def update(self, pk, updated_data):
        async with AsyncClient() as client:
            url = self.generate_url(obj_pk=pk)
            response = client.post(url, data=json.dumps(updated_data))
            return create_image(response)


class DeleteMixin:
    async def delete(self, pk):
        async with AsyncClient() as client:
            url = self.generate_url(obj_pk=pk)
            response = client.delete(url)
            return create_image(response)
