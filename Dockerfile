# [중요] 호환성 문제를 피하기 위해 slim 대신 정식(Full) 버전을 사용합니다.
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 파이썬 버퍼링 해제 (로그가 즉시 출력되도록 설정)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# [중요] requirements.txt를 먼저 복사합니다.
COPY requirements.txt /app/

# [중요] 한국 미러 서버(Kakao)를 사용하여 장고 설치 실패를 방지합니다.
RUN pip install --upgrade pip && \
    pip install -i https://mirror.kakao.com/pypi/simple -r requirements.txt

# 나머지 소스 코드를 복사합니다.
COPY . /app/

# (참고: 실행 명령 CMD는 docker-compose.yml에서 제어하므로 여기서는 생략해도 됩니다.)