FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./
EXPOSE 8000
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0 --chdir=./"
#ENTRYPOINT [ "python","__init__.py" ]
CMD ["gunicorn", "main:app"]