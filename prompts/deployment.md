### **Prompt para Agente de Codificación AI: Desplegar el Servidor MCP de Fewsats-Amazon como un Servicio FastAPI Independiente**

**Objetivo:**
Tu tarea es empaquetar y configurar el código fuente del servidor MCP (proporcionado en `server.py`) como una **aplicación FastAPI independiente y desplegable**. El objetivo es crear un servicio autocontenido que pueda ser construido y ejecutado usando Docker, exponiendo los `tools` de Amazon a través de una API. No implementarás nueva lógica de negocio; esta tarea se enfoca estrictamente en la estructuración, configuración y empaquetado para el despliegue.

**Contexto y Reglas:**
*   **Contexto Primario:** La lógica del servidor está definida en `server.py`, que utiliza `FastMCP` para exponer funciones como herramientas de IA.
*   **Arquitectura:** El resultado final será un servicio web basado en FastAPI, containerizado con Docker. La configuración, como las claves de API, debe gestionarse a través de variables de entorno.
*   **Estándares de Codificación:** Sigue las mejores prácticas para aplicaciones FastAPI y la creación de Dockerfiles.

---

### **Instrucciones Paso a Paso:**

**1. Crear la Estructura de Directorios Raíz:**
Crea la siguiente estructura de directorios y archivos. Todo el código de la aplicación vivirá dentro del directorio `fewsats_mcp/`.

*   `fewsats_mcp/`
*   `tests/`
*   `.dockerignore`
*   `.env`
*   `Dockerfile`
*   `pyproject.toml`
*   `README.md`

**2. Configurar el `pyproject.toml`:**
Este archivo gestionará todas las dependencias del proyecto. Asumiremos que `fastmcp` es un paquete que se instala junto con `amazon-client`, o que `amazon-client` es un paquete local.

`pyproject.toml`:
```toml
[project]
name = "fewsats-mcp-server"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "python-dotenv",
    "fastmcp", # Dependencia principal del servidor
]

[project.scripts]
# Permite ejecutar el servidor con un comando simple
run-server = "fewsats_mcp:main"

[tool.uv]
dev-dependencies = [
    "ruff",
    "pytest",
    "httpx",
]
```

**3. Crear la Estructura de la Aplicación Modular dentro de `fewsats_mcp/`:**
Esta estructura organiza el código fuente del servidor.

```
fewsats_mcp/
├── __init__.py
├── server.py
└── amazon/
    ├── __init__.py
    └── client.py  # <-- Placeholder para el cliente de Amazon
```
**Acción:** Crea todas las carpetas y archivos como se muestra.

**4. Poblar los Archivos de Código Fuente:**
Mueve el código proporcionado a los archivos correspondientes y crea los placeholders necesarios.

`fewsats_mcp/__init__.py`:
```python
# Contenido del archivo __init__.py proporcionado
from . import server
import asyncio

def main():
    """Punto de entrada principal para el paquete."""
    print("Iniciando el servidor MCP de Fewsats...")
    # FastMCP's run() es bloqueante, así que no se necesita asyncio.run aquí.
    # Uvicorn lo gestionará cuando se ejecute a través de Docker.
    server.mcp.run()

# Opcionalmente, exponer otros elementos importantes a nivel de paquete
__all__ = ['main', 'server']
```

