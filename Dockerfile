
FROM python:3.9

# # Install JDK
RUN apt-get update 
RUN wget https://download.oracle.com/java/22/latest/jdk-22_linux-x64_bin.deb
RUN dpkg -i jdk-22_linux-x64_bin.deb
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

