from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class Profile(models.Model):
    def get_upload_to(self, filename):
        return f'users/{self.user_id}/{filename}'

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile', verbose_name=_("User"))
    bio = models.TextField(_("Bio"), default=None, null=True, blank=True)
    profile_picture = models.FileField(_("Profile Picture"), upload_to=get_upload_to, default=None, null=True,
                                       blank=True)

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=UserModel)
def create_profile_for_each_user(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
