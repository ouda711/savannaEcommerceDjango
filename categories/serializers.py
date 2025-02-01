import os
from random import choice
from string import ascii_lowercase

from rest_framework import serializers
from categories.models import Category
from fileuploads.models import CategoryImage


class CategoryIdAndNameSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    # parent_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), allow_null=True, required=False, source="parent"
    # )

    def get_image_urls(self, category):
        if self.context.get('include_urls', False):
            return [x.file_path for x in category.images.all()]
        return None

    def get_children(self, category):
        children = category.children.all()
        if children.exists():
            return CategoryIdAndNameSerializer(children, many=True, context=self.context).data
        return []

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response.get("image_urls") is None:
            response.pop("image_urls")
        return response

    def create(self, validated_data):
        request = self.context["request"]
        images = request.data.getlist("images", [])

        # Extract and remove `parent_id` from `validated_data`
        parent = validated_data.pop("parent", None)

        # Create category with correct parent reference
        category = Category.objects.create(parent=parent, **validated_data)

        # Handle image uploads
        dir = os.path.join(os.getcwd(), "static", "images", "categories")
        if not os.path.exists(dir):
            os.makedirs(dir)

        for image in images:
            file_name = "".join(choice(ascii_lowercase) for _ in range(16)) + ".png"
            file_path = os.path.join(dir, file_name)

            with open(file_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            CategoryImage.objects.create(
                file_name=file_name,
                original_name=image.name,
                file_length=image.size,
                category=category,
                file_path=file_path.replace(os.getcwd(), "").replace("\\", "/"),
            )

        return category

    class Meta:
        model = Category
        fields = ["id", "name", "children", "image_urls"]
