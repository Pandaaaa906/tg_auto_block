FROM python:3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip /tmp/requirements.txt


COPY tg_auto_block /app/tg_auto_block
WORKDIR /app
ENTRYPOINT ["python", "-m", "tg_auto_block.main"]