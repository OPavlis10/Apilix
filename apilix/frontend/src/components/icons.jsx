// Small inline icons (no icon library needed).
const base = { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round' };
export const Brain = (p) => <svg {...base} {...p}><path d="M9 4a3 3 0 0 0-3 3v.5A3 3 0 0 0 4 13a3 3 0 0 0 3 4 3 3 0 0 0 5 1V5a2 2 0 0 0-3-1Z"/><path d="M15 4a3 3 0 0 1 3 3v.5a3 3 0 0 1 2 5.5 3 3 0 0 1-3 4 3 3 0 0 1-5 1"/></svg>;
export const Layout = (p) => <svg {...base} {...p}><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>;
export const Database = (p) => <svg {...base} {...p}><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>;
export const Server = (p) => <svg {...base} {...p}><rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h.01M7 16.5h.01"/></svg>;
export const Star = (p) => <svg {...base} {...p}><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z"/></svg>;
export const Download = (p) => <svg {...base} {...p}><path d="M12 4v11m0 0-4-4m4 4 4-4M5 20h14"/></svg>;
export const Search = (p) => <svg {...base} {...p}><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>;
export const Sun = (p) => <svg {...base} {...p}><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>;
export const Moon = (p) => <svg {...base} {...p}><path d="M21 13A9 9 0 1 1 11 3a7 7 0 0 0 10 10Z"/></svg>;
export const CATEGORY_ICON = { ai: Brain, ui: Layout, backend: Database, devops: Server };
