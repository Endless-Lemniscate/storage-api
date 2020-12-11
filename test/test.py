import pytest
import aiohttp


baseUrl = "http://0.0.0.0:8080"


def test_upload():

    url = baseUrl + '/some'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                resp.read()
                f = await aiofiles.open('/some/file.img', mode='wb')
                await f.write(await resp.read())
                await f.close()
    assert 1 == 0
