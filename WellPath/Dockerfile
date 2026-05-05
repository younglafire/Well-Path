# stage 1Base build stage
FROM python:3.13-slim AS builder

RUN mkdir /app

WORKDIR /app
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#UPGRAdE PIP

RUN pip install --upgrade pip

#Copy the Django projectd and the requirements
COPY requirements.txt /app/

#RUN the cmd to install the requirments
RUN pip install --no-cache-dir -r requirements.txt

# stage 2: production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 

# set the working director
WORKDIR /app
#copy application code
COPY --chown=appuser:appuser . . 

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# swithc to non--root user
USER appuser

# expose the application port

EXPOSE 8000

# start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "WellPath.wsgi:application"]
