from rest_framework import serializers
from accounts.models import Profile


class OrderRatesSerializer(serializers.ModelSerializer):
    orders = serializers.IntegerField()
    testimonials = serializers.IntegerField()
    city_title = serializers.CharField()
    avatar = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    ave_grade = serializers.IntegerField()
    gems = serializers.IntegerField()
    views = serializers.SerializerMethodField()
    get_public_abs_url = serializers

    class Meta:
        model = Profile
        fields = ('name', 'city_title', 'description', 'avatar', 'get_public_abs_url', 'position', 'orders', 'testimonials', 'ave_grade', 'gems', 'views')

    def get_avatar(self, obj):
        return obj.get_avatar().get_thumbnail({'size': (250, 250), 'crop': True}).url

    def get_views(self, obj):
        viewinstance = obj.views.all()
        if viewinstance:
            return viewinstance[0].profiles.count()
        return 0

    def get_description(self, obj):
        return obj.description[:400] + '...'
