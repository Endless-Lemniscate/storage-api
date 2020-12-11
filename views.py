from pathlib import Path
from aiohttp import web
import hashlib


STORAGE_FOLDER_NAME = 'store'
Path("./" + STORAGE_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
storage_folder_path = './{}/'.format(STORAGE_FOLDER_NAME)


async def upload_handle(request):
    reader = await request.multipart()
    field = await reader.next()

    try:
        assert field.name == 'file'
        filename = field.filename

        md5 = hashlib.md5()

        path = Path(storage_folder_path + filename)
        with path.open('ab') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)
                md5.update(chunk)

        hash_of_file = md5.hexdigest()
        # create folder
        Path(storage_folder_path + hash_of_file[:2]).mkdir(parents=True, exist_ok=True)
        Path(storage_folder_path + filename).rename(storage_folder_path + hash_of_file[:2] + '/' + hash_of_file)

        print("file {} uploaded".format(hash_of_file))
        response = {"hash": hash_of_file}
        return web.json_response(response)

    except AssertionError:
        response = {'code': 400,
                    'message': 'No field named file in headers'}
        return web.json_response(response, status=400)


async def download_handle(request):
    name = request.match_info.get('hash', None)
    path_to_file = storage_folder_path + name[:2] + "/" + name

    try:
        file = open(path_to_file, 'rb')
        return web.Response(
            headers={'Content-Disposition': 'Attachment'},
            body=file
        )
    except FileNotFoundError:
        response = {'code': 400,
                    'message': 'No file with hash = {}'.format(name)}
        return web.json_response(response, status=400)


async def delete_handle(request):
    name = request.match_info.get('hash', None)
    path_to_file = storage_folder_path + name[:2] + "/" + name

    try:
        Path(path_to_file).unlink(missing_ok=False)
        response = {'code': 200,
                    'message': 'File deleted'}
        return web.json_response(response)
    except FileNotFoundError:
        response = {'code': 400,
                    'message': 'No file with hash = {}'.format(name)}
        return web.json_response(response, status=400)
