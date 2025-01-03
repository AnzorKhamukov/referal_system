from rest_framework import serializers as s
from users.models import User


class LoginSerializer(s.Serializer):
    phone = s.RegexField(
        regex=r'^([7]{1}[9]{1}[0-9]{9})?$',
        min_length=11,
        max_length=11
    )


class SMSCodeSerializer(s.Serializer):
    sms_code = s.RegexField(
        regex=r'^[0-9]{4}?$',
        max_length=4,
        min_length=4
    )
    sms_token = s.CharField(required=False)


class UserSerializer(s.ModelSerializer):
    invited_users_phones = s.SerializerMethodField(read_only=True)
    invited_by = s.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'invitation_code',
            'invited_by',
            'invited_users_phones'
        ]
        read_only_fields = [
            'invitation_code',
            'invited_by',
            'invited_users_phones',
            'phone'
        ]

    def get_invited_users_phones(self, obj: User):
        return User.objects.filter(
            invited_by=obj.pk).values_list('phone', flat=True)

    def get_invited_by(self, obj: User):
        if obj.invited_by:
            return User.objects.get(pk=obj.invited_by.pk).phone
        return None


class InvitedBySerializer(s.Serializer):
    invitation_code = s.RegexField(regex=r'^[0-9A-Z]{6}?$',)
