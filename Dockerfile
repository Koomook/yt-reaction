FROM python:3.7-stretch

WORKDIR /app
# Install required packages and remove the apt packages cache when done.

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "crawler.py"]