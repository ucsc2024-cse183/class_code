FROM python:3.11-alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add git
RUN apk add chromium
RUN apk add chromium-chromedriver

# upgrade pip
RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/python -m pip install --upgrade mechanize
RUN venv/bin/python -m pip install --upgrade BeautifulSoup4
RUN venv/bin/python -m pip install --upgrade selenium
RUN venv/bin/python -m pip install --upgrade py4web

ADD test.py test.py
CMD ["venv/bin/python", "test.py"]