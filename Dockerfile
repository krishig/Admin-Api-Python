# start by pulling the python image
FROM python:3.8-alpine

RUN pip install --upgrade pip

# switch working directory
WORKDIR /app

ADD . /app

RUN apk --update add gcc musl-dev libffi-dev openssl-dev

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image

# configure the container to run in an executed manner
ENTRYPOINT ["python"]

CMD ["main.py" ]
