import factory
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.contrib.auth.models import Group
from identities.models import (
    Profile,
)


USER_PASSWORD = "pass"  # nosec


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"Group {n}")


@factory.django.mute_signals(signals.post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    affiliation = factory.Faker("company")


@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user_{n}")
    password = factory.PostGenerationMethodCall("set_password", USER_PASSWORD)
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    profile = factory.RelatedFactory(ProfileFactory, "user")

    class Params:
        basic = factory.Trait(
            username="user-basic",
            email="foo@bar.org",
            password=factory.PostGenerationMethodCall("set_password", USER_PASSWORD),
        )
        staff = factory.Trait(
            username="user-staff",
            is_staff=True,
            password=factory.PostGenerationMethodCall("set_password", USER_PASSWORD),
        )
