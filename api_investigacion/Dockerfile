# API Investigación — FastAPI (puerto 8025)
# Instruccion Docker FROM que configura la construccion o ejecucion de la imagen.
FROM python:3.12-slim

# Instruccion Docker WORKDIR que configura la construccion o ejecucion de la imagen.
WORKDIR /app

# Primero las dependencias y después el código: mientras requirements.txt no
# cambie, Docker reutiliza la capa del pip install y reconstruir es rápido.
# Instruccion Docker ARG que configura la construccion o ejecucion de la imagen.
ARG ARCHIVO_REQUISITOS=requirements.txt
# Instruccion Docker COPY que configura la construccion o ejecucion de la imagen.
COPY requirements*.txt requirements*.lock ./
# Instruccion Docker RUN que configura la construccion o ejecucion de la imagen.
RUN pip install --no-cache-dir -r ${ARCHIVO_REQUISITOS}

# Instruccion Docker COPY que configura la construccion o ejecucion de la imagen.
COPY . .

# Instruccion Docker EXPOSE que configura la construccion o ejecucion de la imagen.
EXPOSE 8025

# Instruccion Docker CMD que configura la construccion o ejecucion de la imagen.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8025"]
