import { CATEGORY_ICON, Download, Star } from './icons';

const compact = (n) => new Intl.NumberFormat('en', { notation: 'compact', maximumFractionDigits: 1 }).format(n);

function timeAgo(iso) {
  const d = (Date.now() - new Date(iso).getTime()) / 86400000;
  if (d < 1) return 'today';
  if (d < 30) return `${Math.floor(d)} days ago`;
  if (d < 365) return `${Math.floor(d / 30)} months ago`;
  return `${Math.floor(d / 365)} years ago`;
}

/**
 * Hugging Face style card:
 *   [icon] author/name
 *   Category · Updated x ago · ↓ downloads · ★ stars
 *   summary, tags, licence
 */
export default function LibraryCard({ item, onSelect }) {
  const Icon = CATEGORY_ICON[item.category.slug] ?? CATEGORY_ICON.ai;
  const color = item.category.color;

  return (
    <article
      onClick={() => onSelect?.(item)}
      className="group relative flex cursor-pointer flex-col gap-2 overflow-hidden rounded-xl border border-zinc-200 bg-white p-3.5
                 transition hover:-translate-y-0.5 hover:border-zinc-300 hover:shadow-lg
                 dark:border-lilac/15 dark:bg-ink-900/80 dark:hover:border-lilac/40 dark:hover:shadow-glow"
    >
      {/* colour accent like HF's gradient model icons */}
      <span className="absolute inset-y-0 left-0 w-0.5 opacity-70 group-hover:opacity-100" style={{ background: color, boxShadow: `0 0 12px ${color}` }} />

      <header className="flex items-center gap-2 min-w-0">
        <span className="grid h-6 w-6 shrink-0 place-items-center rounded-md" style={{ background: `${color}22`, color }}>
          <Icon width={14} height={14} />
        </span>
        <h3 className="truncate font-mono text-[13.5px] font-medium text-zinc-900 dark:text-zinc-100">
          <span className="text-zinc-500 dark:text-zinc-400">{item.author}/</span>{item.name}
        </h3>
        {item.is_featured && <span className="ml-auto rounded bg-mint/15 px-1.5 font-mono text-[10px] text-emerald-600 dark:text-mint">featured</span>}
      </header>

      <div className="flex flex-wrap items-center gap-x-2 gap-y-1 font-mono text-[11.5px] text-zinc-500 dark:text-zinc-400">
        <span style={{ color }}>{item.category.name}</span>
        <span aria-hidden>·</span>
        <span>Updated {timeAgo(item.updated_at)}</span>
        <span aria-hidden>·</span>
        <span className="inline-flex items-center gap-1" title={`${item.downloads} downloads`}><Download width={12} height={12} />{compact(item.downloads)}</span>
        <span aria-hidden>·</span>
        <span className="inline-flex items-center gap-1" title={`${item.stars} stars`}><Star width={12} height={12} />{compact(item.stars)}</span>
      </div>

      <p className="line-clamp-2 text-[13.5px] leading-snug text-zinc-600 dark:text-zinc-300">{item.summary}</p>

      <footer className="mt-auto flex flex-wrap items-center gap-1.5 pt-1">
        {item.tags.slice(0, 4).map((t) => <span key={t} className="chip">#{t}</span>)}
        <span className="chip ml-auto border-transparent bg-zinc-100 dark:bg-white/5">{item.license}</span>
      </footer>
    </article>
  );
}
