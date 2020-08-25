from mitmproxy import http
from mitmproxy.net.http import cookies

def request(flow):
    if "X-Host" in flow.request.headers:
        flow.request.host_header = flow.request.headers["X-Host"]
        flow.request.host = flow.request.headers["X-Host"]

    if "X-Port" in flow.request.headers:
        flow.request.port = flow.request.headers["X-Port"]

    if "X-Scheme" in flow.request.headers:
        flow.request.scheme = flow.request.headers["X-Scheme"]
        if not "X-Port" in flow.request.headers:
            if flow.request.headers["X-Scheme"] == "https":
                flow.request.port = 443
            else:
                flow.request.port = 80

    if flow.request.method == "OPTIONS":
        flow.response = http.HTTPResponse.make(
            200,
            b"",
            {
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Method": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,X-Host,X-Port,X-Scheme"
            }
        )
        return

    flow.request.headers.pop("If-None-Match", None)
    flow.request.headers.pop("If-Modified-Since", None)
    flow.request.headers.pop("X-Host", None)
    flow.request.headers.pop("X-Port", None)
    flow.request.headers.pop("X-Scheme", None)

def response(flow):
    if "Origin" in flow.request.headers:
        flow.response.headers["Access-Control-Allow-Origin"] = flow.request.headers["Origin"]
    else:
        flow.response.headers["Access-Control-Allow-Origin"] = "*"
    if "Set-Cookie" in flow.response.headers:
        cookie_group = cookies.parse_set_cookie_header(flow.response.headers["Set-Cookie"])
        for key, val, attrs in cookie_group:
            if key == 'connect.sid':
                attrs.add('SameSite', 'None')
                attrs.add('Secure', '')
        flow.response.headers["Set-Cookie"] = cookies.format_set_cookie_header(cookie_group)
