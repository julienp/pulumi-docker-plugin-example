FROM python
WORKDIR /app
COPY __main__.py .
CMD ["python", "/app/__main__.py"]
