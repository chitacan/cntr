FROM mitmproxy/mitmproxy:4.0.4

ARG API_KEY
ENV API_KEY $API_KEY
ENV PORT 9999
ENV HOST https://chainpartners.kanbanize.com
WORKDIR /root
COPY mitmproxy-ca-cert.pem mitmproxy-ca-cert.pem

RUN echo $API_KEY
CMD mitmweb -p $PORT \
      --mode reverse:$HOST \
      --setheader ":~q:apikey:$API_KEY" \
      --setheader ":~q:Accept:application/json" \
      --no-web-open-browser \
      --web-iface 0.0.0.0
