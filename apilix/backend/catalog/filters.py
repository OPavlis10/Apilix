import django_filters

from .models import Item


class ItemFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")        # ?category=ai
    tag = django_filters.CharFilter(field_name="tags__slug")                 # ?tag=react
    license = django_filters.CharFilter(field_name="license")                # ?license=MIT
    author = django_filters.CharFilter(field_name="author__username")        # ?author=apilix
    featured = django_filters.BooleanFilter(field_name="is_featured")        # ?featured=true

    class Meta:
        model = Item
        fields = ("category", "tag", "license", "author", "featured")
