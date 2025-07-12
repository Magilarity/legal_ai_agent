#############################################
#               Builder stage               #
#############################################
FROM python:3.13-slim AS builder

WORKDIR /app

# System dependencies (including FAISS headers and SWIG)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl procps dos2unix swig libfaiss-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy metadata and install Python dependencies (add fastapi & uvicorn for backend)
COPY pyproject.toml setup.py requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt \
    && pip install --no-cache-dir faiss-cpu openai fastapi uvicorn[standard]

#############################################
#               Runtime stage               #
#############################################
FROM python:3.13-slim

WORKDIR /app

# Additional utilities: curl for healthcheck, dos2unix and libfaiss-dev for FAISS
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl dos2unix libfaiss-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages and CLI utilities from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Make start.sh executable
RUN dos2unix start.sh \
    && chmod +x start.sh

# Expose ports for Streamlit and metrics
EXPOSE 8501 8001

# Default command - run backend, metrics and Streamlit through start.sh
CMD ["sh", "./start.sh"]