from ninja import NinjaAPI

from .module4 import router as router4

api = NinjaAPI(
    title='Django ORM Project',
    description = 'Enpoints for managing Products,Orders and Promotions',
    version='1.0.0',
)

api.add_router("mod4/",router4)