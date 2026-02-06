from datetime import timezone

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

class OAuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

class RegisterValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)


class AuthValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            email=attrs['email'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError('Неверные данные')
        attrs['user'] = user
        return attrs


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'birthdate',
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            birthdate=validated_data.get('birthdate'),
        )
        return user

class GoogleAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    given_name = serializers.CharField(required=False, allow_blank=True)
    family_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        email = attrs['email']
        given_name = attrs.get('given_name', '')
        family_name = attrs.get('family_name', '')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': self._generate_unique_username(email),
                'first_name': given_name,
                'last_name': family_name,
                'is_active': True,
                'registration_source': 'google',
            },
        )

        if not created:
            user.first_name = given_name or user.first_name
            user.last_name = family_name or user.last_name
            user.is_active = True
            user.last_login = timezone.now()
            user.save(update_fields=['first_name', 'last_name', 'is_active', 'last_login'])
        else:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

        attrs['user'] = user
        return attrs

    def _generate_unique_username(self, email):
        base = email.split('@')[0]
        base = base[:150]
        username = base
        suffix = 1
        while User.objects.filter(username=username).exists():
            suffix_str = str(suffix)
            trimmed_base = base[:150 - len(suffix_str) - 1]
            username = f'{trimmed_base}_{suffix_str}'
            suffix += 1
        return username