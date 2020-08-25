from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from gallery_app.models import Gallery


class Advert(models.Model):
    """Модель объявлений"""
    title = models.CharField('Заголовок объявления', max_length=35)
    slug = models.SlugField('URL объявления', max_length=41, unique=True)
    text = models.TextField('Текст объявления', null=True)
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея', on_delete=models.CASCADE, null=True, blank=True)
    telephone_number = models.CharField('Номер телефона', max_length=15, blank=True)
    email = models.EmailField('Электронный адрес', max_length=41)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField('Опубликовано', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('advert_detail', kwargs={'slug': self.slug})

    def get_update_form_url(self):
        return reverse('advert_update', kwargs={'slug': self.slug})

    def get_delete_form_url(self):
        return reverse('advert_delete', kwargs={'slug': self.slug})

    class Meta:
        """Представление модели в административной панели"""
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-date']
