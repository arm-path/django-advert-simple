from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


def get_photo_path(user_name, photo_name):
    return str(user_name) + '/' + str(photo_name)


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=35, blank=True, null=True)
    last_name = models.CharField(
        'Фамилие', max_length=41, blank=True, null=True)
    photo = models.ImageField('Фотография', upload_to='profile/',
                              default="profile/noavatar.png", blank=True, null=True)
    telephone_number = models.CharField(
        'Номер телефона', max_length=15, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})

    def get_udate_form_url(self):
        return reverse('profile_update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """Изменение пути сохранения фотографии"""
        if self.photo and not self.photo=="profile/noavatar.png":
            self.photo.name = get_photo_path(self.user, self.photo.name)
        super().save(**kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @receiver(post_save, sender=User)
    def create_profile_user(sender, instance, created, **kwargs):
        """Создает пустой профиль, при создании пользователя"""
        if created:
            Profile.objects.create(user=instance, pk=instance.pk)

    @receiver
    def save_profile_user(sender, instance, **kwargs):
        instance.profile.save()
