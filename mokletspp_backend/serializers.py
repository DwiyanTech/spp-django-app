# serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Spp, CustomUserAkun, Petugas, Pembayaran, Siswa
from rest_framework import validators


class UpdateUserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUserAkun
        fields = ('username', 'email','role')

    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUserAkun.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        try:
            instance.username = validated_data['username']
            instance.email = validated_data['email']
            instance.role = validated_data['role']
            instance.save()
            print("berhasil")
            return instance
        except Exception as e:
            print(e)
            raise Exception


class AddUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     validators=[validators.UniqueValidator(queryset=CustomUserAkun.objects.all())])
    role = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUserAkun
        fields = ('username', 'email', 'role', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] is not None:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password Didn't Match"})
        return attrs

    def create(self, validated_data):
        user = CustomUserAkun.objects.create(username=validated_data['username'],
                                             role=validated_data['role'],
                                             email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class SppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spp
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUserAkun
        fields = '__all__'


class PetugasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Petugas
        fields = '__all__'


class PembayaranSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = '__all__'


class SiswaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Siswa
        fields = '__all__'


class SppOnlyCountPaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spp
        fields = '__all__'
