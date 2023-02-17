# Imagen base
FROM python:3.9

# Configuración de variables de entorno
ENV FLASK_APP=rutas.py
ENV FLASK_RUN_HOST=0.0.0.0

# Configuración de la carpeta de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY requirements.txt .
COPY app.py .
COPY models.py .
COPY rutas.py .
COPY views.py .

# Instalar dependencias
RUN pip install -r requirements.txt

# Exponer el puerto 5000
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["flask", "run"]

