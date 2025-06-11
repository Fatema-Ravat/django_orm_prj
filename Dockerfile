#official python image
FROM python:3.13.2-alpine3.21
LABEL maintainer="fatelane"

#set working directory
WORKDIR /app

#copy project files
COPY requirements.txt .

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt