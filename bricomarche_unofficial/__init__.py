"""The wood panels Bricomarché France lists, as data on furniture-design's kinds (source, clause, material, tool),
each line read as a board of wood-panels. Unofficial: Bricomarché neither wrote nor endorsed it.

What the shop lists comes from its public product sitemap (range.json, read by tools/read_range.py from the
sitemap files as fetched): every product whose title or address states a board, its line, thickness and sheet
size. Each is a clause under sources/bricomarche-sitemap. wood_panels.shops reads the titles and makes the materials:
one per line and thickness, `bricomarche-<line>-<thickness>`, its payload `shop` saying what is sold and which
board its values are.

    from furniture_design.knowledge import knowledge as general, merge
    from wood_panels import knowledge as wood_panels
    from bricomarche_unofficial import knowledge as bricomarche
    tree.root.children = merge(general(), wood_panels(), bricomarche()) + [pieces]
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from quern.tree import Node
from wood_panels import shops

HERE = Path(__file__).parent
SHOP = "Bricomarché"
PREFIX = "bricomarche"
SOURCE = "bricomarche-sitemap"


@lru_cache(maxsize=1)
def rows() -> list[dict]:
    return json.loads((HERE / "range.json").read_text(encoding="utf-8"))


SERVICE = "bricomarche-cutting-service-page"


def service_page() -> Node:
    """The page where Bricomarché describes its cutting service: what it says, by locator, in our words."""
    return Node(id=SERVICE, kind="source", name="Bricomarché France, its cutting service (https://www.bricomarche.com/services/services-sur-mesure)",
                payload={"publisher": "Bricomarché France", "year": 2026, "url": "https://www.bricomarche.com/services/services-sur-mesure", "fetched": "2026-11-14",
                         "sha256": "22d4941bed6980b1b0b55cc2f26a92ba61042ae2198c2fec7bb8be46366f0649", "licence": "copyrighted",
                         "capture": "private copy, identified by its sha256"},
                children=[Node(id="what-it-cuts", kind="clause",
                               payload={"locator": "the page's description of the service",
                                        "in_our_words": "Straight cuts of wood and glass to the customer's measures, 'selon disponibilité du service en magasin'."})])


def cutting_service() -> Node:
    """Bricomarché's cutting service as a tool a part links sawn_with: the boards it does not cut, as its page says.
    It states no cut, no depth and no narrowest part, which its page does not give."""
    refuses = []
    return Node(id="bricomarche-cutting-service", kind="tool", name="Bricomarché's cutting service",
                payload={"maker": "Bricomarché France", "saw_kind": "panel saw",
                         "does": "cuts the panels the store sells to the customer's sizes, in straight cuts",
                         "unverified": "the service and what it cuts depend on the store, its page says"},
                links={"per": [f"sources/{SERVICE}/what-it-cuts"], "refuses": refuses})


def knowledge() -> list[Node]:
    """The branches to merge beside furniture-design's and wood-panels's: the sources, the materials and the cutting service."""
    out = shops.knowledge(PREFIX, SHOP, SOURCE, "Bricomarché France, product sitemap (https://www.bricomarche.com/sitemap/sitemap.xml)",
                          "https://www.bricomarche.com/sitemap/sitemap.xml", "2026-11-14", rows())
    out[0].children.append(service_page())
    out.append(Node(id="tools", kind="", children=[cutting_service()]))
    return out
