from djoser.serializers import UserSerializer as BasedUserSerializer, UserCreateSerializer

class UserSerializer(BasedUserSerializer):
    class Meta(BasedUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'phone_number']

class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']