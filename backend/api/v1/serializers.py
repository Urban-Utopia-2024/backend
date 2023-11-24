from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from info.models import Answer, News, NewsComment, NewsPicture, Quiz
from user.models import Address, User


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор получения адреса."""

    class Meta:
        model = Address
        fields = (
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределяет TokenObtainPairSerializer для access токена:
        - добавляет поле is_staff, если оно True
        - добавляет поле is_municipal, если оно True
    """
    @classmethod
    def get_token(cls, user):
        token: dict[str, any] = super().get_token(user)
        for attr in ('is_staff', 'is_municipal'):
            val: bool = getattr(user, attr)
            if val:
                token[attr] = user.is_staff
        return token


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор ответов на опросы."""

    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = (
            'id',
            'text',
            'user_count',
        )

    def get_user_count(self, obj):
        return obj.answer_user.count()


class UserShortSerializer(serializers.ModelSerializer):
    """Сериализатор краткого представления данных пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'rating',
        )


class NewsCommentSerializer(serializers.ModelSerializer):
    """Сериализатор получения картинок новости."""

    author = UserShortSerializer()

    class Meta:
        model = NewsComment
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
        )


class NewsPictureSerializer(serializers.ModelSerializer):
    """Сериализатор получения картинок новости."""

    class Meta:
        model = NewsPicture
        fields = (
            'id',
            'picture',
        )


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор получения опроса."""

    answer = AnswerSerializer(many=True)

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'answer',
        )


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор получения новости."""

    address = AddressSerializer()
    category = serializers.CharField(source='category.name')
    comment = NewsCommentSerializer(many=True)
    quiz = QuizSerializer()
    picture = NewsPictureSerializer(many=True)

    class Meta:
        model = News
        fields = (
            'id',
            'category',
            'text',
            'address',
            'pub_date',
            'comment',
            'quiz',
            'picture',
        )

class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        isinstance: User = super().create(validated_data)
        isinstance.set_password(isinstance.password)
        isinstance.save()
        return isinstance
