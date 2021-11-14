admin:admin

customer.user:gelivery

gelivery.delivery: gelivery123



Müşteri 1 adresi Konak / İzmir

from gelivery.core.models import *
from gelivery.accounts.models import User
from rest_framework.authtoken.models import Token

restaurant_1 = Restaurant.objects.create(
    name="Kebapçı Dükkanı",
    address="Kebapçı Dükkanı Adresi",
    city="İzmir"
)

restaurant_2 = Restaurant.objects.create(
    name="Pilavcı",
    address="Pilavcı Adresi",
    city="Ankara"
)

category_1 = FoodCategory.objects.create(
    name="Ev Yemekleri",
    slug="ev-yemekleri",
    description="Ev yemekleri çeşitleri"
)

category_2 = FoodCategory.objects.create(
    name="Fast Food",
    slug="fast-food",
    description="Fast Food çeşitleri"
)

food_1 = Food.objects.create(
    category=category_1,
    name="Pilav",
)

food_2 = Food.objects.create(
    category=category_2,
    name="Hamburger",
)

food_3 = Food.objects.create(
    category=category_2,
    name="Vegan Pizza",
)

food_4 = Food.objects.create(
    category=category_1,
    name="Kuru Fasulye",
)


user_1 = User.objects.create(
    username="customer.user",
    email="user1@gelivery.local",
    first_name="Customer",
    last_name="User1"
)
user_1.set_password("gelivery")
Token.objects.get_or_create(user=user_1)

user_2 = User.objects.create(
    username="customer.user.2",
    email="user2@gelivery.local",
    first_name="Customer",
    last_name="User2"
)
user_2.set_password("gelivery")
Token.objects.get_or_create(user=user_2)


customer_1 = Customer.objects.create(user=user_1, address="Müşteri 1 Adresi")
customer_2 = Customer.objects.create(user=user_2, address="Müşteri 2 Adresi")


order_1 = Order.objects.create
