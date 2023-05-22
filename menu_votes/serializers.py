from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from menu_scores.models import MenuScore
from menu_scores.serializers import MenuScoreSerializer
from menu_votes.models import MenuVote
from menus.models import Menu
from menus.serializers import MenuRetrieveSerializer


class MenuVoteCreateSerializerV1(serializers.ModelSerializer):
    menu = serializers.CharField(required=True)

    class Meta:
        model = MenuVote
        fields = ['user', 'menu']

    def create(self, validated_data):
        try:
            # default score
            score = MenuScore.objects.all().order_by('id').first()  # todo: may need a slug here
            menu_uuid = validated_data.pop('menu')
            menu = Menu.objects.get(uuid=menu_uuid)
            validated_data['menu'] = menu

        except Exception as exc:
            raise ValidationError({'error': exc})

        validated_data['score'] = score
        menu_vote = super().create(validated_data)
        return menu_vote


class MenuVoteCreateSerializerV2(serializers.ModelSerializer):
    menus = serializers.ListSerializer(child=serializers.DictField(child=serializers.CharField()))

    class Meta:
        model = MenuVote
        fields = ['user', 'menus']

    def create(self, validated_data):
        menus_data = validated_data.pop('menus')
        user = self.context.get('request').user
        menu_vote = MenuVote.objects.none()

        for menu_data in menus_data:
            menu_uuid = menu_data.get('menu')
            score_uuid = menu_data.get('score')

            menu = Menu.objects.get(uuid=menu_uuid)
            score = MenuScore.objects.get(uuid=score_uuid)

            menu_vote = MenuVote.objects.create(menu=menu, score=score, user=user)

        return menu_vote

    def to_representation(self, instance):
        if instance and instance.pk:
            return {'detail': 'Success'}
        return {'error': 'Failed to add vote'}


class MenuVoteListTodaySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = MenuVote
        fields = ['user', 'menu', 'score', 'created_at']

    # noinspection PyMethodMayBeStatic
    def get_user(self, instance):
        if instance and instance.user:
            return instance.user.username
        return None

    def get_menu(self, instance):
        if instance and instance.menu:
            return MenuRetrieveSerializer(
                instance=instance.menu,
                read_only=True,
                context=self.context,
            ).data
        return None

    def get_score(self, instance):
        if instance and instance.score:
            return MenuScoreSerializer(
                instance=instance.score,
                read_only=True,
                context=self.context,
            ).data
        return None
