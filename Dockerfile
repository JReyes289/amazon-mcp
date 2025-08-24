# 1. Usar una imagen base de Python oficial
FROM python:3.12-slim

# 2. Instalar uv, el gestor de paquetes
RUN pip install uv

# 3. Establecer el directorio de trabajo
WORKDIR /app

# 4. Copiar el archivo de dependencias e instalarlas
# Esto aprovecha el caché de capas de Docker
COPY pyproject.toml .
RUN uv pip install --system .

# 5. Copiar el código de la aplicación
COPY ./fewsats_mcp ./fewsats_mcp

# 6. Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# 7. Comando para ejecutar la aplicación usando Uvicorn
# Apunta a la instancia 'mcp' dentro del módulo 'server'
CMD ["uvicorn", "fewsats_mcp.server:mcp", "--host", "0.0.0.0", "--port", "8000"]
