from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

##########################################################################################

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Comment(models.Model):
    # Linking the comment to the Post model with a many-to-one relationship
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    # The user who authored the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # The text content of the comment
    content = models.TextField()

    # Timestamp for when the comment was created
    created_at = models.DateTimeField(default=now)

    # Timestamp for when the comment was last updated
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the Comment object
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

