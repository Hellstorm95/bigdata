# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME ./
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip3 install -r requirements.txt
