# Python 3.11이 설치된 슬림 이미지 사용
FROM python:3.11-slim

# 파이썬 설정: pyc 파일 생성 방지, 출력 버퍼링 비활성화
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 컨테이너 내부에서 작업할 디렉터리
WORKDIR /app

# 의존성 설치를 위해 requirements.txt만 먼저 복사
COPY requirements.txt /app/

# 필요한 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 소스를 컨테이너 안으로 복사
COPY . /app

# 정적 파일 수집 (STATIC_ROOT로 CSS, JS 등 모으기)
RUN python manage.py collectstatic --noinput

# 컨테이너가 외부에 개방할 포트
EXPOSE 8000

# Gunicorn으로 Django 실행
# ★ 이 프로젝트의 wsgi 모듈은 config.wsgi 이므로 꼭 이렇게 작성해야 함
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
