"""Django admin: add, edit and moderate hub items."""
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Category, Item, Star, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "badge", "order", "item_count")
    list_editable = ("order",)
    search_fields = ("name",)

    @admin.display(description="Colour")
    def badge(self, obj):
        return format_html('<span style="background:{};padding:2px 10px;border-radius:9px">&nbsp;</span>', obj.color)

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("full_name", "category", "status", "is_featured", "license", "stars", "downloads", "date_added")
    list_display_links = ("full_name",)
    list_editable = ("status", "is_featured")          # moderate straight from the list
    list_filter = ("status", "category", "license", "is_featured", "tags")
    search_fields = ("name", "summary", "description", "author__username", "tags__name")
    autocomplete_fields = ("author",)
    filter_horizontal = ("tags",)
    readonly_fields = ("date_added", "updated_at", "stars", "downloads")
    date_hierarchy = "date_added"
    list_per_page = 50
    actions = ("publish", "hide", "feature")
    fieldsets = (
        (None, {"fields": ("name", "slug", "author", "category", "tags", "summary", "description")}),
        ("Install and source", {"fields": ("github_url", "install_command", "license")}),
        ("Moderation", {"fields": ("status", "is_featured")}),
        ("Statistics", {"fields": ("stars", "downloads", "date_added", "updated_at"), "classes": ("collapse",)}),
    )
    prepopulated_fields = {"slug": ("name",)}

    @admin.action(description="Publish selected items")
    def publish(self, request, queryset):
        n = queryset.update(status=Item.Status.PUBLISHED)
        self.message_user(request, f"{n} item(s) published.", messages.SUCCESS)

    @admin.action(description="Hide selected items")
    def hide(self, request, queryset):
        n = queryset.update(status=Item.Status.HIDDEN)
        self.message_user(request, f"{n} item(s) hidden.", messages.WARNING)

    @admin.action(description="Feature on the homepage")
    def feature(self, request, queryset):
        n = queryset.update(is_featured=True)
        self.message_user(request, f"{n} item(s) featured.", messages.SUCCESS)


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "created_at")
    search_fields = ("user__username", "item__name")
