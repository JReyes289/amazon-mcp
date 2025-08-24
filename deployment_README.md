# Servidor MCP de Fewsats para Amazon

Este proyecto contiene un servidor MCP (Meta-Communication Protocol) basado en FastAPI que expone la funcionalidad de compra de Amazon como un conjunto de herramientas para agentes de IA.

## Requisitos

- Docker
- Un archivo `.env` con una `FEWSATS_API_KEY` válida.

## Cómo Ejecutar

### 1. Configurar el Entorno
Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave de API:

```
FEWSATS_API_KEY="tu_clave_secreta_aqui"
```

### 2. Construir la Imagen de Docker
Desde el directorio raíz del proyecto, ejecuta el siguiente comando:

```bash
docker build -t fewsats-mcp-server .
```

### 3. Ejecutar el Contenedor de Docker
Una vez que la imagen esté construida, puedes iniciar el servidor con este comando:

```bash
docker run --rm -p 8000:8000 --env-file .env --name mcp-server fewsats-mcp-server
```

### 4. Acceder al Servicio
El servidor estará disponible en `http://localhost:8000`. Puedes ver la documentación de la API generada automáticamente en `http://localhost:8000/docs`.
