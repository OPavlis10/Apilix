"""Apilix catalog models (MariaDB, utf8mb4)."""
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """The four main hubs: AI, UI Components, Backend/SQL, DevOps."""

    class Kind(models.TextChoices):
        AI = "ai", "Models / AI"
        UI = "ui", "UI Components"
        BACKEND = "backend", "Backend / SQL"
        DEVOPS = "devops", "DevOps"

    slug = models.SlugField(max_length=20, unique=True, choices=Kind.choices)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=40, blank=True, help_text="Icon key used by the React app, e.g. 'brain', 'layout', 'database', 'server'.")
    color = models.CharField(max_length=7, default="#c8b4ff", help_text="Hex colour of the category badge.")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Free tags: react, python, mariadb, rag, llm, docker..."""

    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=40, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Item(models.Model):
    """One library / model / component / template in the hub."""

    class License(models.TextChoices):
        MIT = "MIT", "MIT"
        APACHE2 = "Apache-2.0", "Apache 2.0"
        GPL3 = "GPL-3.0", "GPL 3.0"
        BSD3 = "BSD-3-Clause", "BSD 3-Clause"
        CC_BY = "CC-BY-4.0", "CC BY 4.0"
        CC0 = "CC0-1.0", "CC0 1.0"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Waiting for review"
        PUBLISHED = "published", "Published"
        HIDDEN = "hidden", "Hidden"

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(max_length=280, help_text="One-line description shown on the card.")
    description = models.TextField(blank=True, help_text="Full description in Markdown (README).")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="items")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    tags = models.ManyToManyField(Tag, blank=True, related_name="items")
    github_url = models.URLField(blank=True)
    install_command = models.CharField(max_length=255, blank=True, help_text="e.g. pip install ... / npm i ... / docker pull ...")
    license = models.CharField(max_length=20, choices=License.choices, default=License.MIT)
    downloads = models.PositiveIntegerField(default=0)
    stars = models.PositiveIntegerField(default=0, help_text="Denormalised counter, kept in sync by the Star model.")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    is_featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-stars", "-downloads"]
        indexes = [
            models.Index(fields=["status", "category"]),
            models.Index(fields=["-stars"]),
            models.Index(fields=["-downloads"]),
            models.Index(fields=["-date_added"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.author.username}-{self.name}")[:130] or "item"
            slug, n = base, 2
            while Item.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        """Hugging Face style 'author/name'."""
        return f"{self.author.username}/{self.name}"

    def __str__(self):
        return self.full_name


class Star(models.Model):
    """One user starred one item (like on Hugging Face). Item.stars is the counter."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stars")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="star_set")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "item"], name="unique_star_per_user")]

    def __str__(self):
        return f"{self.user} ★ {self.item}"
