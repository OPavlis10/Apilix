import { useEffect, useState } from 'react';
import { fetchCategories } from './api';
import Hero from './components/Hero';
import LibraryCard from './components/LibraryCard';
import Navbar from './components/Navbar';
import useItems from './hooks/useItems';

const SORTS = [
  { value: '-stars', label: 'Most stars' },
  { value: '-downloads', label: 'Most downloads' },
  { value: '-date_added', label: 'Recently added' },
];

export default function App() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [ordering, setOrdering] = useState('-stars');
  const [categories, setCategories] = useState([]);
  const [dark, setDark] = useState(true);
  const { items, count, loading, error } = useItems({ search, category, ordering });

  useEffect(() => { fetchCategories().then(setCategories).catch(() => {}); }, []);
  useEffect(() => { document.documentElement.classList.toggle('dark', dark); }, [dark]);

  return (
    <>
      <Navbar search={search} onSearch={setSearch} category={category} onCategory={setCategory} dark={dark} onToggleDark={() => setDark(!dark)} />
      <Hero search={search} onSearch={setSearch} categories={categories} category={category} onCategory={setCategory} />

      <main className="mx-auto max-w-7xl px-4 py-8">
        <div className="mb-4 flex flex-wrap items-baseline justify-between gap-3">
          <h2 className="text-lg font-semibold tracking-tight">
            {category ? categories.find((c) => c.slug === category)?.name : 'All libraries'}
            <span className="ml-2 font-mono text-sm font-normal text-zinc-500">{count}</span>
          </h2>
          <label className="flex items-center gap-2 text-sm text-zinc-500">
            Sort
            <select value={ordering} onChange={(e) => setOrdering(e.target.value)}
                    className="rounded-md border border-zinc-200 bg-transparent px-2 py-1 dark:border-lilac/20">
              {SORTS.map((s) => <option key={s.value} value={s.value} className="dark:bg-ink-900">{s.label}</option>)}
            </select>
          </label>
        </div>

        {error && <p className="rounded-lg border border-rose-300 p-4 text-sm text-rose-500">Cannot reach the API ({error}). Is Django running on :8000?</p>}
        {!error && !loading && items.length === 0 && <p className="py-16 text-center text-zinc-500">Nothing found. Try another word or category.</p>}

        <div className={`grid gap-3 sm:grid-cols-2 lg:grid-cols-3 ${loading ? 'opacity-60' : ''}`}>
          {items.map((it) => <LibraryCard key={it.slug} item={it} />)}
        </div>
      </main>
    </>
  );
}
