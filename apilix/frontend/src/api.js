// Thin client for the Django REST API (/api is proxied by Vite in dev).
const BASE = '/api';

export async function fetchItems({ search = '', category = '', tag = '', ordering = '-stars', page = 1 } = {}, signal) {
  const params = new URLSearchParams();
  if (search) params.set('search', search);
  if (category) params.set('category', category);
  if (tag) params.set('tag', tag);
  if (ordering) params.set('ordering', ordering);
  if (page > 1) params.set('page', page);
  const res = await fetch(`${BASE}/items/?${params}`, { signal, credentials: 'include' });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json(); // { count, next, previous, results: [...] }
}

export async function fetchCategories() {
  const res = await fetch(`${BASE}/categories/`);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}
