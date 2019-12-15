FROM mitmproxy/mitmproxy:4.0.4

ENV PORT 8888
WORKDIR /root
COPY cumberland.pem cert.pem

CMD mitmweb -p $PORT \
      --mode reverse:https://api-v00-cert.cumberlandmining.com \
      --set client_certs=cert.pem \
      --setheader ":~s:Access-Control-Allow-Origin:*" \
      --setheader ":~hq Sec-WebSocket-Extensions:Sec-WebSocket-Extensions:" \
      --no-web-open-browser \
      --web-iface 0.0.0.0
