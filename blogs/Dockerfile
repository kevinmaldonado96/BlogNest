FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh /usr/local/bin/start.sh

RUN chmod +x /usr/local/bin/start.sh

COPY ./ ./

EXPOSE 8080

ENTRYPOINT ["start.sh"]