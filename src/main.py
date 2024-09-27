from fastapi import FastAPI

from src.Orders.router import router as router_orders
from src.Products.router import router as router_products
app = FastAPI()

app.include_router(router_orders)
app.include_router(router_products)