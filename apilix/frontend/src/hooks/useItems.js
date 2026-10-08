import { useEffect, useState } from 'react';
import { fetchItems } from '../api';

/** Real-time search: debounces the query and cancels the previous request. */
export default function useItems(query, delay = 250) {
  const [state, setState] = useState({ items: [], count: 0, loading: true, error: null });

  useEffect(() => {
    const ctrl = new AbortController();
    setState((s) => ({ ...s, loading: true }));
    const t = setTimeout(() => {
      fetchItems(query, ctrl.signal)
        .then((d) => setState({ items: d.results, count: d.count, loading: false, error: null }))
        .catch((e) => { if (e.name !== 'AbortError') setState({ items: [], count: 0, loading: false, error: e.message }); });
    }, delay);
    return () => { clearTimeout(t); ctrl.abort(); };
  }, [query.search, query.category, query.tag, query.ordering, delay]);

  return state;
}
