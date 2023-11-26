from django.contrib import admin

from urban_utopia_2024.app_data import ADMIN_LIST_PER_PAGE
from user.models import Address, User


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Address.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID адреса (id)
            - наименование города (city)
            - наименование района (district)
            - наименование улицы (street)
            - номер дома (house)
            - номер корпуса (building)
            - номер парадной (entrance)
            - номер этажа (floor)
            - номер квартиры (apartment)
            - почтовый индекс (index)
            - координата широты (latitude)
            - координата долготы (longitude)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - наименование города (city)
            - наименование района (district)
            - наименование улицы (street)
            - номер дома (house)
            - номер корпуса (building)
            - номер парадной (entrance)
            - номер этажа (floor)
            - номер квартиры (apartment)
            - почтовый индекс (index)
            - координата широты (latitude)
            - координата долготы (longitude)
        - list_filter (tuple) - список фильтров:
            - наименование города (city)
            - наименование района (district)
            - наименование улицы (street)
            - почтовый индекс (index)
        - list_per_page (int) - количество объектов на одной странице

    Методы:
        - services_list - возвращает строковое перечисление всех сервисов и их
                          количества в заказе для показа в list_display.
                          Атрибут short_description устанавливает название
                          столбца в интерфейсе
    """
    list_display = (
        'id',
        'city',
        'district',
        'street',
        'house',
        'building',
        'entrance',
        'floor',
        'apartment',
        'index',
        'latitude',
        'longitude',
    )
    list_editable = (
        'city',
        'district',
        'street',
        'house',
        'building',
        'entrance',
        'floor',
        'apartment',
        'index',
        'latitude',
        'longitude',
    )
    list_filter = (
        'city',
        'district',
        'street',
        'index',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели User.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID пользователя (id)
            - электронная почта пользователя (email)
            - имя пользователя (first_name)
            - отчество пользователя (mid_name)
            - фамилия пользователя (last_name)
            - ID адреса пользователя (address)
            - контактный телефон по стандарту E.164 (phone)
            - фотография (photo)
            - рейтинг (rating)
            - статус администратора (is_staff)
            - статус муниципальной службы (is_municipal)
            - название муниципальной службы (municipal_name)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - электронная почта пользователя (email)
            - имя пользователя (first_name)
            - отчество пользователя (mid_name)
            - фамилия пользователя (last_name)
            - ID адреса пользователя (address)
            - контактный телефон по стандарту E.164 (phone)
            - фотография (photo)
            - рейтинг (rating)
            - статус администратора (is_staff)
            - статус муниципальной службы (is_municipal)
            - название муниципальной службы (municipal_name)
        - list_filter (tuple) - список фильтров:
            - имя пользователя (first_name)
            - отчество пользователя (mid_name)
            - фамилия пользователя (last_name)
            - рейтинг (rating)
            - статус администратора (is_staff)
            - статус муниципальной службы (is_municipal)
        - search_fields (tuple) - список полей для поиска объектов:
            - электронная почта пользователя (email)
            - контактный телефон по стандарту E.164 (phone)
            - название муниципальной службы (municipal_name)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'email',
        'first_name',
        'mid_name',
        'last_name',
        'address',
        'phone',
        'photo',
        'rating',
        'is_staff',
        'is_municipal',
        'municipal_name',
    )
    list_editable = (
        'email',
        'first_name',
        'mid_name',
        'last_name',
        'address',
        'phone',
        'photo',
        'rating',
        'is_staff',
        'is_municipal',
        'municipal_name',
    )
    list_filter = (
        'first_name',
        'mid_name',
        'last_name',
        'rating',
        'is_staff',
        'is_municipal',
    )
    search_fields = (
        'email',
        'phone',
        'municipal_name',
    )
    list_per_page = ADMIN_LIST_PER_PAGE
