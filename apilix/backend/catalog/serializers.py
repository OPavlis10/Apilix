from rest_framework import serializers

from .models import Category, Item, Tag


class CategorySerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ("slug", "name", "description", "icon", "color", "item_count")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "name")


class ItemListSerializer(serializers.ModelSerializer):
    """Compact shape for the card grid."""

    author = serializers.CharField(source="author.username", read_only=True)
    full_name = serializers.CharField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="slug")

    class Meta:
        model = Item
        fields = ("slug", "name", "full_name", "author", "summary", "category", "tags",
                  "license", "stars", "downloads", "is_featured", "date_added", "updated_at")


class ItemDetailSerializer(ItemListSerializer):
    class Meta(ItemListSerializer.Meta):
        fields = ItemListSerializer.Meta.fields + ("description", "github_url", "install_command")


class ItemSubmitSerializer(serializers.ModelSerializer):
    """[Submit Library]: logged-in user sends an item, it waits for moderation."""

    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all())
    tags = serializers.SlugRelatedField(slug_field="slug", queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Item
        fields = ("name", "summary", "description", "category", "tags", "github_url", "install_command", "license")

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        item = Item.objects.create(author=self.context["request"].user, status=Item.Status.PENDING, **validated_data)
        item.tags.set(tags)
        return item
