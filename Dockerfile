FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --system --exclude-newer "1 week" -r requirements.txt

COPY *.py ./
COPY handlers/ ./handlers/

CMD ["python", "bot.py"]
