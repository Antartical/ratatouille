from faker import Faker
from ratatouille.models import user


fake = Faker(locale='es-ES')


async def user_factory() -> user.User:
    """User factory"""
    return await user.User.create(
        email=fake.email(),
        name=fake.name(),
        surname='',
        birthday=fake.date(),
        phone=fake.phone_number()
    )
