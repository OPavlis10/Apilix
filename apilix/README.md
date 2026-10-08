# Apilix - prototype

The Open Source Ecosystem for Developers. A free, community hub in the style of Hugging Face for
AI models / RAG / agents / prompts, UI components, backend utilities and DevOps templates.

```
apilix/
├── docker-compose.yml        # local MariaDB 11.4
├── backend/                  # Django 5 + Django REST Framework + Django admin
│   ├── apilix/settings.py    # MariaDB (utf8mb4), DRF, CORS for Vite
│   └── catalog/
│       ├── models.py         # Category, Tag, Item, Star
│       ├── admin.py          # add / edit / moderate items
│       ├── serializers.py    # list, detail, submit
│       ├── filters.py        # ?category= ?tag= ?license= ?author= ?featured=
│       ├── views.py          # /api/items/ /api/categories/ /api/tags/
│       └── management/commands/seed_apilix.py   # demo data for the jury
└── frontend/                 # React 18 + Vite + Tailwind CSS 3
    └── src/
        ├── components/LibraryCard.jsx   # Hugging Face style card
        ├── components/Navbar.jsx        # logo, global search, tabs, Submit Library, login
        ├── components/Hero.jsx          # headline + real-time search + category chips
        ├── hooks/useItems.js            # debounced search, cancels stale requests
        └── App.jsx
```

## 1. Run it

**Database**

```bash
docker compose up -d        # MariaDB on 127.0.0.1:3306, db / user / password = apilix
```

No Docker? Set `DB_ENGINE=sqlite` in `backend/.env` for a quick demo without MariaDB.

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt                       # mysqlclient needs the MariaDB/MySQL client libraries
cp .env.example .env
python manage.py migrate
python manage.py seed_apilix                          # 4 categories, 12 sample items
python manage.py createsuperuser
python manage.py runserver                            # http://127.0.0.1:8000/admin/
```

**Frontend**

```bash
cd frontend
npm install
npm run dev                                           # http://localhost:5173 (proxies /api to :8000)
```

## 2. API

| Request | What it does |
|---|---|
| `GET /api/items/` | published items, 24 per page, sorted by stars |
| `GET /api/items/?search=rag` | text search in name, summary, description, author and tags |
| `GET /api/items/?category=ai` | filter by hub: `ai`, `ui`, `backend`, `devops` |
| `GET /api/items/?tag=react&license=MIT` | filter by tag and licence |
| `GET /api/items/?ordering=-stars` | sort by `stars`, `downloads`, `date_added`, `updated_at`, `name` (`-` = descending) |
| `GET /api/items/<slug>/` | detail incl. README, GitHub URL and install command |
| `POST /api/items/` | Submit Library (logged in); the item waits for review |
| `POST /api/items/<slug>/star/` | toggle a star (logged in) |
| `POST /api/items/<slug>/download/` | count a download |
| `GET /api/categories/` | the four hubs with item counts |
| `GET /api/tags/?search=re` | tag autocomplete |

Parameters combine: `/api/items/?search=django&category=backend&ordering=-downloads`.

## 3. Admin panel (`/admin/`)

* **Items**: change `status` (Waiting for review / Published / Hidden) and `featured` directly in the list.
* Bulk actions: *Publish selected items*, *Hide selected items*, *Feature on the homepage*.
* Filters by status, category, licence and tag; search by name, author and tags.
* **Categories**: colour, icon key and order of the four hubs. **Tags**: free tags.

Items sent through the API always arrive as *Waiting for review*, so nothing is public before a moderator approves it.

## 4. Not in the prototype yet

* User registration. Log in uses Django's session login at `/api-auth/login/`; create users in the admin.
* The Submit Library form in React. The API endpoint is ready; the button opens the admin for now.
* Item detail page with README rendering.
