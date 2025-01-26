from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
	categories = (('Hobby', 'Hobby'), ('Fashion', 'Fashion'), ('Electronics', 'Electronics'), ('Home', 'Home'))
	
	name = models.CharField(max_length=64, unique=True)
	categorie = models.CharField(max_length=20, choices=categories)
	picture = models.URLField(blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	text = models.TextField(max_length=200, blank=True)
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	active = models.BooleanField()

	def __str__(self):
		return f"{self.name} with price {self.price}"

class Bid(models.Model):
	item = models.ForeignKey(Auction, on_delete=models.PROTECT)
	bid = models.DecimalField(max_digits=8, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

	def __str__(self):
		return f"{self.user} created bid {self.bid}"

class Comment(models.Model):
	item = models.ForeignKey(Auction, on_delete=models.PROTECT)
	text = models.CharField(max_length=200)
	user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

	def __str__(self):
		return f"{self.user} commented {self.text}"

class Watchlist(models.Model):
	item = models.ForeignKey(Auction, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

	def __str__(self):
		return f"{self.user} added {self.user} to the Watchlist"
