FROM python:3.9
WORKDIR .
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8080
COPY . .
CMD ["gunicorn", "wsgi:app", "-b 0.0.0.0:8080"]