"""
Quick test for Terms of Service generation
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from tos_generator import generate_tos

# Test configuration
test_config = {
    "platform_type": "website",
    "website_url": "https://shopmax.com",
    "website_name": "ShopMax",
    "company_name": "ShopMax Inc",
    "company_address": "123 Commerce Street, San Francisco, CA 94102",
    "country": "United States",
    "contact_email": "legal@shopmax.com",
    "service_description": "E-commerce platform",
    "minimum_age": 18,
    "requires_account": True,
    "has_paid_services": True,
    "has_subscriptions": True,
    "has_free_trial": True,
    "offers_refunds": True,
    "refund_period": "30 days",
    "payment_processors": ["Stripe", "PayPal"],
    "allows_user_content": True,
    "user_content_types": ["reviews", "comments"],
    "moderates_content": True,
    "has_third_party_links": True,
    "provides_api": False,
    "has_mobile_app": False,
    "jurisdiction": "United States",
    "governing_state": "California",
    "has_arbitration": True,
    "disclaims_warranties": True,
}

print("Testing Terms of Service Generator...")
print("=" * 60)

# Generate ToS
tos = generate_tos(test_config, "markdown")

# Print first 2000 characters
print(tos[:2000])
print("\n... [truncated for display]")
print("=" * 60)
print(f"Total length: {len(tos)} characters")
print("ToS generation successful!")
