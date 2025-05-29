
from django import forms

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from .models import Profile, Tag, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Login'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first() or \
               User.objects.filter(email=username).first()
        if not user:
            raise forms.ValidationError("No account found with this username or email.") #FIXIT
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first() or \
                   User.objects.filter(email=username).first()

            if user and not user.check_password(password):
                self.add_error('password', 'Incorrect password.')  #FIXIT
        return cleaned_data


class SignupForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Login'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )
    nickname = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='NickName'
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Avatar'
    )

    class Meta:
        model = User
        fields = ['username', 'email']  # username — это поле из модели User

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

            # Создаем или обновляем профиль
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = self.cleaned_data.get('nickname', '')
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()

        return user


class SettingsForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Login'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )
    nickname = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='NickName'
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Avatar'
    )

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and isinstance(user, User):
            self.user = user
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['nickname'].initial = user.profile.nickname
            self.fields['avatar'].initial = user.profile.avatar.url

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username

        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise ValidationError("This login is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email

        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Обновляем связанный аккаунт User
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.save()

        # Привязываем профиль к пользователю
        profile.user = self.user  # <-- ключевая строка

        if commit:
            profile.save()

        return profile


class AddQuestionForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a question title',
            'maxlength': 100,
        })
    )
    text = forms.CharField(
        label="Text",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your question',
            'rows': 5,
        })
    )
    tags = forms.CharField(
        label="Tags",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (for example: Apple, Tree)',
        }),
        required=False
    )

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Title cannot be empty.")
        if Question.objects.filter(title=title).exists():
            raise ValidationError("This title is already taken.")
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise ValidationError("Text is required.")
        return text

    def save(self, commit=True, author=None):
        question = super().save(commit=False)
        if author and isinstance(author, Profile):  # <-- Проверяем тип
            question.author = author
        if commit:
            question.save()
            self._save_tags(question)  # Выносим логику тегов отдельно
        return question

    def _save_tags(self, question):
        tags_input = self.cleaned_data.get('tags', '')
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)  # <-- Так правильно добавлять теги


class AddAnswerForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your answer here..',
            'rows': 2,
        }),
        required=False
    )

    class Meta:
        model = Answer
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            self.add_error('text', 'Answer cannot be empty.')
        return text

    def save(self, commit=True, author=None, question=None):
        answer = super().save(commit=False)
        if author:
            answer.author = author
        if question:
            answer.question = question
        if commit:
            answer.save()
        return answer