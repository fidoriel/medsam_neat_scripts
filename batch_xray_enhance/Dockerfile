FROM python:3.11

ENV DEBIAN_FRONTEND=nointeractive
ENV PYTHONUNBUFFERED=1

RUN apt-get install -y git

RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/asalmada/x-ray-images-enhancement.git
RUN sed -i '/scipy==1.9.1/d' x-ray-images-enhancement/requirements.txt
RUN pip install -r x-ray-images-enhancement/requirements.txt

RUN apt-get update -y
RUN apt-get install -y parallel
COPY . .

CMD [ "bash /app/batch.sh" ]