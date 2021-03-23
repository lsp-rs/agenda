FROM python:3.8.2-slim

RUN set -ex \
    && buildDeps=' \
        gcc \
        libbz2-dev \
        libc6-dev \
        libgdbm-dev \
        liblzma-dev \
        libncurses-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libpcre3-dev \
        make \
        tcl-dev \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev \
        default-libmysqlclient-dev \
        python3-dev \
        python-setuptools \
        openssh-server \
        apache2 \
        gettext \
        freetds-dev \
    ' \
    && deps=' \
        libexpat1 \
    ' \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip && pip install uwsgi \
    && find /usr/local -depth \
    \( \
        \( -type d -a -name test -o -name tests \) \
        -o \
        \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    \) -exec rm -rf '{}' +


COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN unlink /etc/localtime
RUN ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

WORKDIR /app
COPY ./ /app
EXPOSE 5000
CMD ["uwsgi", "--ini", "wsgi.ini"]