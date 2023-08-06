FROM python:3.8-slim

# Install dependencies
COPY setup.py setup.py
COPY setup.cfg setup.cfg
COPY pyproject.toml pyproject.toml
COPY MANIFEST.in MANIFEST.in
COPY requirements-min.txt requirements-min.txt
COPY classrad classrad
COPY webapp webapp

RUN apt-get update \
    && apt-get install gcc -y
RUN python -m pip install --upgrade pip && python -m pip install numpy
RUN python -m pip install -e . --no-cache-dir

ENV INPUT_DIR /data
ENV RESULT_DIR /data/results
RUN mkdir -p $INPUT_DIR && mkdir -p $RESULT_DIR

EXPOSE 8501

CMD ["streamlit", "run", "webapp/app.py"]
