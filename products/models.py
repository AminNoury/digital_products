from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)
    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='products/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)
    class Meta:
        db_table = 'Product'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class File(models.Model):
    product = models.ForeignKey('Product', verbose_name=_('product'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=50)
    file = models.FileField(_('file'), upload_to='file/%Y/%m/%d/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)

    class Meta:
        db_table = 'file'
        verbose_name = 'File'
        verbose_name_plural = 'Files'





