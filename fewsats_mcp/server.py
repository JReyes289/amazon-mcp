# Contenido del archivo server.py proporcionado
from fastapi import FastAPI
from fewsats_mcp.amazon.client import Amazon # <-- MODIFICADO para usar la ruta del módulo local
import os
from typing import Dict, List, Optional


# Crear instancia de FastAPI
mcp = FastAPI(title="Fewsats MCP Server", description="Amazon MCP Tools API")

# Mock tool decorator for FastAPI compatibility
def tool():
    def decorator(func):
        return func
    return decorator


def get_amazon():
    """Obtiene o crea una instancia de Amazon."""
    return Amazon()


def handle_response(response):
    """Maneja las respuestas de los métodos de Amazon."""
    if hasattr(response, 'status_code'):
        try: return response.status_code, response.json()
        except: return response.status_code, response.text
    return response


@mcp.post("/amazon/search")
async def amazon_search(q: str, domain: str = "amazon.com") -> Dict:
    """Busca productos que coincidan con la consulta en Amazon."""
    response = get_amazon().search(query=q, domain=domain)
    return handle_response(response)


@mcp.post("/amazon/payment-offers")
async def amazon_get_payment_offers(product_url: str, shipping_address: Dict, user: Dict, asin: str = "", quantity: int = 1, protocol: str = "L402") -> Dict:
    """Obtiene las ofertas de pago para un producto."""
    if protocol == "X402":
        response = get_amazon().buy_now_with_x402(product_url=product_url, shipping_address=shipping_address, user=user, asin=asin, quantity=quantity)
    else:
        response = get_amazon().buy_now(product_url=product_url, shipping_address=shipping_address, user=user, asin=asin, quantity=quantity)
    return handle_response(response)


@mcp.post("/amazon/pay-x402")
async def pay_with_x402(x_payment: str, product_url: str, shipping_address: Dict, user: Dict, asin: str = "", quantity: int = 1) -> Dict:
    """Paga un producto con X402."""
    response = get_amazon().buy_now_with_x402(product_url=product_url, shipping_address=shipping_address, user=user, asin=asin, quantity=quantity, x_payment=x_payment)
    return handle_response(response)


@mcp.get("/orders/external/{external_id}")
async def get_order_by_external_id(external_id: str) -> Dict:
    """Obtiene el estado de un pedido específico."""
    response = get_amazon().get_order_by_external_id(external_id=external_id)
    return handle_response(response)

@mcp.get("/orders/payment-token/{payment_context_token}")
async def get_order_by_payment_token(payment_context_token: str) -> Dict:
    """Obtiene el estado de un pedido por el token de contexto de pago."""
    response = get_amazon().get_order_by_payment_token(payment_token=payment_context_token)
    return handle_response(response)


@mcp.get("/orders/user")
async def get_user_orders() -> List[Dict]:
    """Obtiene todos los pedidos del usuario actual."""
    response = get_amazon().get_user_orders()
    return handle_response(response)


def main():
    import uvicorn
    uvicorn.run(mcp, host="0.0.0.0", port=8000)
