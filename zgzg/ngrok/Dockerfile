# https://github.com/wernight/docker-ngrok
FROM chitacan/ngrok

ARG TOKEN
ENV TOKEN $TOKEN

CMD ngrok http mitmproxy:4444 --authtoken $TOKEN --region jp --hostname=$HOST_NAME --log stdout
