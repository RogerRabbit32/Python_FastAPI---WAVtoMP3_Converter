FROM python:3.9

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /code
COPY . /code/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
