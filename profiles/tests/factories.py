import factory
from django.contrib.auth import get_user_model

from ..models import Profile

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'secret')

    @factory.lazy_attribute
    def username(self):
        # Generate unique username from first name and last name
        username_base = (self.first_name + self.last_name).lower()
        username = username_base
        num_suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{username_base}{num_suffix}"
            num_suffix += 1
        return username


