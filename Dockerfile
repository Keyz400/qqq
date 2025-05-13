FROM python:3.10

# Update package lists and install necessary dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get install -y unzip
# Install ChromeDriver
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    rm chromedriver-linux64.zip

RUN useradd -m -u 1000 user
RUN adduser user sudo
USER user
ENV HOME=/home/user \
  PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Continue with your remaining commands
RUN pip install --no-cache-dir --upgrade pip
COPY --chown=user . $HOME/app

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 app.py & python3 main.py
