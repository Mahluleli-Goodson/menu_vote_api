from api import settings
from packaging import version


class VoteGuardAPIMiddleware:
    """
    Middleware guards LEGACY Apps using old endpoint for voting, then maps the request to the v1 version, otherwise
    it lets request proceed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if ('menu/vote' not in request.path_info) or (('menu/vote' in request.path_info) and request.method != 'POST'):
            return self.get_response(request)

        # We assume semantic versioning for app
        app_version = version.parse(self.extract_app_version(request))

        if app_version < version.parse(settings.MIN_APP_VERSION):
            if '/api/v1' in request.path_info:
                return self.get_response(request)

            path = request.path_info.replace('/api', '/api/v1')
            request.path_info = path

        return self.get_response(request)

    def extract_app_version(self, request):
        # Extract the app version from the request headers
        # You can customize this based on the actual header field
        return request.headers.get('X-App-Version', '0.0.0')
