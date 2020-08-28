import json
import urllib.parse
from mitmproxy import http
from mitmproxy.net.http import cookies

def updateOrigin(flow, parsed):
     port = 443 if parsed.scheme == "https" else 80
     flow.request.scheme = parsed.scheme
     flow.request.host_header = parsed.hostname
     flow.request.host = parsed.hostname
     flow.request.port = parsed.port if parsed.port else port

def request(flow):
    # handle "origin" cookie
    if "Cookie" in flow.request.headers:
        cookie_group = cookies.parse_set_cookie_header(flow.request.headers["Cookie"])
        for key, val, attrs in cookie_group:
            if key == "origin":
                parsed = urllib.parse.urlparse(val)
                updateOrigin(flow, parsed)
                flow.request.headers["X-Forwarded-For"] = "::1"

    # handle "origin" query params
    if "origin" in flow.request.query:
         parsed = urllib.parse.urlparse(flow.request.query["origin"])
         updateOrigin(flow, parsed)

    # handle X-Origin: https://host:port (not support path yet)
    if "X-Origin" in flow.request.headers:
         parsed = urllib.parse.urlparse(flow.request.headers["X-Origin"])
         updateOrigin(flow, parsed)

    # handle OPTIONS
    if flow.request.method == "OPTIONS":
        flow.response = http.HTTPResponse.make(
            200,
            b"",
            {
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Method": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,X-Origin"
            }
        )
        return

    # handle GET /__get_cookie
    if flow.request.method == "GET" and flow.request.path_components == ("__get_cookie",):
        flow.response = http.HTTPResponse.make(
            200,
            json.dumps(flow.request.cookies.items(True)),
            {
                "Access-Control-Allow-Credentials": "true",
                "Content-Type": "application/json"
            }
        )
        return

    # handle GET /__set_cookie?name=<name>&value=<value>
    if flow.request.method == "GET" and flow.request.path_components == ("__set_cookie",):
        name = flow.request.query["name"]
        value = flow.request.query["value"]
        flow.response = http.HTTPResponse.make(
            200,
            b"",
            {
                "Access-Control-Allow-Credentials": "true",
                "Set-Cookie": f"{name}={value}; SameSite=None; Secure; HttpOnly; Path=/;"
            }
        )
        return

    # handle GET /__delete_cookie?name=<name>
    if flow.request.method == "GET" and flow.request.path_components == ("__delete_cookie",):
        name = flow.request.query["name"]
        flow.response = http.HTTPResponse.make(
            200,
            b"",
            {
                "Access-Control-Allow-Credentials": "true",
                "Set-Cookie": f"{name}=; SameSite=None; Secure; HttpOnly; Path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT"
            }
        )
        return

    flow.request.headers.pop("If-None-Match", None)
    flow.request.headers.pop("If-Modified-Since", None)
    flow.request.headers.pop("X-Origin", None)

def response(flow):
    flow.response.headers["Access-Control-Allow-Credentials"] = "true"

    if "origin" in flow.request.query:
        flow.response.headers["Set-Cookie"] = f"origin={flow.request.query['origin']}"

    if "Origin" in flow.request.headers:
        flow.response.headers["Access-Control-Allow-Origin"] = flow.request.headers["Origin"]
    else:
        flow.response.headers["Access-Control-Allow-Origin"] = "*"

    if "Set-Cookie" in flow.response.headers:
        cookie_group = cookies.parse_set_cookie_header(flow.response.headers["Set-Cookie"])
        for key, val, attrs in cookie_group:
            if key in ("connect.sid", "ZigzagMarketingCenter"):
                attrs.add("SameSite", "None")
                attrs.add("Secure", '')
        flow.response.headers["Set-Cookie"] = cookies.format_set_cookie_header(cookie_group)
