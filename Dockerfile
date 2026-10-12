FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1 AS builder
WORKDIR /build
COPY pyproject.toml ./
COPY requirements/aks-api.lock.txt ./requirements.lock
COPY src ./src
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.lock \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels .

FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index /wheels/* && rm -rf /wheels \
    && groupadd --gid 10001 pulse && useradd --uid 10001 --gid pulse --no-create-home pulse \
    && mkdir /data && chown 10001:10001 /data
USER 10001:10001
WORKDIR /app
COPY data/contracts/vibration-window.schema.json /app/contracts/vibration-window.schema.json
EXPOSE 8000
CMD ["uvicorn", "pulse.api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--limit-concurrency", "128", "--timeout-keep-alive", "5", "--no-access-log", "--no-proxy-headers"]
