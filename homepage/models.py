from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
import base64

BLACK = 'BK'
BEIGE = 'BG'
BLUE = 'BL'
IVORY = 'IV'
PINK = 'PK'
RED = 'RD'
WHITE = 'WT'
COLOR_CHOICES = (
    (BLACK, 'Black'),
    (BEIGE, 'Beige'),
    (BLUE, 'Blue'),
    (IVORY, 'Ivory'),
    (PINK, 'Pink'),
    (RED, 'Red'),
    (WHITE, 'White'),
)

MAJOR = 'MJ'
CLUB = 'CL'
USER = 'UR'
GROUP_TYPE = (
    (MAJOR, 'Major'),
    (CLUB, 'Club'),
    (USER, 'User'),
)

class Group(models.Model):
    group_type = models.CharField(
        max_length=2,
        choices=GROUP_TYPE,
        default=MAJOR,
    )
    group_name = models.CharField(max_length=50)
    users = models.ManyToManyField('auth.User')
    master = models.ManyToManyField('auth.User', related_name="master")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name

class Design(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    who = models.ManyToManyField('auth.User', related_name="who")
    detail_body = models.CharField(
        max_length=2,
        choices=COLOR_CHOICES,
        default=BLACK,
    )
    detail_sleeve = models.CharField(
        max_length=2,
        choices=COLOR_CHOICES,
        default=WHITE,
    )

    def __str__(self):
        return str(self.group)+'_'+str(self.owner)+"_"+str(self.id)

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE,primary_key=True)
    user_group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='user_group',
        null=True,
    )
    groups = models.ManyToManyField('Group')
    recent = models.OneToOneField(
        Design,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.user)

## 클래스 밖에 정의된 함수입니다 
# def create_profile(sender, instance, created, **kwargs):
#     #create Profile for every new User model
#     if created:
#         Profile.objects.create(user=instance)
# signals.post_save.connect(create_profile, sender='auth.User', weak=False)
##, dispatch_uid='models.create_profile'

def create_profile_and_group(sender, instance, created, **kwargs):
    #create User Group for every new User model
    if created:
        group = Group()
        group.group_type = USER
        group.group_name = 'user_group_'+instance.username
        group.save()
        group.master.add(instance)
        group.users.add(instance)

        profile = Profile()
        profile.user=instance
        profile.user_group=group
        profile.save()
        profile.groups.add(group)
        
signals.post_save.connect(create_profile_and_group, sender='auth.User', weak=False)
