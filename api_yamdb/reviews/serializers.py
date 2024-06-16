from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comment, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('title',)

    def validate(self, attrs):
        title_id = self.context.get('view').kwargs.get('title_id')

        title = Title.objects.filter(pk=title_id).first()

        if title:

            review = Review.objects.filter(
                author=self.context['request'].user,
                title=title)

            if review:
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв для этого произведения!')

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
