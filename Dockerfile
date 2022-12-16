FROM python:3

WORKDIR /usr/src/espelca
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["flask","--app","espelca","run","--host","0.0.0.0"]