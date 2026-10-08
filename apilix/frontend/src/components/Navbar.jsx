import { Moon, Search, Sun } from './icons';

const TABS = [
  { slug: 'ai', label: 'Models/AI' },
  { slug: 'ui', label: 'UI Components' },
  { slug: 'backend', label: 'Backend/SQL' },
  { slug: 'devops', label: 'DevOps' },
];

export default function Navbar({ search, onSearch, category, onCategory, dark, onToggleDark }) {
  return (
    <nav className="sticky top-0 z-30 border-b border-zinc-200 bg-white/80 backdrop-blur-md dark:border-lilac/15 dark:bg-ink-950/80">
      <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-2.5">
        <a href="/" className="flex shrink-0 items-center gap-2 font-semibold tracking-tight">
          <span className="h-2 w-2 rounded-full bg-mint shadow-[0_0_10px_#93f9d2]" />Apilix
        </a>

        <label className="relative hidden w-72 md:block">
          <span className="sr-only">Search Apilix</span>
          <Search className="pointer-events-none absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-400" width={15} height={15} />
          <input
            value={search} onChange={(e) => onSearch(e.target.value)} placeholder="Search models, components, scripts…"
            className="w-full rounded-lg border border-zinc-200 bg-zinc-50 py-1.5 pl-8 pr-3 text-sm outline-none focus:border-lilac-600
                       dark:border-lilac/20 dark:bg-ink-900 dark:focus:border-lilac"
          />
        </label>

        <ul className="hidden items-center gap-1 text-sm lg:flex">
          {TABS.map((t) => (
            <li key={t.slug}>
              <button
                onClick={() => onCategory(category === t.slug ? '' : t.slug)}
                className={`rounded-md px-2.5 py-1.5 transition hover:bg-zinc-100 dark:hover:bg-white/5
                  ${category === t.slug ? 'font-semibold text-lilac-600 dark:text-lilac' : 'text-zinc-600 dark:text-zinc-300'}`}
              >{t.label}</button>
            </li>
          ))}
        </ul>

        <div className="ml-auto flex items-center gap-2 text-sm">
          <button onClick={onToggleDark} aria-label="Toggle dark mode" className="rounded-md p-2 hover:bg-zinc-100 dark:hover:bg-white/5">
            {dark ? <Sun /> : <Moon />}
          </button>
          <a href="/admin/" className="hidden rounded-lg bg-lilac px-3 py-1.5 font-semibold text-ink-950 shadow-glow sm:block">Submit Library</a>
          <a href="/api-auth/login/" className="rounded-md px-2 py-1.5 text-zinc-600 hover:text-zinc-900 dark:text-zinc-300 dark:hover:text-white">Log in</a>
          <a href="/admin/" className="hidden rounded-md border border-zinc-200 px-2.5 py-1.5 dark:border-lilac/20 sm:block">Sign up</a>
        </div>
      </div>
    </nav>
  );
}
