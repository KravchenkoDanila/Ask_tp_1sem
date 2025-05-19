from django.db import models

# Create your models here.

questions = []
for i in range(1, 30):
    questions.append({
        'title': 'title ' + str(i),
        'id': i,
        'text': 'text ' + str(i),
        'tag_name': 'tag' + str(i),
    })

#Массив всех тегов используется для прорисовки Popular tags
tags = []
for i in questions:
    tags.append({
        'tag_name': i['tag_name'],
    })
