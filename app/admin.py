from sqladmin import ModelView

from app.db.models.user import User
from app.db.models.item import Item
from app.db.models.order import Order
from app.db.models.order_item import OrderItem

class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.first_name, User.last_name, User.username]

class ItemAdmin(ModelView, model=Item):
    column_list = [Item.item_id, Item.item_name, Item.item_price, Item.item_description]

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.order_id, Order.user_id, Order.created_at]

class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [
        OrderItem.order_item_id, OrderItem.order_id, OrderItem.item_id,
        OrderItem.order_item_quantity, OrderItem.order_item_price,я
    ]