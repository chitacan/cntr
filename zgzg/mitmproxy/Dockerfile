FROM mitmproxy/mitmproxy:5.2

COPY allow-x-origin.py allow-x-origin.py

CMD mitmdump -p 4444 \
      -s allow-x-origin.py \
      --mode reverse:http://host.docker.internal:$TARGET_PORT
