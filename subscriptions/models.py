from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import validate_sku

from users.models import User


class Package(models.Model):
    title = models.CharField(_('title'), max_length=50)
    sku = models.CharField(_('stock keeping unit'), max_length=30, validators=[validate_sku], db_index=True)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='packages/')
    is_enable = models.BooleanField(_('is_enable'), default=True)
    price = models.PositiveIntegerField(_('price'))
    duration = models.DurationField(_('duration'), null=True, blank=True)
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now_add=True)

    class Meta:
        db_table = 'package'
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')

    def __str__(self):
        return self.title



class Subscription(models.Model):
    user = models.ForeignKey('users.User', related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey(Package, related_name='%(class)s', on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    expire_time = models.DateTimeField(_('expire time'), blank=True, null=True)

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

