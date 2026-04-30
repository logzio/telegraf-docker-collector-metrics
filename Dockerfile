FROM python:3.12-slim

RUN apt-get update && \
	apt-get install -y wget && \
    wget https://dl.influxdata.com/telegraf/releases/telegraf_1.37.1-1_amd64.deb && \
	dpkg -i telegraf_1.37.1-1_amd64.deb && \
    rm telegraf_1.37.1-1_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY app.py ./

RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["python3", "app.py"]
