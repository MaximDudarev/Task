from fastapi import HTTPException


from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.Products.models import Products
from src.Products.schemas import ProductsResponseGet, CreateProducts
from src.database import get_async_session

router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/', response_model=ProductsResponseGet)
async def get_all_products(session: AsyncSession = Depends(get_async_session)):

    query = select(Products).order_by(Products.id)
    result = await session.execute(query)
    products = result.scalars().all()
    return {
        'status': 'success',
        'data': [product.__dict__ for product in products]
    }

@router.get('/{total_id}', response_model=ProductsResponseGet)
async def get_product_on_id(total_id: int, session: AsyncSession = Depends(get_async_session)):

    query = select(Products).where(Products.id==total_id)
    result = await session.execute(query)
    return {
        'status': 'success',
        'data': result.scalars().all()
    }


@router.post('/')
async def create_product(new_products: CreateProducts, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Products).values(**new_products.__dict__)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success',
                'data': new_products.__dict__}
    except:
        raise HTTPException(
            status_code=500,
            detail={'status': 'error',
                    'data': 'Unable to create item'})

@router.put('/{total_id}')
async def update_product(total_id: int, new_products: CreateProducts, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(Products).where(Products.id==total_id).values(**new_products.__dict__)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success',
                'data': new_products.__dict__}
    except:
        raise HTTPException(
            status_code=500,
            detail={'status': 'error',
                    'data': 'Unable to update item'}
        )

@router.delete('/{total_id}')
async def delete_product(total_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(Products).where(Products.id==total_id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success',
                'data': None}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={'status': 'error',
                    'data': 'Unable to delete item'}
        )