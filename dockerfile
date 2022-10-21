FROM python:3.9
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysql-connector-python pandas

CMD ["python", "./project_up.py"]