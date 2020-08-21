FROM mitmproxy/mitmproxy:5.2

COPY allow-cross-site.py allow-cross-site.py

CMD mitmweb -p 4444 \
      -s allow-cross-site.py \
      --mode reverse:http://host.docker.internal:$TARGET_PORT \
      --no-web-open-browser \
      --web-host 0.0.0.0
