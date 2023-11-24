from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from urban_utopia_2024.app_data import (
    ADDRESS_APARTMENT_MAX_VAL, ADDRESS_BUILDING_MAX_LEN, ADDRESS_CITY_MAX_LEN,
    ADDRESS_DISTRICT_MAX_LEN, ADDRESS_INDEX_MAX_VAL, ADDRESS_ENTRANCE_MAX_VAL,
    ADDRESS_FLOOR_MAX_VAL, ADDRESS_HOUSE_MAX_VAL, ADDRESS_STREET_MAX_LEN,
    USER_FULL_EMAIL_MAX_LEN, USER_NAME_MAX_LEN, USER_PASS_MAX_LEN,
    USER_PHOTO_PATH, USER_RATING_MAX_VAL,
)
from user.validators import (
    validate_building, validate_email, validate_lat, validate_lon,
    validate_first_name, validate_last_name, validate_password,
)


class Address(models.Model):
    """Модель адреса."""

    city = models.CharField(
        verbose_name='Город',
        max_length=ADDRESS_CITY_MAX_LEN,
    )
    district = models.CharField(
        verbose_name='Район',
        max_length=ADDRESS_DISTRICT_MAX_LEN,
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=ADDRESS_STREET_MAX_LEN,
    )
    house = models.PositiveSmallIntegerField(
        verbose_name='Дом',
        validators=(
            MaxValueValidator(
                ADDRESS_HOUSE_MAX_VAL,
                'Укажите корректный номер дома.',
            ),
        ),
    )
    building = models.CharField(
        verbose_name='Корпус',
        max_length=ADDRESS_BUILDING_MAX_LEN,
        validators=(
            validate_building,
        ),
    )
    entrance = models.PositiveSmallIntegerField(
        verbose_name='Подъезд',
        validators=(
            MaxValueValidator(
                ADDRESS_ENTRANCE_MAX_VAL,
                'Укажите корректный подъезд.',
            ),
        ),
        null=True,
        blank=True,
    )
    floor = models.PositiveSmallIntegerField(
        verbose_name='Этаж',
        validators=(
            MaxValueValidator(
                ADDRESS_FLOOR_MAX_VAL,
                'Укажите корректный этаж.',
            ),
        ),
        null=True,
        blank=True,
    )
    apartment = models.PositiveSmallIntegerField(
        verbose_name='Квартира',
        validators=(
            MaxValueValidator(
                ADDRESS_APARTMENT_MAX_VAL,
                'Укажите корректный номер квартиры.',
            ),
        ),
        null=True,
        blank=True,
    )
    # INFO: данные полей 'index', 'latitude' и 'longitude'
    #       должны заполняться автоматически в методе save(),
    #       но это стоит денег, и пока что заполняется вручную.
    index = models.PositiveIntegerField(
        verbose_name='Индекс',
        validators=(
            MaxValueValidator(
                ADDRESS_INDEX_MAX_VAL,
                'Укажите корректный индекс.',
            ),
        ),
    )
    latitude = models.FloatField(
        verbose_name='Широта (десятичные градусы)',
        validators=(
            validate_lat,
        ),
    )
    longitude = models.FloatField(
        verbose_name='Долгота (десятичные градусы)',
        validators=(
            validate_lon,
        ),
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('city', 'street', 'house', 'building', 'apartment'),
                name='unique_address',
            ),
        )
        ordering = (
            'city',
            'street',
            'house',
            'apartment',
        )
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        address: str = (
            f'{self.index}, г. {self.city}, ул. {self.street}, '
            f'д. {self.house}, корп. {self.building}'
        )
        if self.apartment:
            address: str = f'{address}, кв. {self.apartment}'
        return address


class UserManager(BaseUserManager):
    """Менеджер модели пользователя."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с полученными почтой и паролем."""
        if not email or not password:
            raise ValueError('Укажите email и password.')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_municipal(self, email, password, **extra_fields):
        """Обрабатывает метод создания муниципального-пользователя."""
        extra_fields.setdefault('is_municipal', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Обрабатывает метод создания пользователя-администратора."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        """Обрабатывает метод создания пользователя."""
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=USER_FULL_EMAIL_MAX_LEN,
        validators=(
            validate_email,
        ),
        unique=True,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=USER_PASS_MAX_LEN,
        validators=(
            validate_password,
        ),
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USER_NAME_MAX_LEN,
        validators=(
            validate_first_name,
        ),
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=USER_NAME_MAX_LEN,
        validators=(
            validate_last_name,
        ),
    )
    address = models.ForeignKey(
        verbose_name='Адрес',
        to=Address,
        related_name='user',
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        region='RU',
        unique=True,
    )
    photo = models.ImageField(
        verbose_name='Фотография профиля',
        upload_to=USER_PHOTO_PATH,
        blank=True,
        null=True
    )
    rating = models.DecimalField(
        verbose_name='Рейтинг',
        max_digits=4,
        decimal_places=1,
        validators=(
            MaxValueValidator(
                USER_RATING_MAX_VAL,
                'Рейтинг не может меньше 0 и больше 100.',
            ),
        ),
        default=0.0,
    )

    # Fields for Municipal Services.
    is_municipal = models.BooleanField(
        verbose_name='Муниципальная служба',
        default=False,
    )
    municipal_name = models.CharField(
        verbose_name='Название муниципальной службы',
        max_length=USER_NAME_MAX_LEN,
        blank=True,
        null=True,
    )

    # Excess fields
    # Copy Django default, set value: None.
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        default=None,
        blank=True,
        null=True
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
