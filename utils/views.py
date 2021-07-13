import re
import requests
from django.http import HttpResponse
from django.http import QueryDict
from urllib.parse import urlparse


def proxy(url, headers=None, data=None, params=None):
    def view(request):
        requests_args = {
            "params": params or request.GET.copy(),
            "data": data or request.body,
            "headers": headers or {},
        }

        response = requests.request(request.method, url, **requests_args)

        proxy_response = HttpResponse(response.content, status=response.status_code)

        excluded_headers = set(
            [
                # Hop-by-hop headers
                # ------------------
                # Certain response headers should NOT be just tunneled through.  These
                # are they.  For more info, see:
                # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
                "connection",
                "keep-alive",
                "proxy-authenticate",
                "proxy-authorization",
                "te",
                "trailers",
                "transfer-encoding",
                "upgrade",
                # Although content-encoding is not listed among the hop-by-hop headers,
                # it can cause trouble as well.  Just let the server set the value as
                # it should be.
                "content-encoding",
                # Since the remote server may or may not have sent the content in the
                # same encoding as Django will, let Django worry about what the length
                # should be.
                "content-length",
            ]
        )
        for key, value in response.headers.items():
            if key.lower() in excluded_headers:
                continue
            elif key.lower() == "location":
                # If the location is relative at all, we want it to be absolute to
                # the upstream server.
                proxy_response[key] = make_absolute_location(response.url, value)
            else:
                proxy_response[key] = value

        return proxy_response

    return view


def make_absolute_location(base_url, location):
    """
    Convert a location header into an absolute URL.
    """
    absolute_pattern = re.compile(r"^[a-zA-Z]+://.*$")
    if absolute_pattern.match(location):
        return location

    parsed_url = urlparse(base_url)

    if location.startswith("//"):
        # scheme relative
        return parsed_url.scheme + ":" + location

    elif location.startswith("/"):
        # host relative
        return parsed_url.scheme + "://" + parsed_url.netloc + location

    return (
        parsed_url.scheme
        + "://"
        + parsed_url.netloc
        + parsed_url.path.rsplit("/", 1)[0]
        + "/"
        + location
    )
