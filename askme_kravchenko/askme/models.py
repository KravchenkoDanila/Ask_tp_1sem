from django.db import models

# Create your models here.

questions = []
for i in range(1, 21):
    questions.append({
        'title': 'title ' + str(i),
        'id': i,
        'text': 'text ' + str(i),
        'tag_name': 'tag' + str(i % 6),
    })


answers = []
for i in range(1, 10):
    answers.append({
        'title': 'answer title ' + str(i),
        'id': i,
        'text': 'answer text ' + str(i),
        'tag_name': 'tag' + str(i),
    })


tags = []
seen_tags = set()

for q in questions:
    tag_name = q['tag_name']
    if tag_name not in seen_tags:
        tags.append({'tag_name': tag_name})
        seen_tags.add(tag_name)
