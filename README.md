# cntr

개인적인 컨테이너들 ❤️

## Build & Run

mitm cumberland

```sh
# create mitm-ca-cert.pem, cumberland.pem
$ docker build -t gcr.io/<PROJECT_ID>/mitm-cumberland:<TAG> -f cumberland.dockerfile .
$ docker run --restart=always -m 100m -d -p 8888:8888 [-p 8081] --name cbld gcr.io/<PROJECT_ID>/mitm-cumberland:<TAG>
```

mitm kanbanize

```sh
$ docker build --build-arg API_KEY=<API_KEY> -t gcr.io/<PROJECT_ID>/mitm-kanbanize:<TAG> -f kanbanize.dockerfile .
$ docker run --restart=always -m 100m -d -p 9999:9999 [-p 8081] --name knz gcr.io/<PROJECT_ID>/mitm-kanbanize:<TAG>
```

ngrok ssh

```sh
$ docker build --build-arg TOKEN=<NGROK_AUTH_TOKEN> -t gcr.io/<PROJECT_ID>/ngrok-ssh:<TAG> -f ssh.dockerfile .
$ docker run --restart=always -m 100m -d -p 4040:4040 --name ngrok-ssh --env REMOTE_ADDR=<ADDR> gcr.io/<PROJECT_ID>/ngrok-ssh:<TAG>
```

## Why?

### [cumberland.dockerfile](https://github.com/chitacan/cntr/blob/master/cumberland.dockerfile)

![](https://user-images.githubusercontent.com/286950/70865916-09f05900-1fa6-11ea-9a0f-888baf05c588.png)

cumberland Websocket API 서버에는 지정된 클라이언트 인증서 (SSL pinning) 를 가진 클라이언트만 접속할 수 있습니다. 응답에 CORS 헤더도 없어, 브라우져 환경에서 cumberland API 를 직접 사용하는 것은 불가능합니다. [mitmproxy](https://mitmproxy.org/) 의 인증서 옵션을 사용하면, 오리진(cumberland API) 요청때 원하는 인증서를 사용해 서버와 연결을 맺을 수 있습니다. 이 연결을 중계하는 포트를 통해 브라우져는 별도의 인증서 설정 없이 cumberland API 서버에 연결할 수 있습니다.

### [kanbanize.dockerfile](https://github.com/chitacan/cntr/blob/master/kanbanize.dockerfile)

![](https://user-images.githubusercontent.com/286950/70881185-207eca80-200f-11ea-87de-6c4510a5ddaa.png)

IntelliJ 의 [Tasks and context](https://www.jetbrains.com/help/idea/managing-tasks-and-context.html) 기능을 완전히 활용하기 위해서는 Task Server 설정이 필요합니다. IntelliJ 가 지원하지 않는 이슈 트래커 서비스는 이슈 목록과 이슈 상세 정보를 조회하는 HTTP API 를 직접 설정해야 합니다. (Generic Server 옵션) 하지만 설정할 수 있는 값들이 너무 제한적이어서 HTTP 헤더에 API Key 를 사용하는 서비스는 등록하는 것이 불가능합니다. HTTP 요청에 API Key 헤더를 추가하도록 [mitmproxy](https://mitmproxy.org/) 를 설정해 IntelliJ 가 지원하지 않는 kanbanize 서비스를 Task Server 로 등록할 수 있습니다.

### [ssh.dockerfile](https://github.com/chitacan/cntr/blob/master/ssh.dockerfile)

![](https://user-images.githubusercontent.com/286950/87880591-cd9a4500-ca2d-11ea-8bc2-6e6381417a0b.gif)

NAT 내에 존재하는 Remote Machine 에 [Visual Studio Code Remote - SSH](https://code.visualstudio.com/docs/remote/ssh) 로 접근할 수 있는 컨테이너를 생성합니다. 컨테이너에서 실행되는 [ngrok](https://github.com/inconshreveable/ngrok) 프로세스는 `host.docker.internal` 도메인을 통해 호스트 머신의 `22` 번 포트를 ngrok reserved TCP address 에 오픈합니다.  인터넷만 가능하면 어디서든 컨테이너가 실행된 Remote Machine 의 프로젝트를 Visual Studio Code 로 작업할 수 있습니다.

> ngrok reserved TCP address 를 사용하기 위해서는 [ngrok Pro](https://ngrok.com/pricing) 가 필요합니다.
