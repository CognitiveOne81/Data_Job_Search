from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MarketplaceService:
    def __init__(self, fixture_path: Path):
        self.fixture_path = fixture_path

    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Return up to `limit` marketplace entries matching `query` from fixture data."""
        normalized_query = query.lower().strip()
        with self.fixture_path.open("r", encoding="utf-8") as f:
            items = json.load(f)

        filtered = [
            item
            for item in items
            if normalized_query in item["name"].lower() or normalized_query in item.get("description", "").lower()
        ]
        return filtered[:limit]
