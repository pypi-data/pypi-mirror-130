from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import io
from django.core.files.storage import default_storage as storage

# Create your models here.


def get_sentinal_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Group(models.Model):
    group_name = models.SlugField(max_length=20)
    creater = models.ForeignKey(User, on_delete=models.SET(get_sentinal_user))
    group_info = models.CharField(max_length=300, blank=True, null=True)
    members = models.ManyToManyField(User, related_name="all_groups")
    # last_opened = models.DateTimeField()

    def __str__(self):
        return self.group_name

    def last_10_messages(grp_name, times=0):
        group = Group.objects.get(group_name=grp_name)
        if not times:
            return list(group.messages.order_by("date_posted"))[-30:]
        return list(group.messages.order_by("date_posted"))[(-30*(times+1)):(-30*times)]

class Messages(models.Model):
    parent_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="messages"
    )
    parent_user = models.ForeignKey(User, on_delete=models.SET(get_sentinal_user))
    message_text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.localtime().now)

    def __str__(self):
        tup = tuple([self.parent_user, self.parent_group, self.message_text])
        return str(tup)

    def get_absolute_url(self):
        return reverse("group", kwargs={"grp_name": self.parent_group})


# To store user profile images dynamically
def get_image_path(instance, filename):
    from os.path import join

    return join("profile_pics", instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_info = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField( upload_to=get_image_path)

    def __str__(self):
        return self.user.username



def get_group_image_path(instance, filename):
    from os.path import join

    return join("group_profile_pics", instance.group.group_name, filename)


class GroupProfile(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name="group_profile"
    )
    image = models.ImageField(
         upload_to=get_group_image_path
    )

    def __str__(self):
        return self.group.group_name

  