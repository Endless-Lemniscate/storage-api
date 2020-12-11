from views import upload_handle, download_handle, delete_handle


def setup_routes(app):
    app.router.add_route('POST', '/upload', upload_handle)
    app.router.add_route('GET', '/download/{hash}', download_handle)
    app.router.add_route('DELETE', '/delete/{hash}', delete_handle)
