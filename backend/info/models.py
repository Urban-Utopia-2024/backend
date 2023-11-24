from django.core.validators import MaxValueValidator
from django.db import models

from urban_utopia_2024.app_data import (
    APPEAL_RATING_MAX_VAL, APPEAL_RATING_MESSAGE,
    APPEAL_STATUS_CHOICES, APPEAL_STAGE_INITIAL, APPEAL_STATUS_MAX_LEN,
    APPEAL_TEXT_MAX_LEN, APPEAL_TOPIC_MAX_LEN,
    NEWS_CATEGORY_CHOICES, NEWS_CATEGORY_MAX_LEN,
    NEWS_COMMENT_MAX_LEN, NEWS_COMMENT_SLICE,
    NEWS_PICTURES_PATH, NEWS_TEXT_MAX_LEN,
    TASK_TITLE_MAX_LEN,
    QUIZ_ANSWER_MAX_LEN, QUIZ_ANSWER_SLICE, QUIZ_TITLE_MAX_LEN,
)
from user.models import Address, User


class Task(models.Model):
    """Модель плановых работ."""

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=TASK_TITLE_MAX_LEN,
    )
    municipal = models.ForeignKey(
        verbose_name='Муниципальная служба',
        to=User,
        related_name='task',
        on_delete=models.PROTECT,
    )
    address = models.ForeignKey(
        verbose_name='Адрес',
        to=Address,
        related_name='tasks',
        on_delete=models.PROTECT,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True,
    )
    start_date = models.DateTimeField(
        verbose_name='Дата и время начала работ',
    )
    end_date = models.DateTimeField(
        verbose_name='Дата и время окончания работ',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'municipal'),
                name='unique_municipal_task',
            ),
        )
        ordering = ('id',)
        verbose_name = 'Плановая работа'
        verbose_name_plural = 'Плановые работы'

    def __str__(self):
        return f'{self.title} ({self.municipal.municipal_name})'


class Quiz(models.Model):
    """Модель опросов."""

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=QUIZ_TITLE_MAX_LEN,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title


class Answer(models.Model):
    """Модель ответов на опросы."""

    quiz = models.ForeignKey(
        verbose_name='Опрос',
        to=Quiz,
        related_name='answer',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name='Ответ',
        max_length=QUIZ_ANSWER_MAX_LEN,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('quiz', 'text'),
                name='unique_quiz_answer_text',
            ),
        )
        ordering = ('id',)
        verbose_name = 'Ответ на опрос'
        verbose_name_plural = 'Ответы на опросы'

    def __str__(self):
        return f'{self.quiz}: {self.text[:QUIZ_ANSWER_SLICE]}'


class AnswerUser(models.Model):
    """Модель учета ответивших на вопрос опроса."""

    answer = models.ForeignKey(
        verbose_name='Ответ на опрос',
        to=Answer,
        related_name='answer_user',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Ответивший пользователь',
        to=User,
        related_name='answer_user',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('answer', 'user'),
                name='unique_answer_user',
            ),
        )
        ordering = ('id',)
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'

    def __str__(self):
        return f'{self.user}: {self.answer[:QUIZ_ANSWER_SLICE]}'


class NewsCategory(models.Model):
    """Модель категорий новостей."""

    name = models.CharField(
        verbose_name='Название',
        max_length=NEWS_CATEGORY_MAX_LEN,
        choices=NEWS_CATEGORY_CHOICES,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория новостей'
        verbose_name_plural = 'Категории новостей'

    def __str__(self):
        return self.name


class News(models.Model):
    """Модель новостей."""

    category = models.ForeignKey(
        verbose_name='Категория',
        to=NewsCategory,
        related_name='news',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=NEWS_TEXT_MAX_LEN,
        unique=True,
    )
    address = models.ForeignKey(
        verbose_name='Адрес',
        to=Address,
        related_name='news',
        on_delete=models.PROTECT,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True,
    )
    quiz = models.ForeignKey(
        verbose_name='Опрос',
        to=Quiz,
        related_name='news',
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.category} ({self.pub_date})'


class NewsComment(models.Model):
    """Класс комментариев к новостям."""

    author = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        related_name='comment',
        on_delete=models.CASCADE,
    )
    news = models.ForeignKey(
        verbose_name='Новость',
        to=News,
        related_name='comment',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name='Комментарий',
        max_length=NEWS_COMMENT_MAX_LEN,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('news', 'text', 'pub_date'),
                name='unique_single_comment',
            ),
        )
        ordering = ('pub_date',)
        verbose_name = 'Комментарий новости'
        verbose_name_plural = 'Комментарии новостей'

    def __str__(self):
        return f'{self.comment[:NEWS_COMMENT_SLICE]} ({self.news})'


class NewsPicture(models.Model):
    """Класс картинок в новостях."""

    news = models.ForeignKey(
        verbose_name='Новость',
        to=News,
        related_name='picture',
        on_delete=models.CASCADE,
    )
    picture = models.ImageField(
        verbose_name='Картинка',
        upload_to=NEWS_PICTURES_PATH,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('news', 'picture'),
                name='unique_news_picture',
            ),
        )
        ordering = ('news', 'id',)
        verbose_name = 'Картинка новости'
        verbose_name_plural = 'Картинки новостей'

    def __str__(self):
        return f'{self.picture} ({self.news})'


class Appeal(models.Model):
    """Модель обращений граждан."""

    user = models.ForeignKey(
        verbose_name='Гражданин',
        to=User,
        related_name='appeal',
        on_delete=models.SET_NULL,
        null=True,
    )
    topic = models.CharField(
        verbose_name='Тема',
        max_length=APPEAL_TOPIC_MAX_LEN,
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=APPEAL_TEXT_MAX_LEN,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True,
    )
    address = models.ForeignKey(
        verbose_name='Адрес',
        to=Address,
        related_name='appeal',
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
    )
    answer = models.TextField(
        verbose_name='Ответ',
        max_length=APPEAL_TEXT_MAX_LEN,
        default=None,
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name='Статус ответа',
        max_length=APPEAL_STATUS_MAX_LEN,
        choices=APPEAL_STATUS_CHOICES,
        default=APPEAL_STAGE_INITIAL,
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Оценка ответа',
        validators=(
            MaxValueValidator(
                limit_value=APPEAL_RATING_MAX_VAL,
                message=APPEAL_RATING_MESSAGE,
            ),
        ),
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'text'),
                name='unique_user_text',
            ),
        )
        ordering = ('id',)
        verbose_name = 'Обращение гражданина'
        verbose_name_plural = 'Обращение граждан'

    def __str__(self):
        return f'{self.user} ({self.pub_date})'
