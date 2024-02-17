FROM python:3.10-bookworm

WORKDIR /app
 
RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y python3-pip

COPY . /app

RUN chmod 755 /

RUN pip install -U pip \
   && pip install -r requirements.txt

# Expose the port that uvicorn will run on
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
