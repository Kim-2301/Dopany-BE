# Dopany

본 프로젝트는 Data Engineering, Django 학습을 위해 진행된 팀 프로젝트입니다.<br/>
**'도메인별 기업 정보를 제공하는 웹서버'** 를 개발하였으며, 제공되는 정보는 아래와 같습니다.
- 도메인별 ETF 대시보드
- 도메인별 기업 리스트
- 기업별 정보, 채용 공고

<br/>

## 웹사이트 화면
![screencapture-127-0-0-1-8000-etf-2024-05-21-12_17_25](https://github.com/Dopany/.github/assets/64184518/917f5064-5f8f-4ddb-8304-d63642cc71a1)
![screencapture-127-0-0-1-8000-company-2024-05-21-13_57_08](https://github.com/Dopany/.github/assets/64184518/3ef9a97b-0021-4a1c-8b11-3a7cec2436cf)
![screencapture-127-0-0-1-8000-company-채용공고](https://github.com/Dopany/.github/assets/64184518/fb1c19fe-d753-455a-a1d5-935a4c265c80)

<br/>

## 기술스택

- Language/Markup : Python, Javascript, HTML, CSS
- Server : Django
- Extraction : Selenium
- Visualizing : Chart.js, D3

<br/>

## 시스템 구조도

![시스템 구조도](https://github.com/Dopany/.github/assets/64184518/07f409d4-276a-4cd2-a552-31a635488507)

<br/>

## API

[API 명세.pdf](https://github.com/Dopany/.github/files/15383691/API.9605c343a9174d839e6add9d37b3b12e.pdf)

<br/>

## ERD

![ERD](https://github.com/Dopany/.github/assets/64184518/9fbec8a8-6061-4ed7-8dc7-8307bff218ea)

## 세부 활동 기록

https://project-public.notion.site/TrendyDE-b56c9458c1d849379155df594f48532f?pvs=4


<br/>
# BE

## Django 프로젝트 구조

Project : dopany
- App1 : ETF
- App2 : Company

<br/>

## 개발환경 시작

1. 실행 환경을 준비합니다.<br/>
  (1) 본 레포지토리를 clone 합니다.<br/>
  (2) python 3.11을 설치합니다.<br/>
  (3) 프로젝트 최상위 경로(dopany/)에서 requirements.txt의 라이브러리들을 설치합니다.<br/>

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
