from django.contrib.auth.models import User #юзаем стандартную модель User
from django.core.urlresolvers import reverse
from django.db import models

#класс петиций
#verbose_name юзаем для отображения нормального названия
class Petition(models.Model):
    title = models.CharField(verbose_name='Title of this petition', max_length=200, unique = True)
    slug_name = models.SlugField(verbose_name = 'Petition\'s slug name', unique = True, null = True, max_length = 200)
    text = models.TextField(verbose_name='Text of this petition')
    creator = models.ForeignKey(User, verbose_name='The creator of this petition')
    datetime_created = models.DateTimeField(verbose_name='Date and Time when this petition was created', auto_now_add = True)

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('petition-details', args = [self.slug_name])

class PetitionSignature(models.Model):
    petition = models.ForeignKey(Petition, verbose_name='The associated petition')
    signator = models.ForeignKey(User, verbose_name='The user who signed the petition')
    datetime_signed = models.DateTimeField(verbose_name='Date and time when this user signed this petition', auto_now_add = True)
    comment = models.TextField(verbose_name='Comments made by signator', blank = True)

    def __unicode__(self):
        return '%s signed by %s on %s' % (self.petition, self.signator, str(self.datetime_signed))

    class Meta:
        unique_together = ('petition', 'signator')
        ordering = ['datetime_signed']