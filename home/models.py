from django.db import models
from accounts.models import CustomUser
from django.urls import reverse

RENT_CHOICES = [
	('Per Hour', 'Per Hour'),
	('Per Day', 'Per Day'),
	('Per Week', 'Per Week'),
	('Per Month', 'Per Month'),
	('Per Year', 'Per Year'),
]

class Post(models.Model):
	tool = models.CharField(max_length=100)
	content = models.CharField(max_length=300)
	rent = models.DecimalField(decimal_places=2,max_digits=12)
	rent_type = models.CharField(max_length=100,choices=RENT_CHOICES,default=RENT_CHOICES[0][0])
	rating = models.FloatField(default=0)
	owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='tool_pics')
	available = models.BooleanField(default=False)

	def __str__(self):
		return self.tool

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})

RATE_CHOICES = [
	(1, '1 - Trash'),
	(2, '2 - Bad'),
	(3, '3 - Ok'),
	(4, '4 - Good'),
	(5, '5 - Great'),
]

class Review(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField(max_length=3000, blank=True)
	rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

	def __str__(self):
		return self.user.email