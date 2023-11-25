from drf_spectacular.utils import extend_schema_field
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from info.models import Appeal, Answer, News, NewsComment, NewsPicture, Quiz
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


class AppealAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор проверки ответа обращения."""

    class Meta:
        model = Appeal
        fields = (
            'answer',
        )


class AppealRatingSerializer(serializers.ModelSerializer):
    """Сериализатор проверки оценки обращения."""

    class Meta:
        model = Appeal
        fields = (
            'rating',
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
    """Сериализатор представления ответов на опросы."""

    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = (
            'id',
            'text',
            'user_count',
        )

    @extend_schema_field(int)
    def get_user_count(self, obj):
        return obj.answer_user.count()


class UserFullSerializer(serializers.ModelSerializer):
    """Сериализатор полного представления данных пользователя."""

    address = AddressSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'address',
            'phone',
            'photo',
            'rating',
            'is_municipal',
            'municipal_name',
        )


class MunicipalSerializer(serializers.ModelSerializer):
    """Сериализатор представления данных муниципальной службы."""

    address = AddressSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'municipal_name',
            'address',
            'email',
            'phone',
            'photo',
        )


class AppealAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор представления обращения граждан.

    Используется для отображения информации администратору портала.
    """

    address = AddressSerializer()
    municipal = UserFullSerializer()
    user = UserFullSerializer()

    class Meta:
        model = Appeal
        fields = (
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


class AppealMunicipalSerializer(serializers.ModelSerializer):
    """
    Сериализатор представления обращения граждан.

    Используется для отображения информации муниципальной службе.
    """

    address = AddressSerializer()
    user = UserFullSerializer()

    class Meta:
        model = Appeal
        fields = (
            'id',
            'user',
            'topic',
            'text',
            'pub_date',
            'address',
            'answer',
            'status',
            'rating',
        )


class AppealUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор представления обращения граждан.

    Используется для отображения информации пользователю.
    """

    address = AddressSerializer()
    municipal = MunicipalSerializer()

    class Meta:
        model = Appeal
        fields = (
            'id',
            'municipal',
            'topic',
            'text',
            'pub_date',
            'address',
            'answer',
            'status',
            'rating',
        )


class AppealUserPostSerializer(serializers.ModelSerializer):
    """
    Сериализатор представления обращения граждан.

    Используется для отображения информации пользователю.
    """

    address = AddressSerializer()
    municipal_id = serializers.IntegerField()

    class Meta:
        model = Appeal
        fields = (
            'municipal_id',
            'topic',
            'text',
            'address',
        )

    def create(self, validated_data):
        address, _ = Address.objects.get_or_create(
            **validated_data.get('address')
        )
        user: User = User.objects.get(id=self.context.get('user_id'))
        municipal: User = User.objects.get(id=validated_data.get('municipal_id'))  # noqa (E501)
        appeal: Appeal = Appeal.objects.create(
            user=user,
            municipal=municipal,
            topic=validated_data.get('topic'),
            text=validated_data.get('text'),
            address=address,
        )
        return appeal


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
