"""python manage.py seed_apilix - demo data for the jury (all items are made-up samples)."""
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from catalog.models import Category, Item, Tag

CATEGORIES = [
    ("ai", "Models / AI", "Models, RAG pipelines, agents and prompts", "brain", "#c8b4ff", 1),
    ("ui", "UI Components", "React, Tailwind CSS and Vue components", "layout", "#ff7ab6", 2),
    ("backend", "Backend / SQL", "Django, Python and MariaDB/SQL utilities", "database", "#93f9d2", 3),
    ("devops", "DevOps", "Docker, Kubernetes and Nginx templates", "server", "#ffd36b", 4),
]
ITEMS = [
    ("ai", "czech-rag-starter", "RAG pipeline for Czech documents with chunking and citations.", ["python", "rag", "llm"], "pip install czech-rag-starter", "Apache-2.0"),
    ("ai", "prompt-pack-code-review", "Tested prompts for code review in pull requests.", ["prompts", "llm"], "", "CC0-1.0"),
    ("ai", "support-agent-template", "Customer support agent with tools, memory and guardrails.", ["agents", "python", "llm"], "pip install support-agent-template", "MIT"),
    ("ui", "glass-cards", "Glassmorphism cards for React with Tailwind CSS.", ["react", "tailwind"], "npm i @apilix/glass-cards", "MIT"),
    ("ui", "vue-data-table", "Sortable, filterable data table for Vue 3.", ["vue", "tailwind"], "npm i vue-data-table-lite", "MIT"),
    ("ui", "shader-backgrounds", "Animated WebGL backgrounds as React components.", ["react", "webgl"], "npm i @apilix/shader-bg", "MIT"),
    ("backend", "django-audit-log", "Model change history for Django with admin integration.", ["django", "python"], "pip install django-audit-log-lite", "BSD-3-Clause"),
    ("backend", "mariadb-fulltext-helpers", "Full-text search helpers for Django on MariaDB.", ["mariadb", "django", "sql"], "pip install mariadb-fts", "MIT"),
    ("backend", "sql-migration-cheatsheet", "Safe patterns for zero-downtime schema changes.", ["sql", "mariadb"], "", "CC-BY-4.0"),
    ("devops", "django-docker-compose", "Production-ready Docker Compose: Django, MariaDB, Redis, Nginx.", ["docker", "django", "nginx"], "git clone https://github.com/apilix/django-docker-compose", "MIT"),
    ("devops", "k8s-django-helm", "Helm chart for Django apps with migrations job.", ["kubernetes", "helm"], "helm install app ./chart", "Apache-2.0"),
    ("devops", "nginx-hardening", "Hardened Nginx config with TLS, headers and rate limits.", ["nginx", "security"], "", "MIT"),
]


class Command(BaseCommand):
    help = "Create categories, tags, demo users and sample items."

    def handle(self, *args, **opts):
        for slug, name, desc, icon, color, order in CATEGORIES:
            Category.objects.update_or_create(slug=slug, defaults=dict(name=name, description=desc, icon=icon, color=color, order=order))
        User = get_user_model()
        authors = []
        for u in ("apilix", "devteam", "studentlab"):
            user, _ = User.objects.get_or_create(username=u)
            authors.append(user)
        rnd = random.Random(42)
        for cat, name, summary, tags, cmd, lic in ITEMS:
            author = rnd.choice(authors)
            item, _ = Item.objects.update_or_create(
                name=name, author=author,
                defaults=dict(category=Category.objects.get(slug=cat), summary=summary, install_command=cmd, license=lic,
                              github_url=f"https://github.com/{author.username}/{name}", status=Item.Status.PUBLISHED,
                              stars=rnd.randint(5, 900), downloads=rnd.randint(50, 25000),
                              description=f"# {name}\n\n{summary}\n\n_Sample item created by seed_apilix._"))
            item.tags.set([Tag.objects.get_or_create(name=t)[0] for t in tags])
        Item.objects.filter(name__in=["czech-rag-starter", "glass-cards", "django-docker-compose"]).update(is_featured=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {Category.objects.count()} categories, {Item.objects.count()} items."))
