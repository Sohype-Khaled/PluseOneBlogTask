import factory
from faker import Faker

from profiles.tests.factories import UserFactory
from ..models import Post, Category, Tag, Comment

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "Category #%s" % n)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: "Tag #%s" % n)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: "Post #%s" % n)
    content = factory.Faker('paragraph')

    @factory.lazy_attribute
    def author(self):
        user = UserFactory()
        return user.profile

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.categories.add(*extracted)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.tags.add(*extracted)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    content = factory.Faker('paragraph')

    @factory.lazy_attribute
    def post(self):
        return PostFactory()

    @factory.lazy_attribute
    def author(self):
        return self.post.author
