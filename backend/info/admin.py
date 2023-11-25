from django.contrib import admin

from info.models import (
    Answer, AnswerUser, Appeal,
    News, NewsComment, NewsPicture,
    ServiceCategory, Task, Quiz,
)
from urban_utopia_2024.app_data import ADMIN_LIST_PER_PAGE


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Answer.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID ответа (id)
            - ID опроса (quiz)
            - текст ответа (text)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - ID опроса (quiz)
            - текст ответа (text)
        - list_filter (tuple) - список фильтров:
            - ID опроса (quiz)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'quiz',
        'text',
    )
    list_editable = (
        'quiz',
        'text',
    )
    list_filter = (
        'quiz',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(AnswerUser)
class AnswerUserAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели AnswerUser.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID ответа пользователя (id)
            - ID ответа (answer)
            - ID пользователя (user)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - ID ответа (answer)
            - ID пользователя (user)
        - list_filter (tuple) - список фильтров:
            - ID ответа (answer)
            - ID пользователя (user)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'answer',
        'user',
    )
    list_editable = (
        'answer',
        'user',
    )
    list_filter = (
        'answer',
        'user',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Appeal.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID обращения (id)
            - ID пользователя (user)
            - ID муниципальной службы (municipal)
            - тема обращения (topic)
            - текст обращения (text)
            - дата и время обращения (pub_date)
            - ID адреса (address)
            - текст ответа на обращение (answer)
            - статус обращения (status)
            - рейтинг ответа обращения (rating)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - ID пользователя (user)
            - ID муниципальной службы (municipal)
            - тема обращения (topic)
            - текст обращения (text)
            - ID адреса (address)
            - текст ответа на обращение (answer)
            - статус обращения (status)
            - рейтинг ответа обращения (rating)
        - list_filter (tuple) - список фильтров:
            - ID пользователя (user)
            - ID муниципальной службы (municipal)
            - ID адреса (address)
            - статус обращения (status)
            - рейтинг ответа обращения (rating)
        - search_fields (tuple) - список полей для поиска объектов:
            - тема обращения (topic)
            - текст обращения (text)
            - дата и время обращения (pub_date)
            - текст ответа на обращение (answer)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'user',
        'municipal',
        'topic',
        'text',
        'pub_date',
        'address',
        'answer',
        'status',
        'rating',
    )
    list_editable = (
        'user',
        'municipal',
        'topic',
        'text',
        'address',
        'answer',
        'status',
        'rating',
    )
    list_filter = (
        'user',
        'municipal',
        'address',
        'status',
        'rating',
    )
    search_fields = (
        'topic',
        'text',
        'pub_date',
        'answer',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели News.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID новости (id)
            - категория (category)
            - текст (text)
            - ID адреса (address)
            - дата и время обращения (pub_date)
            - ID опроса (quiz)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - категория (category)
            - текст (text)
            - ID адреса (address)
            - ID опроса (quiz)
        - list_filter (tuple) - список фильтров:
            - категория (category)
            - ID адреса (address)
        - search_fields (tuple) - список полей для поиска объектов:
            - текст (text)
            - дата и время обращения (pub_date)
            - ID опроса (quiz)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'category',
        'text',
        'address',
        'pub_date',
        'quiz',
    )
    list_editable = (
        'category',
        'text',
        'address',
        'quiz',
    )
    list_filter = (
        'category',
        'address',
    )
    search_fields = (
        'text',
        'pub_date',
        'quiz',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели ServiceCategory.  # noqa (E501)

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID категории новостей (id)
            - название категории (name)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - название категории (name)
        - search_fields (tuple) - список полей для поиска объектов:
            - название категории (name)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'name',
    )
    list_editable = (
        'name',
    )
    search_fields = (
        'name',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели NewsComment.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID комментария новости (id)
            - ID автора (author)
            - ID новости (news)
            - текст комментария (text)
            - дата и время публикации (pub_date)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - ID автора (author)
            - ID новости (news)
            - текст комментария (text)
        - list_filter (tuple) - список фильтров:
            - ID автора (author)
            - ID новости (news)
        - search_fields (tuple) - список полей для поиска объектов:
            - текст комментария (text)
            - дата и время публикации (pub_date)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'author',
        'news',
        'text',
        'pub_date',
    )
    list_editable = (
        'author',
        'news',
        'text',
    )
    list_filter = (
        'author',
        'news',
    )
    search_fields = (
        'text',
        'pub_date',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(NewsPicture)
class NewsPictureAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели NewsPicture.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID картинки новости (id)
            - ID новости (news)
            - картинка (picture)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - ID новости (news)
            - картинка (picture)
        - list_filter (tuple) - список фильтров:
            - ID новости (news)
        - search_fields (tuple) - список полей для поиска объектов:
            - картинка (picture)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'news',
        'picture',
    )
    list_editable = (
        'news',
        'picture',
    )
    list_filter = (
        'news',
    )
    search_fields = (
        'picture',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Task.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID задачи (id)
            - заголовок (title)
            - ID муниципальной службы (municipal)
            - ID адреса (address)
            - дата и время обращения (pub_date)
            - дата и время начала работ (start_date)
            - дата и время окончания работ (end_date)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - заголовок (title)
            - ID муниципальной службы (municipal)
            - ID адреса (address)
            - дата и время начала работ (start_date)
            - дата и время окончания работ (end_date)
        - list_filter (tuple) - список фильтров:
            - ID муниципальной службы (municipal)
            - ID адреса (address)
        - search_fields (tuple) - список полей для поиска объектов:
            - заголовок (title)
            - дата и время обращения (pub_date)
            - дата и время начала работ (start_date)
            - дата и время окончания работ (end_date)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'title',
        'municipal',
        'address',
        'pub_date',
        'start_date',
        'end_date',
    )
    list_editable = (
        'title',
        'municipal',
        'address',
        'start_date',
        'end_date',
    )
    list_filter = (
        'municipal',
        'address',
    )
    search_fields = (
        'title',
        'pub_date',
        'start_date',
        'end_date',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Quiz.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID опроса (id)
            - заголовок (title)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - заголовок (title)
        - search_fields (tuple) - список полей для поиска объектов:
            - заголовок (title)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'title',
    )
    list_editable = (
        'title',
    )
    search_fields = (
        'title',
    )
    list_per_page = ADMIN_LIST_PER_PAGE
