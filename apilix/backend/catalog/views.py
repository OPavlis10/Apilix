from django.db.models import Count, F, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import ItemFilter
from .models import Category, Item, Star, Tag
from .serializers import (CategorySerializer, ItemDetailSerializer, ItemListSerializer,
                          ItemSubmitSerializer, TagSerializer)


class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    GET  /api/items/?search=rag&category=ai&tag=python&ordering=-stars
    GET  /api/items/<slug>/
    POST /api/items/                 (logged in, goes to moderation)
    POST /api/items/<slug>/star/     (toggle star)
    POST /api/items/<slug>/download/ (count a download / install copy)
    """

    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = ItemFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "summary", "description", "author__username", "tags__name"]
    ordering_fields = ["stars", "downloads", "date_added", "updated_at", "name"]
    ordering = ["-stars"]

    def get_queryset(self):
        qs = Item.objects.select_related("author", "category").prefetch_related("tags")
        if self.action in ("list", "retrieve", "star", "download"):
            qs = qs.filter(status=Item.Status.PUBLISHED)
        return qs.distinct()  # tag search joins M2M, avoid duplicates

    def get_serializer_class(self):
        if self.action == "create":
            return ItemSubmitSerializer
        if self.action == "retrieve":
            return ItemDetailSerializer
        return ItemListSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        item = ser.save()
        return Response({"slug": item.slug, "status": item.status,
                         "detail": "Thanks! Your library is waiting for review."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def star(self, request, slug=None):
        item = self.get_object()
        star, created = Star.objects.get_or_create(user=request.user, item=item)
        if created:
            Item.objects.filter(pk=item.pk).update(stars=F("stars") + 1)
        else:
            star.delete()
            Item.objects.filter(pk=item.pk, stars__gt=0).update(stars=F("stars") - 1)
        item.refresh_from_db(fields=["stars"])
        return Response({"starred": created, "stars": item.stars})

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def download(self, request, slug=None):
        item = self.get_object()
        Item.objects.filter(pk=item.pk).update(downloads=F("downloads") + 1)
        item.refresh_from_db(fields=["downloads"])
        return Response({"downloads": item.downloads})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/categories/ - the four hubs with item counts (for tabs)."""

    serializer_class = CategorySerializer
    lookup_field = "slug"
    pagination_class = None
    filter_backends = []

    def get_queryset(self):
        return (Category.objects
                .annotate(item_count=Count("items", filter=Q(items__status=Item.Status.PUBLISHED)))
                .order_by("order", "name"))  # Meta.ordering is ignored with GROUP BY


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/tags/?search=re - tag autocomplete."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
