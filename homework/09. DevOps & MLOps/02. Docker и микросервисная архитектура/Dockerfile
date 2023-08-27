FROM continuumio/miniconda3:latest
WORKDIR /app
COPY 1.sh /app/
RUN chmod +x /app/1.sh
RUN conda install -y mlflow boto3 pymysql
CMD ["/app/1.sh"]
