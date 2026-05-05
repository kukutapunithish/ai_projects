FROM python:3.13.12
WORKDIR /support_chatbot

COPY . /support_chatbot
RUN pip install -e .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]