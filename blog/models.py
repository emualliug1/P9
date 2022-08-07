from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from PIL import Image


class Ticket(models.Model):

    IMAGE_MAX_SIZE = (300, 300)

    title = models.CharField(max_length=128)

    description = models.TextField(max_length=2048,
                                   blank=True)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    image = models.ImageField(null=True,
                              blank=True)

    time_created = models.DateTimeField(auto_now_add=True)

    has_review = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):

    ticket = models.ForeignKey(to=Ticket,
                               on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],
                                              verbose_name="Note",)
    headline = models.CharField(max_length=128)

    body = models.TextField(max_length=8192,
                            blank=True)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline


class UserFollows(models.Model):
    user = models.ForeignKey(null=True,
                             to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')

    followed_user = models.ForeignKey(null=True,
                                      to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user',)
