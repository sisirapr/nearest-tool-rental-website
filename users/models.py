from django.db import models
from accounts.models import CustomUser
from home.models import Post
from PIL import Image 

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.first_name} Profile'
    # to resize image
    def save(self):
    	super().save()

    	img = Image.open(self.image.path)

    	if img.height > 300 or img.width > 300:
    		output_size = (300, 300)
    		img.thumbnail(output_size)
    		img.save(self.image.path)

class RequestTool(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='u_from')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='u_to')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, blank=True)
    status = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.post.tool

class ReplayTool(models.Model):
    from_u = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_u')
    to_u = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_u')
    reply_to = models.ForeignKey(RequestTool, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, blank=True)
    status = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.reply_to.post.tool

class Contract(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    period = models.DecimalField(decimal_places=2,max_digits=12)
    total_rent = models.DecimalField(decimal_places=2,max_digits=12)
    status = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.post.tool