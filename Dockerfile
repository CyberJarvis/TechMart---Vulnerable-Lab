# TechMart Vulnerable Web Application Lab
# Educational Docker Image - NOT FOR PRODUCTION USE

FROM python:3.13-slim

# Metadata labels
LABEL maintainer="Security Research Team <security@example.com>"
LABEL version="1.0.0"
LABEL description="TechMart Vulnerable Web Application for Security Education"
LABEL org.opencontainers.image.title="TechMart Security Lab"
LABEL org.opencontainers.image.description="Intentionally vulnerable e-commerce platform for security training"
LABEL org.opencontainers.image.source="https://github.com/security-labs/techmart-vulnerable-lab"
LABEL org.opencontainers.image.licenses="Educational Use License"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=development \
    FLASK_DEBUG=1

# Set working directory
WORKDIR /app

# Install system dependencies for security testing tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    netcat-traditional \
    net-tools \
    iputils-ping \
    dnsutils \
    sqlite3 \
    vim-tiny \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create application user (intentionally with weak security for lab purposes)
RUN groupadd -r techmart && useradd -r -g techmart -m techmart

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=techmart:techmart . .

# Create necessary directories with proper permissions
RUN mkdir -p uploads static/uploads database logs \
    && chown -R techmart:techmart /app \
    && chmod 755 uploads static/uploads database logs

# Create sample files for security testing
RUN echo "This is a sample file for download testing." > uploads/sample.txt \
    && echo "Secret configuration data - DO NOT EXPOSE" > uploads/config.txt \
    && echo "Database backup file" > uploads/backup.sql \
    && echo "#!/bin/bash\necho 'System information:'\nuname -a" > uploads/system_info.sh \
    && chmod +x uploads/system_info.sh

# Create educational warning script
RUN echo "#!/bin/bash\n\
echo '============================================================'\n\
echo '🔥 TECHMART VULNERABLE WEB APPLICATION LAB 🔥'\n\
echo '============================================================'\n\
echo '⚠️  WARNING: This application contains intentional vulnerabilities!'\n\
echo '⚠️  DO NOT use this in production environments!'\n\
echo '============================================================'\n\
echo ''\n\
echo '🎯 EDUCATIONAL PURPOSES ONLY:'\n\
echo '   - Security testing and penetration testing practice'\n\
echo '   - Web application security education'\n\
echo '   - Vulnerability assessment training'\n\
echo '============================================================'\n\
echo '🌐 Access the application at: http://localhost:5001'\n\
echo '============================================================'\n" > /app/warning.sh \
    && chmod +x /app/warning.sh

# Create health check script
RUN echo "#!/bin/bash\ncurl -f http://localhost:5001/ || exit 1" > /app/healthcheck.sh \
    && chmod +x /app/healthcheck.sh

# Expose port (changed to 5001 to match our configuration)
EXPOSE 5001

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /app/healthcheck.sh

# Switch to application user (with intentional sudo access for lab purposes)
RUN echo "techmart ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER techmart

# Set up development environment
ENV PATH="/home/techmart/.local/bin:${PATH}"

# Create startup script that shows warning and starts application
RUN echo "#!/bin/bash\n\
/app/warning.sh\n\
exec python app.py" > /app/start.sh \
    && chmod +x /app/start.sh

# Default command
CMD ["/app/start.sh"]

# Optional: Add build arguments for customization
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

LABEL org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${VCS_REF}"
    echo "echo '=============================================='" >> /app/warning.sh && \
    echo "echo '🔥 VULNERABLE LAB ENVIRONMENT 🔥'" >> /app/warning.sh && \
    echo "echo '=============================================='" >> /app/warning.sh && \
    echo "echo '⚠️  WARNING: This contains intentional vulnerabilities!'" >> /app/warning.sh && \
    echo "echo '⚠️  DO NOT use in production environments!'" >> /app/warning.sh && \
    echo "echo '⚠️  Only for educational and testing purposes!'" >> /app/warning.sh && \
    echo "echo '=============================================='" >> /app/warning.sh && \
    echo "echo '🌐 Application running on: http://localhost:5000'" >> /app/warning.sh && \
    echo "echo '🔑 Default credentials: admin/admin123'" >> /app/warning.sh && \
    echo "echo '=============================================='" >> /app/warning.sh && \
    chmod +x /app/warning.sh

# Start command
CMD ["/bin/bash", "-c", "/app/warning.sh && python app.py"]
