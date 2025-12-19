"""
Refund Policy Generator
Generates comprehensive refund and return policies for e-commerce, SaaS, and services.
"""

from datetime import datetime
from typing import Any


def generate_refund_policy(config: dict[str, Any], output_format: str = "markdown") -> str:
    """Generate a Refund Policy document based on the provided configuration."""

    company_name = config.get("company_name") or "Company"
    website_url = config.get("website_url") or "https://example.com"
    website_name = config.get("website_name") or config.get("app_name") or "Website"
    company_address = config.get("company_address") or ""
    contact_email = config.get("contact_email") or ""
    effective_date = config.get("effective_date") or datetime.now().strftime("%B %d, %Y")

    business_type = config.get("business_type", "services")  # products, services, digital, subscription

    sections = []

    # Header
    sections.append(f"""# Refund Policy

**{company_name}**

**Effective Date:** {effective_date}

**Last Updated:** {datetime.now().strftime("%B %d, %Y")}""")

    # Introduction
    sections.append(f"""
## Introduction

Thank you for shopping at {website_name}. We appreciate your business and want to ensure your complete satisfaction.

This Refund Policy outlines the terms and conditions for refunds, returns, and exchanges. Please read this policy carefully before making a purchase. By placing an order with us, you agree to the terms of this policy.

If you have any questions about our refund policy, please contact us at {contact_email if contact_email else "[contact email]"}.""")

    # Satisfaction Guarantee (if applicable)
    if config.get("has_satisfaction_guarantee", False):
        guarantee_period = config.get("guarantee_period", "30 days")
        sections.append(f"""
## Satisfaction Guarantee

We stand behind our products/services with a {guarantee_period} satisfaction guarantee. If you are not completely satisfied with your purchase, we will work with you to make it right.

Our satisfaction guarantee means:

- Full refund if you're not satisfied within {guarantee_period}
- No questions asked returns
- Easy and hassle-free process
- Quick processing of refunds""")

    # Digital Products / Services
    if business_type in ["digital", "services", "subscription"]:
        refund_period = config.get("refund_period", "14 days")
        offers_prorated = config.get("offers_prorated_refunds", False)

        sections.append(f"""
## Refund Policy for Digital Products/Services

### Refund Eligibility

You may request a refund within **{refund_period}** of your purchase if:

- The service/product does not work as described
- You have not substantially used the service
- Technical issues prevent you from using the product
- The product was purchased by mistake (limited circumstances)

### Non-Refundable Items

The following are generally NOT eligible for refunds:

- Services that have been fully rendered or consumed
- Custom or personalized digital products
- Products purchased on sale or with promotional discounts (unless defective)
- Subscriptions after the refund period has passed
- Products where you have violated our terms of service""")

        if offers_prorated:
            sections.append("""
### Pro-Rated Refunds

For subscription services cancelled mid-cycle:

- We offer pro-rated refunds based on unused time
- The refund amount is calculated from the cancellation date
- Pro-rated refunds are processed within 5-10 business days""")

    # Physical Products
    if business_type == "products":
        return_period = config.get("return_period", "30 days")
        requires_receipt = config.get("requires_receipt", True)
        requires_original_packaging = config.get("requires_original_packaging", True)
        offers_exchanges = config.get("offers_exchanges", True)
        restocking_fee = config.get("restocking_fee")
        who_pays_return_shipping = config.get("return_shipping", "customer")

        sections.append(f"""
## Return Policy for Physical Products

### Return Window

You have **{return_period}** from the date of delivery to return eligible items for a refund or exchange.

### Return Conditions

To be eligible for a return, items must:

- Be unused and in the same condition that you received them
- Be in the original packaging{" (required)" if requires_original_packaging else " (preferred)"}
- {"Include the receipt or proof of purchase" if requires_receipt else "Have proof of purchase available upon request"}
- Not be damaged due to misuse or negligence

### Non-Returnable Items

The following items cannot be returned:

- Perishable goods (food, flowers, etc.)
- Personal care items (cosmetics, hygiene products)
- Intimate or sanitary goods
- Hazardous materials
- Custom or personalized items
- Gift cards
- Downloadable software products
- Items marked as "Final Sale" or "Non-Returnable\"""")

        if offers_exchanges:
            sections.append("""
### Exchanges

We are happy to exchange items for a different size, color, or product of equal value. To request an exchange:

1. Contact our customer service team
2. Provide your order number and the item you wish to exchange
3. Specify the replacement item you want
4. Ship the original item back to us
5. We will ship the replacement once we receive the return""")

        if restocking_fee:
            sections.append(f"""
### Restocking Fee

A restocking fee of **{restocking_fee}** may apply to:

- Items returned without original packaging
- Items returned after the standard return window (if accepted)
- Large or specialty items
- Electronics and appliances that have been opened""")

        sections.append(f"""
### Return Shipping

{"**We provide free return shipping** for defective or incorrectly shipped items." if who_pays_return_shipping == "company" else ""}
{"**Customers are responsible for return shipping costs** for standard returns." if who_pays_return_shipping == "customer" else ""}
{"**We provide prepaid return labels** for all returns." if who_pays_return_shipping == "prepaid" else ""}

Important shipping notes:

- Use a trackable shipping service
- Keep your shipping receipt as proof of return
- We recommend insuring valuable items
- We are not responsible for items lost in return transit""")

    # Subscription Refunds
    if business_type == "subscription" or config.get("has_subscriptions", False):
        subscription_refund_policy = config.get("subscription_refund_policy", "prorated")

        sections.append(f"""
## Subscription Refunds

### Cancellation Policy

You may cancel your subscription at any time through:

- Your account dashboard
- Contacting customer support
- Email request to {contact_email if contact_email else "our support team"}

### Refund Options

{"**Full Refund:** Cancel within the first billing period for a full refund." if subscription_refund_policy == "full" else ""}
{"**Pro-Rated Refund:** Receive a refund for the unused portion of your subscription." if subscription_refund_policy == "prorated" else ""}
{"**No Refund:** Subscription fees are non-refundable, but you retain access until the end of your billing period." if subscription_refund_policy == "none" else ""}

### Free Trial Conversions

If you signed up for a free trial:

- Cancel before the trial ends to avoid charges
- No refund for charges if you forget to cancel
- Set a reminder before your trial expires""")

    # How to Request a Refund
    sections.append(f"""
## How to Request a Refund

### Step-by-Step Process

1. **Contact Us**
   - Email: {contact_email if contact_email else "[support email]"}
   - Include your order number and reason for refund

2. **Provide Required Information**
   - Order number or transaction ID
   - Date of purchase
   - Reason for refund request
   - Photos of damaged items (if applicable)

3. **Wait for Confirmation**
   - We will review your request within 2-3 business days
   - You will receive an email with instructions or approval

4. **Return Items (if applicable)**
   - Ship items to the provided address
   - Include any required documentation

5. **Receive Your Refund**
   - Refunds are processed after we receive and inspect returns
   - Allow 5-10 business days for the refund to appear""")

    # Refund Processing
    refund_processing_time = config.get("refund_processing_time", "5-10 business days")

    sections.append(f"""
## Refund Processing

### Processing Time

Once your refund is approved, please allow:

- **Credit/Debit Cards:** {refund_processing_time}
- **PayPal:** 3-5 business days
- **Bank Transfer:** 5-10 business days
- **Store Credit:** Immediate

### Refund Method

Refunds will be issued to the original payment method used for the purchase unless:

- The original payment method is no longer valid
- You request store credit instead
- Local regulations require a different method

### Partial Refunds

We may issue partial refunds in cases where:

- Items are returned after the return window (at our discretion)
- Items show signs of use or damage
- Not all items from an order are returned
- Restocking fees apply""")

    # Late or Missing Refunds
    sections.append(f"""
## Late or Missing Refunds

If you haven't received your refund after the expected timeframe:

1. **Check Your Account**
   - Review your bank or credit card statement
   - Check your PayPal account (if applicable)

2. **Contact Your Bank**
   - There may be processing delays on their end
   - Some banks take additional time to post refunds

3. **Contact Your Credit Card Company**
   - Processing times vary between providers
   - Ask about their refund posting timeline

4. **Contact Us**
   - If you've completed all steps above and still haven't received your refund
   - Email us at {contact_email if contact_email else "[support email]"} with your order details
   - We will investigate and resolve the issue""")

    # Sale Items
    sale_items_policy = config.get("sale_items_refundable", True)

    sections.append(f"""
## Sale Items and Promotions

### Sale Items

{"Sale items are eligible for refunds under the same terms as regular-priced items." if sale_items_policy else "Sale items and clearance items are FINAL SALE and cannot be returned or refunded unless defective."}

### Promotional Discounts

- Items purchased with promo codes follow standard refund policies
- Refund amounts will reflect the discounted price paid
- Free promotional items must be returned with the qualifying purchase

### Bundle Deals

- Returning part of a bundle may affect the refund amount
- The full bundle discount may be deducted from partial returns
- We recommend returning the entire bundle for a full refund""")

    # Damaged or Defective Items
    sections.append(f"""
## Damaged or Defective Items

### Damaged in Shipping

If your item arrived damaged:

1. Take photos of the packaging and damage
2. Contact us within 48 hours of delivery
3. Do not discard the packaging or items
4. We will arrange a replacement or full refund

### Defective Products

If your product is defective:

1. Contact us with a description of the defect
2. Provide photos or videos if possible
3. We may request you return the item for inspection
4. We will provide a replacement, repair, or refund

### Wrong Item Received

If you received the wrong item:

1. Contact us immediately
2. Do not use or open the incorrect item
3. We will send the correct item and arrange return pickup
4. Return shipping is free for our errors""")

    # Chargebacks
    sections.append(f"""
## Chargebacks and Disputes

### Before Filing a Chargeback

Please contact us before disputing a charge with your bank or credit card company. We want to resolve any issues directly and can often do so faster than the dispute process.

### Our Commitment

- We respond to all refund requests within 48 hours
- We work to find a fair resolution for all parties
- We honor all valid refund requests within our policy

### Chargeback Consequences

Filing a chargeback without first contacting us may result in:

- Suspension of your account
- Inability to make future purchases
- Additional fees if the chargeback is found to be unwarranted""")

    # Regional Rights
    sections.append("""
## Your Legal Rights

### Consumer Protection Laws

This refund policy does not affect your statutory rights under consumer protection laws. In some jurisdictions, you may have additional rights, including:

- **European Union:** 14-day cooling-off period for online purchases
- **United Kingdom:** Consumer Rights Act protections
- **Australia:** Australian Consumer Law guarantees
- **United States:** State-specific consumer protection laws

### Right of Withdrawal (EU/UK)

If you are in the European Union or United Kingdom, you have the right to withdraw from your purchase within 14 days without giving any reason, subject to certain exceptions for:

- Digital content after download has begun
- Personalized or custom-made products
- Sealed goods unsealed after delivery""")

    # Exceptions
    sections.append("""
## Exceptions and Special Circumstances

### Force Majeure

In cases of natural disasters, pandemics, or other events beyond our control:

- Return windows may be extended
- Shipping delays will not affect your refund eligibility
- We will communicate any policy changes

### Goodwill Exceptions

At our sole discretion, we may make exceptions to this policy in special circumstances. Please contact us to discuss your situation.

### Fraud Prevention

We reserve the right to refuse refunds if we detect:

- Patterns of abuse (frequent returns, "wardrobing")
- Fraudulent claims
- Violation of our terms of service""")

    # Changes to Policy
    sections.append(f"""
## Changes to This Policy

We reserve the right to modify this refund policy at any time. Changes will be effective immediately upon posting to our website.

- The policy in effect at the time of your purchase applies to that transaction
- We will notify customers of significant changes via email
- Continued use of our services constitutes acceptance of the updated policy""")

    # Contact Information
    sections.append(f"""
## Contact Us

If you have any questions about our Refund Policy, please contact us:

**{company_name}**
{f"Address: {company_address}" if company_address else ""}
{f"Email: {contact_email}" if contact_email else ""}
{f"Website: {website_url}" if website_url else ""}

Our customer service team is available:

- Monday - Friday: 9:00 AM - 5:00 PM
- Response time: Within 24-48 hours

We value your business and will do our best to ensure your satisfaction.""")

    # Combine all sections
    content = "\n".join(sections)

    if output_format == "html":
        return convert_to_html(content, f"Refund Policy - {company_name}")

    return content


