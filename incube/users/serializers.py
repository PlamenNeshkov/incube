from rest_framework import serializers
from users import models

class StripeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StripeAccount
        fields = ('stripe_id', 'pub_key')
        read_only_fields = ('stripe_id', 'pub_key')

class UserSerializer(serializers.ModelSerializer):
    stripe_account = StripeAccountSerializer(read_only=True)

    class Meta:
        model = models.User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'stripe_account')
        read_only_fields = ('username',)

class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = models.User
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name', 'auth_token')
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
