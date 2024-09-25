FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyter

EXPOSE 8080

CMD ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8080", "--no-browser", "--allow-root"]
