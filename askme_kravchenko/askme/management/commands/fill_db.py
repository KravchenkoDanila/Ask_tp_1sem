from django.core.management.base import BaseCommand
from askme.models import AnswerLike, Profile, QuestionLike, User, Question, Answer, Tag
import random
from itertools import product


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
        parser.add_argument('--delete', action='store_true')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        delete_users = kwargs['delete']

        if delete_users:
            User.objects.filter(is_superuser=False).delete()
            Question.objects.all().delete()
            Tag.objects.all().delete()
            self.stdout.write('Данные удалены')
            return

        user_count = ratio
        question_count = ratio * 10
        answer_count = ratio * 100
        tag_count = ratio
        likes_count = ratio * 200

        self.stdout.write(f'Генерация {user_count} пользователей')
        self._create_users(user_count)

        self.stdout.write(f'Генерация {tag_count} тегов')
        tags = self._create_tags(tag_count)

        self.stdout.write(f'Генерация {question_count} вопросов')
        questions = self._create_questions(question_count, tags)

        self.stdout.write(f'Генерация {answer_count} ответов')
        answers = self._create_answers(answer_count, questions)

        self.stdout.write(f'Генерация {likes_count} оценок пользователей')
        self._create_likes(likes_count, questions, answers, user_count)

        self.stdout.write('✅ База данных успешно заполнена')


    def _create_users(self, count):
        for i in range(count):
            username = f'user{i}'
            email = f'{username}@mail.ru'
            User.objects.create_user(
                username=username,
                password='password',
                email=email
            )
            Profile.objects.create(user=User.objects.get(username=username))


    def _create_tags(self, count):
        tags = [Tag(name=f'tag_{i}') for i in range(count)]
        Tag.objects.bulk_create(tags)
        return list(Tag.objects.all())


    def _create_questions(self, count, tags):
        profiles = list(Profile.objects.all())
        questions = []
        for i in range(count):
            author = random.choice(profiles)
            title = f'Ребята, как выйти из Vim? N{i}'
            text = 'Etiam imperdiet dapibus urna, sed pharetra orci fringilla a. Etiam imperdiet dapibus urna, sed pharetra orci fringilla a. Integer porta lobortis felis, sed auctor tellus posuere at. Proin quam quam, consectetur facilisis velit nec, ultrices tincidunt eros. Pellentesque porttitor tristique nisi, non commodo lectus rhoncus nec. Nunc ac diam arcu. Duis posuere turpis et velit lobortis, consequat placerat magna ultricies. Cras facilisis, ante a congue molestie'
            questions.append(Question(author=author, title=title, text=text))

        batch_size = 10_000
        for i in range(0, len(questions), batch_size):
            Question.objects.bulk_create(questions[i:i + batch_size])

        all_questions = list(Question.objects.all())

        for q in all_questions:
            if tags:
                num_tags = min(random.randint(1, 3), len(tags))
                selected_tags = random.sample(tags, num_tags)
                q.tags.set(selected_tags)

        return all_questions


    def _create_answers(self, count, questions):
        profiles = list(Profile.objects.all())
        answers = []

        for i in range(count):
            author = random.choice(profiles)
            question = random.choice(questions)
            text = 'Лол попробуй выйти из дома, et interdum mauris lacinia. Etiam imperdiet dapibus urna, sed pharetra orci fringilla a. Integer porta lobortis felis, sed auctor tellus posuere at. Proin quam quam, consectetur facilisis velit nec, ultrices tincidunt eros. Pellentesque porttitor tristique nisi, non commodo lectus rhoncus nec. Nunc ac diam arcu. Duis posuere turpis et velit lobortis, consequat placerat magna ultricies. Cras facilisis, ante a congue molestie'
            answers.append(Answer(author=author, question=question, text=text))

        batch_size = 10_000
        for i in range(0, len(answers), batch_size):
            Answer.objects.bulk_create(answers[i:i + batch_size])

        return list(Answer.objects.all())


    def _create_likes(self, total_likes, questions, answers, user_count):
        profiles = list(Profile.objects.all())

        # Сгенерируем уникальные комбинации (user_id, object_id) заранее
        possible_question_ids = set(q.id for q in questions)
        possible_answer_ids = set(a.id for a in answers)

        half_questions = total_likes // 10 * 3
        half_answers = total_likes // 10 * 7

        question_pairs = random.sample(list(product(profiles, possible_question_ids)), k=min(half_questions, len(profiles) * len(possible_question_ids)))
        question_likes = [
            QuestionLike(user=p[0], question_id=p[1], value=random.choice([1, -1]))
            for p in question_pairs
        ]
        QuestionLike.objects.bulk_create(question_likes)

        answer_pairs = random.sample(list(product(profiles, possible_answer_ids)), k=min(half_answers, len(profiles) * len(possible_answer_ids)))
        answer_likes = [
            AnswerLike(user=p[0], answer_id=p[1], value=random.choice([1, -1]))
            for p in answer_pairs
        ]
        AnswerLike.objects.bulk_create(answer_likes)

        self.stdout.write(f'Добавлено {QuestionLike.objects.count()} лайков к вопросам')
        self.stdout.write(f'Добавлено {AnswerLike.objects.count()} лайков к ответам')