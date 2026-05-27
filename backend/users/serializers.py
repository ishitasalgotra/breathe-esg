from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TenantTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["tenant_id"] = user.tenant_id
        token["role"] = user.role
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {"id": self.user.id, "email": self.user.email, "tenant_id": self.user.tenant_id, "role": self.user.role}
        return data


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    role = serializers.CharField()
    tenant_id = serializers.IntegerField(allow_null=True)
    tenant_name = serializers.CharField(source="tenant.name", allow_null=True)
