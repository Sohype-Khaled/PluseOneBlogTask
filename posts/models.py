from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('id',)

    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"))

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ('id',)

    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"))

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('created_at',)

    title = models.CharField(_("Title"), max_length=255)
    content = models.TextField(_("Content"))
    author = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE, related_name='posts',
                               verbose_name=_("Author"))
    categories = models.ManyToManyField(Category, related_name="posts", verbose_name=_("Categories"))
    tags = models.ManyToManyField(Tag, related_name="posts", verbose_name=_("Tags"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ('created_at',)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Post"))
    author = models.ForeignKey("profiles.Profile",
                               on_delete=models.CASCADE, related_name='comments', verbose_name=_("Author"))
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return self.content