`fewsats_mcp/server.py`:
```python
# Contenido del archivo server.py proporcionado
from mcp.server.fastmcp import FastMCP
from fewsats_mcp.amazon.client import Amazon # <-- MODIFICADO para usar la ruta del módulo local
import os
from typing import Dict, List, Optional


# Crear instancia de FastMCP
mcp = FastMCP("Fewsats MCP Server")


def get_amazon():
    """Obtiene o crea una instancia de Amazon."""
    return Amazon()


def handle_response(response):
    """Maneja las respuestas de los métodos de Amazon."""
    if hasattr(response, 'status_code'):
        try: return response.status_code, response.json()
        except: return response.status_code, response.text
    return response


@mcp.tool()
async def amazon_search(q: str, domain: str = "amazon.com") -> Dict:
    """Busca productos que coincidan con la consulta en Amazon."""
    response = get_amazon().search(query=q, domain=domain)
    return handle_response(response)


@mcp.tool()
async def amazon_get_payment_offers(product_url: str, shipping_address: Dict, user: Dict, asin: str = "", quantity: int = 1, protocol: str = "L402") -> Dict:
    """Obtiene las ofertas de pago para un producto."""
    if protocol == "X402":
        response = get_amazon().buy_now_with_x402(product_url=product_url, shipping_address=shipping_address, user=user, asin=asin, quantity=quantity)
    else:
        response = get_amazon().buy_now(product_url=product_url, shipping_address=shipping_address, user=user, asin=asin, quantity=quantity)
    return handle_response(response)


@mcp.tool()
async def pay_with_x402(x_payment: str, product_url: str, shipping_address: Dict, user: Dict, asin: str = "", quantity: int = 1) -> Dict:
    """Paga un producto con X402."""
    response = get_amazon().buy_now_with_x402(product_url=product_url, shipping_address=shipping_address, user=user, asin=asin, quantity=quantity, x_payment=x_payment)
    return handle_response(response)


@mcp.tool()
async def get_order_by_external_id(external_id: str) -> Dict:
    """Obtiene el estado de un pedido específico."""
    response = get_amazon().get_order_by_external_id(external_id=external_id)
    return handle_response(response)

@mcp.tool()
async def get_order_by_payment_token(payment_context_token: str) -> Dict:
    """Obtiene el estado de un pedido por el token de contexto de pago."""
    response = get_amazon().get_order_by_payment_token(payment_token=payment_context_token)
    return handle_response(response)


@mcp.tool()
async def get_user_orders() -> List[Dict]:
    """Obtiene todos los pedidos del usuario actual."""
    response = get_amazon().get_user_orders()
    return handle_response(response)


def main():
    mcp.run()

```

`fewsats_mcp/amazon/client.py` (Placeholder):
```python
# Placeholder para el cliente de la API de Amazon.
# La lógica de negocio para interactuar con Amazon iría aquí.

class Amazon:
    def __init__(self):
        print("Amazon client initialized.")
        # La inicialización, como cargar claves de API, iría aquí.
        pass

    def search(self, query: str, domain: str):
        print(f"Buscando '{query}' en '{domain}'...")
        return {"status": "ok", "results": [{"name": "Placeholder Product", "price": "$10"}]}

    def buy_now(self, product_url: str, shipping_address: dict, user: dict, asin: str, quantity: int):
        print(f"Iniciando compra para {product_url} con L402...")
        return {"status_code": 402, "detail": "Payment Required", "offer": "L402_TOKEN_HERE"}
    
    def buy_now_with_x402(self, product_url: str, shipping_address: dict, user: dict, asin: str, quantity: int, x_payment: str = None):
        if x_payment:
            print(f"Procesando pago X402 para {product_url}...")
            return {"status": "ok", "order_id": "123-abc"}
        else:
            print(f"Iniciando compra para {product_url} con X402...")
            return {"status_code": 402, "detail": "Payment Required", "offer": "X402_OFFER_HERE"}

    def get_order_by_external_id(self, external_id: str):
        return {"status": "ok", "order_id": external_id, "details": "shipped"}
        
    def get_order_by_payment_token(self, payment_token: str):
        return {"status": "ok", "order_id": "123-xyz", "details": "processing"}

    def get_user_orders(self):
        return [{"order_id": "123-abc", "details": "shipped"}]
```

**5. Crear la Configuración de Despliegue (Docker y Entorno):**

`Dockerfile`:
```Dockerfile
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
```

`.env` (Archivo de variables de entorno):
```
# Clave de API requerida por el cliente de Amazon/Fewsats
# Reemplaza 'TU_CLAVE_DE_API' con una clave real para el despliegue
FEWSATS_API_KEY="TU_CLAVE_DE_API"
```

`.dockerignore`:
```
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.ruff_cache/
.env
```

**6. Crear un `README.md` para el Despliegue:**
Este archivo explicará cómo construir y ejecutar el servicio.

`README.md`:
```markdown
# Servidor MCP de Fewsats para Amazon

Este proyecto contiene un servidor MCP (Meta-Communication Protocol) basado en FastAPI que expone la funcionalidad de compra de Amazon como un conjunto de herramientas para agentes de IA.

## Requisitos

- Docker
- Un archivo `.env` con una `FEWSATS_API_KEY` válida.

## Cómo Ejecutar

### 1. Configurar el Entorno
Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave de API:

```FEWSATS_API_KEY="tu_clave_secreta_aqui"
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
```

---
**Resumen del Resultado Final Esperado:**
Un proyecto completamente funcional y autocontenido que define el servidor MCP de Fewsats-Amazon. El proyecto incluye todo lo necesario para ser construido como una imagen de Docker y ejecutado como un contenedor, leyendo la configuración sensible desde un archivo `.env`. El resultado es un servicio robusto y desplegable, listo para ser consumido por un agente de IA.