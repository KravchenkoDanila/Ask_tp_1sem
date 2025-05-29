from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum


class QuestionManager(models.Manager):
    def with_like_sum(self):
        return self.annotate(like_sum=Sum('question_likes__value'))

    def best(self):
        return self.with_like_sum().order_by('-like_sum')

    def new(self):
        return self.with_like_sum().order_by('-created_at')


class TagManager(models.Manager):
    def popular(self):
        return self.order_by('-usage_count')[:10]


class AnswerManager(models.Manager):
    def for_question(self, question_id):
        return self.filter(question_id=question_id).annotate(
            like_sum=Sum('answer_likes__value')
        ).order_by('-like_sum')


class ProfileManager(models.Manager):
    def top(self):
        return self.annotate(
            question_count=Count('questions')
        ).order_by('-question_count')[:10]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatads/', null=True, blank=True, default='avatars/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username




class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='questions')
    title = models.CharField(max_length=255)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='answers')
    text = models.TextField()
    likes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    objects = AnswerManager()

    def __str__(self):
        return f"Ответ на '{self.question.title}'"


class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes')
    value = models.SmallIntegerField(choices=[
        (1, 'Like'),
        (-1, 'Dislike')
    ])

    class Meta:
        unique_together = ('user', 'question')


class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes')
    value = models.SmallIntegerField(choices=[
        (1, 'Like'),
        (-1, 'Dislike')
    ])

    class Meta:
        unique_together = ('user', 'answer')


