from django.utils.text import slugify
from factory import LazyAttribute, SubFactory, faker, post_generation
from factory.django import DjangoModelFactory as BaseFactory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal, FuzzyInteger
from rest_framework.authtoken.models import Token

from gelivery.core.models.order import OrderStatus


class RestaurantFactory(BaseFactory):
    class Meta:
        model = 'core.Restaurant'

    name = faker.Faker('name')
    address = faker.Faker('street_name')
    city = faker.Faker('city')


class UserFactory(BaseFactory):
    class Meta:
        model = 'accounts.User'

    username = faker.Faker('user_name')
    first_name = faker.Faker('first_name')
    last_name = faker.Faker('last_name')

    @post_generation
    def post(self, *args, **kwargs):
        Token.objects.get_or_create(user=self)


class CustomerFactory(BaseFactory):
    class Meta:
        model = 'core.Customer'

    user = SubFactory('gelivery.core.factories.UserFactory')
    address = faker.Faker('address')


class FoodCategoryFactory(BaseFactory):
    class Meta:
        model = 'core.FoodCategory'

    name = faker.Faker('name')
    slug = LazyAttribute(lambda f: slugify(f.name))
    description = faker.Faker('text')


class FoodFactory(BaseFactory):
    class Meta:
        model = 'core.Food'

    name = faker.Faker('name')
    category = SubFactory('gelivery.core.factories.FoodCategoryFactory')


class OrderFactory(BaseFactory):
    class Meta:
        model = 'core.Order'

    customer = SubFactory('gelivery.core.factories.CustomerFactory')
    restaurant = SubFactory('gelivery.core.factories.RestaurantFactory')
    status = FuzzyChoice(choices=[c[0] for c in OrderStatus.choices])
    address = faker.Faker('street_name')


class OrderItemFactory(BaseFactory):
    class Meta:
        model = 'core.OrderItem'

    order = SubFactory('gelivery.core.factories.OrderFactory')
    food = SubFactory('gelivery.core.factories.FoodFactory')
    quantity = FuzzyInteger(100)
    amount = FuzzyDecimal(0.1)
