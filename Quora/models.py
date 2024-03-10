from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce import models as tinymce_models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile (models.Model):
    user = models.OneToOneField(User, related_name="profile_user",on_delete=models.CASCADE)
    # main_info
    name = models.CharField(max_length=50, help_text="write your name")
    avatar = models.ImageField(upload_to='avatar',default='avatar/default profile.jpg', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    # employment info
    profession = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    start_year = models.DateField(null=True,blank=True, help_text="time you started working for the company ")
    end_year = models.DateField(null=True, blank=True,help_text="time you stopped working for the company ")
    # school info
    grad_year = models.DateField(null=True,blank=True)
    school = models.CharField(max_length=70, null=True, blank=True)
    degree_type = models.CharField(max_length=50, null=True, blank=True)
    # location of user
    location = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-profile'


class Question(models.Model):
    content = models.CharField(max_length=250,help_text="enter the question you want to ask")
    creator = models.ForeignKey(User, related_name="question_creator",on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=100,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    to = models.ManyToManyField(User, related_name="question_for")

    def __str__(self):
        return f'from {self.creator}'


class Image(models.Model):
    img_answer = models.ForeignKey("Answer",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="answer_images",null=True)

    def __str__(self):
        return f'image for {self.img_answer.content[0:14]} ... '


class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    responder = models.ForeignKey(User, related_name="responder_user",on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name="upvotes")
    downvotes = models.ManyToManyField(User, related_name="downvotes")
    images = models.ManyToManyField(Image)

    def upvote(self, user):
        if user not in self.upvotes.all():
            self.upvotes.add(user)
            self.downvotes.remove(user)

    def downvote(self, user):
        if user not in self.downvotes.all():
            self.downvotes.add(user)
            self.upvotes.remove(user)

    def __str__(self):
        return f'{self.content[0:14]} ... '


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name="followee", on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)


class msg_image(models.Model):
    img_message = models.ForeignKey("Message", on_delete=models.CASCADE)
    image = models.ImageField(null=True)


class Message(models.Model):
    sender = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="receiver",on_delete=models.CASCADE)
    content = models.TextField(help_text="write your message here ... ")
    date_created = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(msg_image)


class Space (models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    follow = models.ManyToManyField(User, related_name="space_follow")


class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
