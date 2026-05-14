#!/usr/bin/env python3
"""
Proof script: confirms every supported country returns at least one news article.

Usage:
    python prove_all_countries.py
"""

import sys
import time
from pathlib import Path

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from tidebreak import get_news_by_country
from tidebreak.country_mappings import get_all_supported_countries


def main():
    countries = sorted(get_all_supported_countries().items())
    total = len(countries)
    passed = []
    failed = []

    print(f"{'='*70}")
    print(f"  TIDEBREAK LIVE PROOF — Testing all {total} countries")
    print(f"{'='*70}\n")

    start = time.time()

    for i, (code, name) in enumerate(countries, 1):
        t0 = time.time()
        try:
            articles = get_news_by_country(code, timeout=15)
            elapsed = time.time() - t0
            count = len(articles)

            if count >= 1:
                status = f"✅ PASS"
                passed.append(code)
            else:
                status = f"❌ FAIL (0 articles)"
                failed.append((code, name, "returned 0 articles"))

            print(
                f"  [{i:>2}/{total}] {status}  {code} ({name}) — {count} article(s) in {elapsed:.1f}s"
            )
            for article in articles:
                print(f"           • {article['Title']}")

        except Exception as e:
            elapsed = time.time() - t0
            status = f"❌ FAIL"
            failed.append((code, name, str(e)[:80]))
            print(
                f"  [{i:>2}/{total}] {status}  {code} ({name}) — ERROR: {e!s:.60s} ({elapsed:.1f}s)"
            )

    total_time = time.time() - start

    # Summary
    print(f"\n{'='*70}")
    print(f"  RESULTS: {len(passed)}/{total} passed, {len(failed)}/{total} failed")
    print(f"  Total time: {total_time:.1f}s")
    print(f"{'='*70}")

    if failed:
        print(f"\n  ❌ FAILED COUNTRIES:")
        for code, name, reason in failed:
            print(f"     {code} ({name}): {reason}")
        print()
        sys.exit(1)
    else:
        print(f"\n  🎉 ALL {total} COUNTRIES SUCCESSFULLY RETURN ARTICLES\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
