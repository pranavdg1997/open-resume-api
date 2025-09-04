# Multi-stage build for OpenResume API Wrapper
# Stage 1: Node.js setup for OpenResume dependencies
FROM node:18-alpine AS node-builder

# Set working directory
WORKDIR /app

# Copy Node.js related files
COPY package*.json ./
COPY openresume_*.js ./

# Install Node.js dependencies
RUN npm ci --only=production

# Stage 2: Python setup with Node.js runtime
FROM python:3.11-slim

# Install Node.js in the Python container
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Node.js dependencies from builder stage
COPY --from=node-builder /app/node_modules ./node_modules
COPY --from=node-builder /app/package*.json ./

# Copy JavaScript bridge files
COPY openresume_*.js ./

# Copy Python requirements first (for better caching)
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.116.1 \
    uvicorn==0.35.0 \
    pydantic==2.11.7 \
    email-validator==2.2.0 \
    reportlab==4.4.3 \
    requests==2.31.0

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p output temp static/fonts

# Copy configuration template
RUN if [ -f config.example.json ]; then cp config.example.json config.json; fi

# Set environment variables
ENV PYTHONPATH=/app
ENV NODE_ENV=production
ENV PORT=5000
ENV HOST=0.0.0.0

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "main.py"]