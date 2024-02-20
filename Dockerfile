# Execute with: docker build -t streamlit .
#         Then: docker run -p 8501:8501 --name project_CSD streamlit

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get install -y \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/Meguazy/project_CSD.git .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/app/Tool/streamlitProject/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]