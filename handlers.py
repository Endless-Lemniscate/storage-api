from pathlib import Path
from aiohttp import web
import aiofiles
import tempfile
import hashlib
import yaml


cfg = yaml.full_load(open("config.yaml", "r"))
STORAGE_FOLDER_NAME = cfg.get('storage_folder_name')
Path("./" + STORAGE_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
storage_folder_path = './{}/'.format(STORAGE_FOLDER_NAME)


async def upload_handle(request):
    reader = await request.multipart()
    field = await reader.next()

    try:
        assert field.name == 'file'
    except AssertionError:
        response = {'code': 400,
                    'message': 'No field named file in headers'}
        return web.json_response(response, status=400, reason='No field named file in headers')

    tmp_name = next(tempfile._get_candidate_names())
    md5 = hashlib.md5()

    tmp_path = Path(storage_folder_path + tmp_name)
    async with aiofiles.open(tmp_path, 'ab') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            await f.write(chunk)
            md5.update(chunk)

    hash_of_file = md5.hexdigest()
    Path(storage_folder_path + hash_of_file[:2]).mkdir(parents=True, exist_ok=True)
    Path(storage_folder_path + tmp_name).rename(storage_folder_path + hash_of_file[:2] + '/' + hash_of_file)

    print("file {} uploaded".format(hash_of_file))
    response = {"hash": hash_of_file}
    return web.json_response(response, status=200, reason='File uploaded successfully')


async def download_handle(request):
    name = request.match_info.get('hash', None)

    # verify hash is hexadecimal
    try:
        int(name, 16)
    except ValueError:
        response = {'code': 401, 'message': 'Not valid hash'}
        return web.json_response(response, status=401, reason='Not valid hash')

    path_to_file = storage_folder_path + name[:2] + "/" + name
    try:
        async with aiofiles.open(path_to_file, 'rb') as f:
            return web.Response(
                headers={'Content-Disposition': 'Attachment'},
                body=await f.read()
            )
    except FileNotFoundError:
        response = {'code': 400,
                    'message': 'No file with specified hash found'}
        return web.json_response(response, status=400, reason='No file with specified hash found')


async def delete_handle(request):
    name = request.match_info.get('hash', None)

    # verify hash is hexadecimal
    try:
        int(name, 16)
    except ValueError:
        response = {'code': 401, 'message': 'Not valid hash'}
        return web.json_response(response, status=401, reason='Not valid hash')

    path_to_file = storage_folder_path + name[:2] + "/" + name

    try:
        Path(path_to_file).unlink(missing_ok=False)
        response = {'code': 200,
                    'message': 'File deleted successfully'}
        return web.json_response(response)
    except FileNotFoundError:
        response = {'code': 400,
                    'message': 'No file with specified hash found'}
        return web.json_response(response, status=400, reason='No file with specified hash found')
