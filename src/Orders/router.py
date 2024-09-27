from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.Orders.models import Orders, OrdersItems
from src.Orders.schemas import OrdersUpdate, OrdersResponseGet, OrdersCreate, OrdersWithItems
from src.Products.models import Products
from src.database import get_async_session

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.get('/', response_model=OrdersResponseGet)
async def get_all_orders(page: int = 1, session: AsyncSession = Depends(get_async_session)):
    skip = (page - 1) * 10
    limit = 10
    query = (
        select(Orders, OrdersItems.id_products, OrdersItems.count)
        .join(OrdersItems, OrdersItems.id_orders == Orders.id)
        .offset(skip)
        .limit(limit)
        .order_by(Orders.id)
    )
    result = await session.execute(query)
    orders_with_items = result.all()

    return {'status': 'success',
            'data': [OrdersWithItems(id=order.id,
                      status= order.status,
                      create_at= order.create_at,
                      id_product= id_product,
                      count= count
                      ) for order, id_product, count in orders_with_items]}

@router.get('/{total_id}', response_model=OrdersResponseGet)
async def get_orders_on_id(total_id: int, session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Orders, OrdersItems.id_products, OrdersItems.count)
        .join(OrdersItems, OrdersItems.id_orders == Orders.id)
        .where(Orders.id == total_id)
    )
    result = await session.execute(query)
    orders_with_items = result.all()
    if not orders_with_items:
        raise HTTPException(status_code=404, detail={'status': 'error', 'data': 'Order not found'})
    return {'status': 'success', 'data': [OrdersWithItems(id=order.id,
                      status= order.status,
                      create_at= order.create_at,
                      id_product= id_product,
                      count= count
                      ) for order, id_product, count in orders_with_items]}



@router.post('/')
async def create_orders(new_order: OrdersCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt1 = insert(Orders).values(**{'status': 'in_progress'}).returning(Orders.id)   # из первого запроса
        result = await session.execute(stmt1)                                             # получаем новый Order.id
        total_order_id = result.scalars().one()

        stmt2 = insert(OrdersItems).values(id_orders=total_order_id, **new_order.__dict__
                                          ).returning(OrdersItems.id_products, OrdersItems.count)
        result = await session.execute(stmt2)                               # из второго запроса извлекаем
        total_products_id, count = result.fetchall()[0]                     # id и count продукта для заказа

        query = select(Products.amount).where(Products.id==total_products_id)
        result = await session.execute(query)                               # получаем количество продуктов на складе
        total_amount = result.scalar_one_or_none()

        if total_amount is None or total_amount < count:                    # проверяем хватит ли товара и есть ли он на складе
            raise HTTPException(status_code=400, detail={'status': 'error', 'data': 'Insufficient stock'})


        stmt3 = update(Products).where(Products.id==total_products_id).values(amount=total_amount-count)
        await session.execute(stmt3)                                         # вычитаем со склада необходимое количество

        await session.commit()
        return {'status': 'success',
                'data': f'order placed'}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={'status': 'error',
                    'data': f'error creating new_order'}
        )



@router.patch('/{total_id}/status')
async def update_orders(total_id: int, new_order: OrdersUpdate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(Orders).where(Orders.id==total_id).values(status=new_order.status)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success',
                'data': new_order.status}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={'status': 'error',
                    'data': 'error updating status order'}
        )
