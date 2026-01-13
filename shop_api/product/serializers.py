import random

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Название категории должно быть не менее 3 символов"
            )
        return value

    class Meta:
        model = Category
        fields = "__all__"




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'stars')




from django.db.models import Avg

class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'reviews', 'rating')

    def get_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg('stars'))['avg']

class ProductSerializer(serializers.ModelSerializer):

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Название товара должно быть не менее 3 символов"
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Цена должна быть больше 0"
            )
        return value

    class Meta:
        model = Product
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):

    def validate_text(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Отзыв должен содержать минимум 5 символов"
            )
        return value

    def validate_stars(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5"
            )
        return value

    class Meta:
        model = Review
        fields = "__all__"

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False
        )

        code = str(random.randint(100000, 999999))

        UserConfirm.objects.create(
            user=user,
            code=code
        )

        return user


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            confirm = user.confirm
        except:
            raise serializers.ValidationError("Пользователь не найден")

        if confirm.code != data['code']:
            raise serializers.ValidationError("Неверный код")

        user.is_active = True
        user.save()
        confirm.delete()

        Token.objects.create(user=user)

        return data


from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Неверные данные")

        if not user.is_active:
            raise serializers.ValidationError("Пользователь не подтвержден")

        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key}
