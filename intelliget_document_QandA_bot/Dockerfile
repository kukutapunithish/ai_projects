FROM python:3.13.12
WORKDIR /intelliget_document_QandA_bot

COPY . /intelliget_document_QandA_bot
RUN pip install -e .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]