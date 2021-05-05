from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    pass

class Listing(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='User')
    title = models.CharField(max_length=50)
    start_bit = models.IntegerField()
    description = models.TextField(max_length=200)
    picture_URL = models.URLField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    bids = models.ManyToManyField('Bid', related_name='bids_in_the_auction', blank=True)
    last_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='last_bid_for_the_listing', blank=True, null=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="new_owner", null=True, blank=True)

    CATEGORY_CHOICES = [
        ('Fasion', 'Fasion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Business','Business'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Fasion',
    )

    def __str__(self):
        return f"{self.title}"

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    class Meta:
        verbose_name_plural = "Listing"


class Watchlist(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   items = models.ManyToManyField(Listing)

   def __str__(self):
       return f"{self.user}+{self.items}"


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='0')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default='0')
    bid = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s' % (self.bid)
    
    class Meta:
        verbose_name_plural = "Bid"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='0')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default='0')
    comment = models.TextField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
     
    def __str__(self):
        return f"{self.comment}"

    class Meta:
        verbose_name_plural = "Comment"