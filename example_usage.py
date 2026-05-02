"""
Example usage of the Tidebreak news aggregation package.
"""

from tidebreak import get_news_by_country

# Example 1: Get news for the United States
print("=" * 60)
print("Example 1: Getting news for the United States")
print("=" * 60)

result = get_news_by_country("US")

print("\nCountry: United States (US)")
print(f"Articles retrieved: {len(result)}")

print("\nArticles:")
for i, article in enumerate(result, 1):
    print(f"\n{i}. {article['Title']}")
    print(f"   Link: {article['URL']}")
    print(f"   Source: {article['Source Name']}")
    print(f"   Summary: {(article['Summary'] or 'N/A')[:100]}...")

# Example 2: Get news for another country
print("\n" + "=" * 60)
print("Example 2: Getting news for the United Kingdom")
print("=" * 60)

result = get_news_by_country("GB")
print("\nCountry: United Kingdom (GB)")
print(f"Articles retrieved: {len(result)}")

for i, article in enumerate(result, 1):
    print(f"\n{i}. {article['Title']}")
    print(f"   Link: {article['URL']}")

# Example 3: Error handling - invalid country code
print("\n" + "=" * 60)
print("Example 3: Handling invalid country code")
print("=" * 60)

try:
    result = get_news_by_country("XX")
except Exception as e:
    print(f"\n✓ Caught expected error: {type(e).__name__}")
    print(f"  Message: {e}")

# Example 4: Serialize result to JSON
print("\n" + "=" * 60)
print("Example 4: Serialize to JSON")
print("=" * 60)

result = get_news_by_country("FR")

import json
print("\nJSON representation:")
print(json.dumps(result, indent=2)[:500] + "...")

