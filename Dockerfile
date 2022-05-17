FROM python:3.9-slim

RUN apt-get update && \
	apt-get install -y wget && \
	wget https://dl.influxdata.com/telegraf/releases/telegraf_1.22.3-1_amd64.deb && \
	dpkg -i telegraf_1.22.3-1_amd64.deb

COPY telegraf.conf  /telegraf.conf
COPY app.py ./

CMD ["python3", "app.py"]
