# BE

## Django 프로젝트 구조

Project : dopany
- App1 : ETF
- App2 : Company

<br/>

## 개발환경 시작

1. 실행 환경을 준비합니다.<br/>
  (1) 본 레포지토리를 clone 합니다.<br/>
  (2) python version 11을 설치합니다.<br/>
  (3) 프로젝트 최상위 경로(dopany/)에서 dev-requirements.txt의 라이브러리들을 설치합니다.<br/>

2. 로컬 데이터베이스를 준비합니다.<br/>
  (1) 로컬에 PostgreSQL을 설치합니다.<br/>
  (2) PostgreSQL에 데이터베이스를 생성합니다.<br/>
  (3) 프로젝트 최상위 경로(dopany/)에서 .env 파일을 아래와 같이 생성합니다.<br/>

```text
#Database configuration_(2)에서 생성한 데이터베이스 정보
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

3. 데이터를 마이그레이션합니다. 프로젝트 최상위 경로(dopany/)에서 다음의 명령어들을 차례대로 실행합니다.<br/>
  (1) python manage.py makemigrations<br/>
  (2) python manage.py migrate<br/>
  (3) python manage.py preload_etf_app<br/>
  (4) python manage.py preload_company_app<br/>

4. 서버를 실행합니다.<br/>
  (1) 프로젝트 최상위 경로(dopany/)에서 'python manage.py runserver'를 실행합니다.<br/>
  (2) 'localhost:8000/etf' 접속<br/>
