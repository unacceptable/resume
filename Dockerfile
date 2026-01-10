FROM ubuntu:24.04

WORKDIR /app

# Install system dependencies including wkhtmltopdf
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-pip \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt

# Download spaCy language model for NLP processing
RUN python3 -m pip install --break-system-packages https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

COPY . .

ENTRYPOINT ["python3", "resume.py"]
