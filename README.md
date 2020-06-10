# cntr

개인적인 컨테이너들 ❤️

## Build & Run

mitm cumberland

```sh
# create mitm-ca-cert.pem, cumberland.pem
$ docker build -t gcr.io/<PROJECT_ID>/mitm-cumberland:<TAG> -f cumberland.dockerfile .
$ docker run --restart=always -m 100m -d -p 8888:8888 [-p 8081] gcr.io/<PROJECT_ID>/mitm-cumberland:<TAG>
```

mitm kanbanize

```sh
$ docker build --build-arg API_KEY=<API_KEY> -t gcr.io/<PROJECT_ID>/mitm-kanbanize:<TAG> -f kanbanize.dockerfile .
$ docker run --restart=always -m 100m -d -p 9999:9999 [-p 8081] gcr.io/<PROJECT_ID>/mitm-kanbanize:<TAG>
```

ngrok ssh

```sh
$ docker build --build-arg TOKEN=<NGROK_AUTH_TOKEN> -t gcr.io/<PROJECT_ID>/ngrok-ssh:<TAG> -f ssh.dockerfile .
$ docker run --restart=always -m 100m -d -p 4040:4040 gcr.io/<PROJECT_ID>/ngrok-ssh<TAG>
```

## Why?

### [cumberland.dockerfile](https://github.com/chitacan/mitm/blob/master/cumberland.dockerfile)

![](https://user-images.githubusercontent.com/286950/70865916-09f05900-1fa6-11ea-9a0f-888baf05c588.png)

cumberland Websocket API 서버에는 지정된 클라이언트 인증서 (SSL pinning) 를 가진 클라이언트만 접속할 수 있습니다. 응답에 CORS 헤더도 없어, 브라우져 환경에서 cumberland API 를 직접 사용하는 것은 불가능합니다. [mitmproxy](https://mitmproxy.org/) 는 지정된 인증서를 사용해 cumberland API 서버에 연결할 수 있습니다. 이 연결을 중계하는 포트를 통해 브라우져는 별도의 인증서 설정 없이 cumberland API 서버에 연결할 수 있습니다.

### [kanbanize.dockerfile](https://github.com/chitacan/mitm/blob/master/kanbanize.dockerfile)

![](https://user-images.githubusercontent.com/286950/70881185-207eca80-200f-11ea-87de-6c4510a5ddaa.png)

IntelliJ 의 [Tasks and context](https://www.jetbrains.com/help/idea/managing-tasks-and-context.html) 기능을 완전히 활용하기 위해서는 Task Server 설정이 필요합니다. IntelliJ 가 지원하지 않는 이슈 트래커 서비스는 이슈 목록과 이슈 상세 정보를 조회하는 HTTP API 를 직접 설정해야 합니다. (Generic Server 옵션) 하지만 설정할 수 있는 값들이 너무 제한적이어서 HTTP 헤더에 API Key 를 사용하는 서비스는 등록하는 것이 불가능합니다. HTTP 요청에 API Key 헤더를 추가하도록 [mitmproxy](https://mitmproxy.org/) 를 설정해 IntelliJ 가 지원하지 않는 kanbanize 서비스를 Task Server 로 등록할 수 있습니다.