def convert_to_html(markdown_content: str, title: str) -> str:
    """Convert markdown content to HTML."""
    import re

    html_content = markdown_content

    # Convert headers
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Convert bold and italic
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)

    # Convert numbered lists
    lines = html_content.split('\n')
    in_ul = False
    in_ol = False
    result = []

    for line in lines:
        stripped = line.strip()

        # Check for numbered list
        if stripped and stripped[0].isdigit() and '. ' in stripped[:4]:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if not in_ol:
                result.append('<ol>')
                in_ol = True
            content = stripped.split('. ', 1)[1] if '. ' in stripped else stripped
            result.append(f'<li>{content}</li>')
        # Check for bullet list
        elif stripped.startswith('- '):
            if in_ol:
                result.append('</ol>')
                in_ol = False
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            result.append(f'<li>{stripped[2:]}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)

    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')

    html_content = '\n'.join(result)

    # Convert paragraphs
    html_content = re.sub(r'\n\n([^<])', r'\n\n<p>\1', html_content)
    html_content = re.sub(r'([^>])\n\n', r'\1</p>\n\n', html_content)

    # Wrap in HTML document
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #27ae60; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        h3 {{ color: #7f8c8d; margin-top: 20px; }}
        ul, ol {{ padding-left: 20px; }}
        li {{ margin: 5px 0; }}
        strong {{ color: #2c3e50; }}
        p {{ margin: 10px 0; text-align: justify; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
