"""
Simple JSON-based cache for Claude API responses.

Key design decisions:
    - Hash inputs (persona + email_brief + prompt_version) to create cache key
    - Store responses as JSON for human-readable inspection
    - One file per cache entry — easy to delete selectively if needed
    - No TTL by default — cache invalidates only when prompt_version bumps

This reduces cost significantly during iteration (each API call ~$0.003-0.015
depending on model). With caching, re-running the same brief is free.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Optional


class ResponseCache:
    """File-based cache for API responses."""

    def __init__(self, cache_dir: Path | str = "cache/subject_optimizer"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _make_key(self, *args: str) -> str:
        """Create a deterministic cache key from input arguments."""
        combined = "||".join(args)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16]

    def get(self, *args: str) -> Optional[Any]:
        """
        Retrieve a cached response.

        Args:
            *args: Strings to hash into a cache key (e.g., persona, brief, prompt_version)

        Returns:
            The cached response (parsed JSON) or None if not in cache.
        """
        key = self._make_key(*args)
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Corrupted cache entry, invalidate
            cache_file.unlink()
            return None

    def set(self, value: Any, *args: str) -> None:
        """
        Store a response in cache.

        Args:
            value: The data to cache (must be JSON-serializable)
            *args: Same strings used in get() — must be deterministic
        """
        key = self._make_key(*args)
        cache_file = self.cache_dir / f"{key}.json"

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, ensure_ascii=False)

    def stats(self) -> dict:
        """Return basic stats about the cache."""
        files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in files)
        return {
            "entries": len(files),
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2),
            "cache_dir": str(self.cache_dir),
        }

    def clear(self) -> int:
        """Delete all cache entries. Returns count of files removed."""
        files = list(self.cache_dir.glob("*.json"))
        for f in files:
            f.unlink()
        return len(files)
