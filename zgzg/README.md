# zgzg

personal tunnel for zigzag internal services.

## run

create `.env` file with following content.

```
HOST_NAME=
TARGET_PORT=
TOKEN=
```


```
$ docker-compose build
$ docker-compose up -d
```

## development

ngrok

```
$ ngrok http 4444 --hostname <HOST_NAME> --region jp
```

mitmproxy

```
$ mitmdump -p 4444 --mode reverse:http://127.0.0.1:<TARGET_PORT> -s mitmproxy/allow-x-origin.py
```
