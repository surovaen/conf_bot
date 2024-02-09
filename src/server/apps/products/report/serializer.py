from rest_framework import serializers


class BreakfastUserSerializer(serializers.Serializer):
    """Класс-сериализатор участников коуч-завтрака."""

    name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    menu = serializers.CharField()

    def get_name(self, obj):
        return obj.user.full_name

    def get_phone_number(self, obj):
        return obj.user.phone_number


class BreakfastSerializer(serializers.Serializer):
    """Класс-сериализатор коуч-завтрака."""

    title = serializers.CharField()
    date = serializers.DateField(format='%d.%m.%Y')
    time = serializers.TimeField(format='%H:%M')
    users = BreakfastUserSerializer(many=True)
