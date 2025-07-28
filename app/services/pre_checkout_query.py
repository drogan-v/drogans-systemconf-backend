import json

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import OrderInfo, PreCheckoutQuery
from telegram import User as TgUser

from app.db.models.item import Item
from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.user import User
from app.db.session import async_session_maker
from app.schemas.item import ItemsID


async def save_pre_checkout_query_info(pre_checkout_query: PreCheckoutQuery):
    async with async_session_maker() as session:
        try:
            async with session.begin():
                user = await _save_user(pre_checkout_query.from_user, session)
                order = await _save_users_order(
                    pre_checkout_query.order_info, user, session
                )
                invoice_payload = await _get_item(
                    ItemsID(**json.loads(pre_checkout_query.invoice_payload)), session
                )
                order_item = await _save_order_item(order, invoice_payload, session)
        except Exception as e:
            raise Exception("save_pre_checkout_query_info" + str(e))


async def _save_user(from_user: TgUser, session: AsyncSession) -> User:
    user = await session.get(User, from_user.id)
    if not user:
        user = User(
            user_id=from_user.id,
            first_name=from_user.first_name,
            last_name=from_user.last_name,
            username=from_user.username,
        )
        session.add(user)
        await session.flush()
    return user


async def _save_users_order(
    users_order: OrderInfo | None, user: User, session: AsyncSession
) -> Order:
    order = Order(user_id=user.user_id)
    session.add(order)
    await session.flush()
    return order


async def _get_item(invoice_payload: ItemsID, session: AsyncSession) -> Item:
    item = await session.get(Item, invoice_payload.item_id)
    if not item:
        raise Exception("No Item")
    return item


async def _save_order_item(
    order: Order, item: Item, session: AsyncSession
) -> OrderItem:
    order_item = OrderItem(
        order_id=order.order_id,
        item_id=item.item_id,
        order_item_quantity=1,
        order_item_price=item.item_price,
    )
    session.add(order_item)
    await session.flush()
    return order_item
