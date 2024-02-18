# Execute with: docker build -t streamlit .
#         Then: docker run -p 8501:8501 streamlit

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Meguazy/project_CSD.git .

RUN pip3 install -r requirements.txt

RUN cd /app/project_CSD/Tool/streamlitProject

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]