from views import upload_handle, download_handle, delete_handle


def setup_routes(app):
    app.router.add_route('POST', '/file', upload_handle)
    app.router.add_route('GET', '/file/{hash}', download_handle)
    app.router.add_route('DELETE', '/file/{hash}', delete_handle)
