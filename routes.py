from handlers import upload_handle, download_handle, delete_handle


def setup_routes(app):
    app.router.add_route('POST', '/api/file', upload_handle)
    app.router.add_route('GET', '/api/file/{hash}', download_handle)
    app.router.add_route('DELETE', '/api/file/{hash}', delete_handle)
