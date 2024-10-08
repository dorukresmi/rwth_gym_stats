FROM debian:bullseye-slim

USER root

RUN apt-get update && apt-get install -y build-essential cmake pkg-config libjpeg-dev libpng-dev libtiff-dev

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev \
    libuuid1 \
    uuid-dev \
    libasound2 \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    fonts-liberation \
    libxt6 \
    libxrender1 \
    libxcomposite1 \
    libxdamage1 \
    libxcursor1 \
    libxrandr2 \
    libxi6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libnss3 \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz \
    && tar xzf Python-3.11.6.tgz \
    && cd Python-3.11.6 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.11.6.tgz Python-3.11.6

RUN python3.11 -m ensurepip --upgrade \
    && python3.11 -m pip install --upgrade pip

RUN wget -O firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64" \
    && tar -xjf firefox.tar.bz2 \
    && mv firefox /opt/firefox \
    && ln -s /opt/firefox/firefox /usr/local/bin/firefox \
    && rm firefox.tar.bz2

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.35.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.35.0-linux64.tar.gz

ENV PATH="/usr/local/bin:/opt/firefox:${PATH}"
ENV MOZ_HEADLESS=1

WORKDIR /app

RUN git clone https://github.com/dorukresmi/rwth_gym_stats /app

# COPY ./gym_stats ./gym_stats
# COPY main.py .
# COPY requirements_linux.txt .

RUN python3.11 -m venv .venv && \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install --retries=3 -v -r requirements_linux.txt

RUN mkdir -p /app/data && chmod 755 /app/data
VOLUME ["/app/data"]

CMD ["/app/.venv/bin/python", "main.py"]
#ENTRYPOINT ["/bin/bash"]