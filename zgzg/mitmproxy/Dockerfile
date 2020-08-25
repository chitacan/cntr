FROM mitmproxy/mitmproxy:5.2

COPY allow-x-origin.py allow-x-origin.py

CMD mitmweb -p 4444 \
      -s allow-x-origin.py \
      --mode reverse:http://host.docker.internal:$TARGET_PORT \
      --no-web-open-browser \
      --web-host 0.0.0.0
