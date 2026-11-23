# Dockerfile del FRONT — Flask + Jinja2, puerto 8078.
#
# LA API DE ESTE MÓDULO TAMBIÉN ESTÁ EN PYTHON, y eso hace que la separación
# entre los dos procesos haya que sostenerla a pulso: nada impide, salvo la
# disciplina, importar el código de la API desde aquí. Por eso el front vive
# en su propia imagen, con sus propias dependencias —Flask y requests, ni
# FastAPI ni el driver de PostgreSQL— y lo único que comparten es el JSON.
#
# Fíjese en lo que este archivo NO instala: `asyncpg`. La ausencia no es un
# olvido, es la comprobación. Este proceso no puede llegar a la base de datos
# ni queriendo.
# Instruccion Docker FROM que configura la construccion o ejecucion de la imagen.
FROM python:3.12-slim

# Instruccion Docker WORKDIR que configura la construccion o ejecucion de la imagen.
WORKDIR /app

# Primero las dependencias y después el código: mientras requirements.txt no
# cambie, Docker reutiliza la capa del pip install.
# Instruccion Docker ARG que configura la construccion o ejecucion de la imagen.
ARG ARCHIVO_REQUISITOS=requirements.txt
# Instruccion Docker COPY que configura la construccion o ejecucion de la imagen.
COPY requirements*.txt requirements*.lock ./
# Instruccion Docker RUN que configura la construccion o ejecucion de la imagen.
RUN pip install --no-cache-dir -r ${ARCHIVO_REQUISITOS}

# Instruccion Docker COPY que configura la construccion o ejecucion de la imagen.
COPY . .

# Instruccion Docker ENV que configura la construccion o ejecucion de la imagen.
ENV PUERTO=8078
# Instruccion Docker EXPOSE que configura la construccion o ejecucion de la imagen.
EXPOSE 8078

# Instruccion Docker CMD que configura la construccion o ejecucion de la imagen.
CMD ["python", "app.py"]
