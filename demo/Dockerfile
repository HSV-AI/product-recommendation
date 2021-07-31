FROM python:3.7
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /app
WORKDIR /app
CMD ["streamlit", "run", "streamlit_demo.py"]