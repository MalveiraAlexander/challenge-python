# Usa una imagen oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos requeridos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Expone el puerto de Django
EXPOSE 8000

# Configura el comando predeterminado para el contenedor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]