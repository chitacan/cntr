# https://github.com/wernight/docker-ngrok
FROM chitacan/ngrok

ARG TOKEN
ENV TOKEN $TOKEN

EXPOSE 4040

CMD ngrok tcp --authtoken $TOKEN --region jp host.docker.internal:22
