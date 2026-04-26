FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    VIRTUAL_ENV=/opt/venv \
    MPLCONFIGDIR=/tmp/matplotlib \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app

RUN addgroup --system app && \
    adduser --system --ingroup app --home /home/app app && \
    python -m venv "${VIRTUAL_ENV}"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=app:app src/ src/
COPY --chown=app:app utils/ utils/

RUN mkdir -p /tmp/matplotlib && \
    chown -R app:app /app /home/app /tmp/matplotlib "${VIRTUAL_ENV}"

USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3)"

CMD ["streamlit", "run", "src/app.py"]
