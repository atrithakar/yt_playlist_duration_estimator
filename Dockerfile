FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --no-compile --prefix=/install -r requirements.txt


FROM python:3.12-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser -D -H appuser

COPY --from=builder /install /usr/local
COPY app.py get_durations.py ./
COPY static ./static
COPY templates ./templates

USER appuser

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "app:app"]