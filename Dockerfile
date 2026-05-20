FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    ninja-build \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    build \
    scikit-build-core>=0.5 \
    pybind11 \
    cmake>=3.15

WORKDIR /workspace

CMD ["/bin/bash"]
