FROM ubuntu:22.04

WORKDIR /app

ADD https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_arm64.deb .

RUN apt-get update && \
      apt-get install -y ./wkhtmltox_0.12.6.1-3.jammy_arm64.deb python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "resume.py"]
