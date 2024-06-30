from rest_framework import serializers

from profiles.serializers import AuthorField
from .models import Post, Category, Tag, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return CategorySerializer(value).data

    def to_internal_value(self, data):
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagField(serializers.RelatedField):
    def to_representation(self, value):
        return TagSerializer(value).data

    def to_internal_value(self, data):
        return data


class PostSerializer(serializers.ModelSerializer):
    categories = CategoryField(queryset=Category.objects.all(), many=True)
    tags = TagField(queryset=Tag.objects.all(), many=True)
    author = AuthorField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'categories', 'tags', 'created_at', 'updated_at')
        read_only_fields = ('author', 'created_at', 'updated_at')

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        tags = validated_data.pop('tags')
        validated_data['author'] = self.context['request'].user.profile

        instance = super().create(validated_data)

        instance.tags.set(tags)
        instance.categories.set(categories)

        return instance

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', [])
        tags = validated_data.pop('tags', [])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if categories:
            instance.categories.set(categories)

        if tags:
            instance.tags.set(tags)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'author', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)
