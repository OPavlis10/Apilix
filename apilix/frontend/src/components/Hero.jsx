import { Search } from './icons';

export default function Hero({ search, onSearch, categories, category, onCategory }) {
  return (
    <section className="relative overflow-hidden border-b border-zinc-200 dark:border-lilac/15">
      {/* soft glow standing in for the WebGL background of the concept site */}
      <div aria-hidden className="pointer-events-none absolute inset-0 opacity-60 dark:opacity-100"
           style={{ background: 'radial-gradient(60% 80% at 20% 0%, rgba(200,180,255,.25), transparent 60%), radial-gradient(50% 70% at 90% 20%, rgba(147,249,210,.14), transparent 60%)' }} />
      <div className="relative mx-auto max-w-7xl px-4 py-16 md:py-24">
        <p className="mb-4 font-mono text-[11px] uppercase tracking-[.22em] text-zinc-500">100% free · open source · community</p>
        <h1 className="max-w-4xl text-5xl font-semibold leading-[.95] tracking-[-.045em] md:text-7xl">
          The Open Source Ecosystem <span className="font-serif font-normal italic text-lilac-600 dark:text-lilac">for Developers</span>
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-zinc-600 dark:text-zinc-400">
          AI models, UI components, backend utilities and DevOps templates in one hub. No paid tier.
        </p>

        <label className="relative mt-8 block max-w-2xl">
          <span className="sr-only">Search the hub</span>
          <Search className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400" width={18} height={18} />
          <input
            autoFocus value={search} onChange={(e) => onSearch(e.target.value)}
            placeholder="Try “rag”, “tailwind”, “mariadb”, “nginx”…"
            className="glass w-full rounded-xl py-3.5 pl-11 pr-4 text-base outline-none focus:ring-2 focus:ring-lilac/60"
          />
        </label>

        <div className="mt-4 flex flex-wrap gap-2">
          <button onClick={() => onCategory('')}
                  className={`rounded-full border px-3 py-1 text-sm ${!category ? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-ink-950' : 'border-zinc-200 dark:border-lilac/20'}`}>
            All
          </button>
          {categories.map((c) => (
            <button key={c.slug} onClick={() => onCategory(c.slug)}
                    className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm
                      ${category === c.slug ? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-ink-950' : 'border-zinc-200 dark:border-lilac/20'}`}>
              <span className="h-2 w-2 rounded-full" style={{ background: c.color, boxShadow: `0 0 8px ${c.color}` }} />
              {c.name}<span className="font-mono text-xs opacity-60">{c.item_count}</span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
