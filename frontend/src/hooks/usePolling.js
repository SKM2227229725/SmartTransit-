import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Polls an async function every `interval` ms.
 * Returns { data, loading, error, refetch }.
 * `data` is always an array (never null) for list-style APIs.
 */
export function usePolling(fetcher, { interval = 5000, enabled = true } = {}) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const savedFetcher = useRef(fetcher);

  useEffect(() => {
    savedFetcher.current = fetcher;
  }, [fetcher]);

  const run = useCallback(async () => {
    try {
      setLoading(true);
      const result = await savedFetcher.current();
      setData(Array.isArray(result) ? result : []);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    let timer;

    const tick = async () => {
      if (cancelled) return;
      await run();
      if (!cancelled) timer = setTimeout(tick, interval);
    };

    tick();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [enabled, interval, run]);

  return { data, loading, error, refetch: run };
}