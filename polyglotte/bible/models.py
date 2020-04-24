from django.urls import reverse
from django.db import models


class Verse(models.Model):
    book = models.CharField(max_length=10)
    chapter = models.IntegerField()
    verse = models.IntegerField()
    txt_hebrew = models.TextField(blank=True, null=True)
    txt_greek = models.TextField(blank=True, null=True)
    txt_latin = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Verse'

    def get_absolute_url(self):
        return reverse('bible:update', kwargs={'book': self.book, 'chapter': self.chapter, 'verse': self.verse})
