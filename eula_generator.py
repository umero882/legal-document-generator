"""
EULA (End User License Agreement) Generator
Generates comprehensive EULAs for software applications, SaaS, and mobile apps.
"""

from datetime import datetime
from typing import Any


def generate_eula(config: dict[str, Any], output_format: str = "markdown") -> str:
    """Generate an EULA document based on the provided configuration."""

    company_name = config.get("company_name") or "Company"
    app_name = config.get("app_name") or config.get("website_name") or "Application"
    website_url = config.get("website_url") or "https://example.com"
    company_address = config.get("company_address") or ""
    contact_email = config.get("contact_email") or ""
    effective_date = config.get("effective_date") or datetime.now().strftime("%B %d, %Y")

    sections = []

    # Header
    sections.append(f"""# End User License Agreement (EULA)

**{company_name}**

**{app_name}**

**Effective Date:** {effective_date}

**Last Updated:** {datetime.now().strftime("%B %d, %Y")}""")

    # Introduction
    sections.append("""
## Introduction

This End User License Agreement ("Agreement" or "EULA") is a legal agreement between you ("User", "you", or "your") and {company} ("Company", "we", "us", or "our") for the use of {app} (the "Software" or "Application").

By installing, copying, or otherwise using the Software, you agree to be bound by the terms of this Agreement. If you do not agree to the terms of this Agreement, do not install or use the Software.

This Agreement applies to all versions of the Software, including any updates, upgrades, or new releases.""".format(
        company=company_name,
        app=app_name
    ))

    # License Grant
    license_type = config.get("license_type", "subscription")
    transferable = config.get("is_transferable", False)

    if license_type == "perpetual":
        license_text = "a perpetual, non-exclusive license"
    elif license_type == "subscription":
        license_text = "a limited, non-exclusive, subscription-based license"
    else:
        license_text = "a limited, non-exclusive license"

    transfer_text = "This license is transferable to another party with our prior written consent." if transferable else "This license is non-transferable and may not be assigned to any third party."

    sections.append(f"""
## License Grant

Subject to the terms and conditions of this Agreement, {company_name} hereby grants you {license_text} to:

- Install and use the Software on devices that you own or control
- Use the Software for your personal or internal business purposes
- Make a reasonable number of copies of the Software for backup purposes

{transfer_text}

This license does not include the right to sublicense the Software to third parties.""")

    # License Restrictions
    restrictions = []

    if config.get("no_reverse_engineering", True):
        restrictions.append("Reverse engineer, decompile, disassemble, or otherwise attempt to derive the source code of the Software")

    if config.get("no_modification", True):
        restrictions.append("Modify, adapt, translate, or create derivative works based on the Software")

    if config.get("no_redistribution", True):
        restrictions.append("Distribute, sublicense, lease, rent, loan, or otherwise transfer the Software to any third party")

    if config.get("no_commercial_use", False):
        restrictions.append("Use the Software for commercial purposes without obtaining a commercial license")

    restrictions.extend([
        "Remove, alter, or obscure any proprietary notices, labels, or marks on the Software",
        "Use the Software in any way that violates applicable laws or regulations",
        "Use the Software to transmit malware, viruses, or other harmful code",
        "Use the Software to infringe upon the intellectual property rights of others",
        "Use the Software to collect or harvest personal information without consent",
    ])

    restrictions_text = "\n".join([f"- {r}" for r in restrictions])

    sections.append(f"""
## License Restrictions

You agree NOT to:

{restrictions_text}

Any violation of these restrictions may result in immediate termination of this license and may expose you to civil and criminal liability.""")

    # Intellectual Property
    sections.append(f"""
## Intellectual Property Rights

The Software and all copies thereof are proprietary to {company_name} and title thereto remains exclusively with {company_name}. All rights in the Software not specifically granted in this Agreement are reserved to {company_name}.

The Software is protected by copyright laws, international treaty provisions, and other intellectual property laws. You acknowledge that the Software contains valuable trade secrets and proprietary information belonging to {company_name}.

### Ownership

- The Software, including its code, documentation, appearance, structure, and organization, is owned by {company_name}
- This Agreement does not grant you any ownership rights to the Software
- All trademarks, service marks, and trade names are the property of {company_name}

### Feedback

If you provide any feedback, suggestions, or ideas regarding the Software, you grant {company_name} a perpetual, irrevocable, royalty-free license to use such feedback for any purpose.""")

    # User Accounts
    if config.get("requires_account", False):
        sections.append(f"""
## User Accounts

### Account Creation

To access certain features of the Software, you may be required to create an account. You agree to:

- Provide accurate, current, and complete information during registration
- Maintain and promptly update your account information
- Keep your password secure and confidential
- Accept responsibility for all activities under your account
- Notify us immediately of any unauthorized use of your account

### Account Termination

We reserve the right to suspend or terminate your account at any time for:

- Violation of this Agreement
- Suspected fraudulent, abusive, or illegal activity
- Extended periods of inactivity
- Non-payment of applicable fees

Upon termination, your right to use the Software will immediately cease.""")

    # Subscription Terms
    if config.get("is_subscription", False):
        billing_cycle = config.get("billing_cycle", "monthly")
        auto_renew = config.get("auto_renewal", True)

        renewal_text = """Your subscription will automatically renew at the end of each billing period unless you cancel before the renewal date. You authorize us to charge your payment method for each renewal period.""" if auto_renew else """Your subscription will not automatically renew. You must manually renew your subscription before it expires to continue using the Software."""

        sections.append(f"""
## Subscription Terms

### Billing

- Subscription fees are billed {billing_cycle}
- All fees are non-refundable unless otherwise stated
- Prices are subject to change with reasonable notice

### Auto-Renewal

{renewal_text}

### Cancellation

You may cancel your subscription at any time through your account settings or by contacting us. Cancellation will take effect at the end of the current billing period.""")

    # Free Trial
    if config.get("has_free_trial", False):
        trial_period = config.get("trial_period", "14 days")
        sections.append(f"""
## Free Trial

We may offer a free trial period of {trial_period} for new users. During the trial:

- You will have access to the Software's features as specified
- No payment is required during the trial period
- Your trial may convert to a paid subscription automatically unless cancelled

We reserve the right to limit free trials to one per user or household.""")

    # Updates and Upgrades
    sections.append(f"""
## Updates and Upgrades

### Automatic Updates

The Software may automatically download and install updates. These updates are designed to improve, enhance, and further develop the Software and may include bug fixes, feature enhancements, or entirely new features.

### Update Terms

- Updates are provided at our sole discretion
- Some updates may be required to continue using the Software
- Major version upgrades may require additional payment
- We are not obligated to provide updates or support for older versions

### Changes to Features

We reserve the right to modify, suspend, or discontinue any feature of the Software at any time with or without notice.""")

    # Data Collection
    if config.get("collects_data", True):
        sections.append(f"""
## Data Collection and Privacy

### Information We Collect

The Software may collect certain information, including:

- Device information (hardware model, operating system, unique identifiers)
- Usage data (features used, time spent, crash reports)
- Account information (if applicable)
- Any data you choose to store or process through the Software

### Use of Data

We use collected data to:

- Provide and improve the Software
- Analyze usage patterns and trends
- Fix bugs and improve performance
- Communicate with you about updates and changes

### Privacy Policy

For complete information about our data practices, please review our Privacy Policy at {website_url}/privacy.""")

    # Third-Party Components
    if config.get("uses_third_party", True):
        sections.append("""
## Third-Party Components

### Third-Party Software

The Software may include third-party software components subject to separate license terms. Your use of such components is governed by their respective licenses.

### Third-Party Services

The Software may integrate with or provide access to third-party services. We are not responsible for:

- The availability or functionality of third-party services
- The content, policies, or practices of third-party services
- Any damages arising from your use of third-party services

Your use of third-party services is at your own risk and subject to their terms of service.""")

    # Warranty Disclaimer
    warranty_period = config.get("warranty_period")

    if warranty_period:
        sections.append(f"""
## Limited Warranty

{company_name} warrants that for a period of {warranty_period} from the date of purchase, the Software will perform substantially in accordance with its documentation.

### Warranty Remedies

If the Software does not meet this warranty, your exclusive remedy is:

- Repair or replacement of the Software, or
- A refund of the license fee paid

This warranty does not apply to issues caused by misuse, unauthorized modification, or use with incompatible systems.""")
    else:
        sections.append(f"""
## Disclaimer of Warranties

THE SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

{company_name.upper()} DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO:

- WARRANTIES OF MERCHANTABILITY
- WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE
- WARRANTIES OF NON-INFRINGEMENT
- WARRANTIES REGARDING SECURITY, RELIABILITY, OR ACCURACY

WE DO NOT WARRANT THAT:

- The Software will meet your requirements
- The Software will be uninterrupted, timely, secure, or error-free
- Any defects in the Software will be corrected
- The Software is free of viruses or other harmful components""")

    # Limitation of Liability
    liability_cap = config.get("liability_cap", "amount paid for the Software in the 12 months preceding the claim")

    sections.append(f"""
## Limitation of Liability

### Exclusion of Damages

TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT SHALL {company_name.upper()} BE LIABLE FOR ANY:

- Indirect, incidental, special, consequential, or punitive damages
- Loss of profits, revenue, data, or business opportunities
- Cost of substitute goods or services
- Damages arising from interruption of use or loss of data

### Liability Cap

{company_name.upper()}'S TOTAL LIABILITY SHALL NOT EXCEED THE {liability_cap.upper()}.

### Essential Purpose

Some jurisdictions do not allow the exclusion or limitation of certain damages. In such jurisdictions, our liability is limited to the maximum extent permitted by law.""")

    # Indemnification
    sections.append(f"""
## Indemnification

You agree to indemnify, defend, and hold harmless {company_name}, its officers, directors, employees, agents, and affiliates from and against any claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising from:

- Your use of the Software
- Your violation of this Agreement
- Your violation of any rights of another party
- Any content you submit or transmit through the Software
- Your violation of any applicable laws or regulations""")

    # Term and Termination
    sections.append(f"""
## Term and Termination

### Term

This Agreement is effective until terminated by either party.

### Termination by You

You may terminate this Agreement at any time by:

- Uninstalling and destroying all copies of the Software
- Cancelling your subscription (if applicable)
- Notifying us in writing of your intent to terminate

### Termination by Us

We may terminate this Agreement immediately if you:

- Breach any term of this Agreement
- Fail to pay applicable fees
- Use the Software in violation of applicable laws
- Engage in conduct that harms us or other users

### Effects of Termination

Upon termination:

- All rights granted to you under this Agreement cease immediately
- You must uninstall and destroy all copies of the Software
- Any data stored within the Software may be deleted
- Termination does not relieve you of payment obligations incurred before termination

### Survival

The following sections survive termination: Intellectual Property Rights, Disclaimer of Warranties, Limitation of Liability, Indemnification, and General Provisions.""")

    # Export Compliance
    if config.get("has_export_restrictions", True):
        sections.append("""
## Export Compliance

The Software may be subject to export control laws and regulations. You agree to:

- Comply with all applicable export and import laws
- Not export or re-export the Software to prohibited countries or persons
- Not use the Software for prohibited end-uses (such as nuclear, chemical, or biological weapons development)

You represent that you are not located in a country subject to embargo and are not on any prohibited party list.""")

    # Governing Law
    jurisdiction = config.get("jurisdiction", "the State of Delaware")
    dispute_resolution = config.get("dispute_resolution", "binding arbitration")

    sections.append(f"""
## Governing Law and Disputes

### Governing Law

This Agreement shall be governed by and construed in accordance with the laws of {jurisdiction}, without regard to its conflict of law provisions.

### Dispute Resolution

Any dispute arising from this Agreement shall be resolved through {dispute_resolution}.

### Class Action Waiver

You agree to resolve disputes with us on an individual basis and waive any right to participate in class action lawsuits or class-wide arbitration.

### Venue

Any legal proceedings shall be conducted in the courts located in {jurisdiction}.""")

    # General Provisions
    sections.append(f"""
## General Provisions

### Entire Agreement

This Agreement constitutes the entire agreement between you and {company_name} regarding the Software and supersedes all prior agreements and understandings.

### Severability

If any provision of this Agreement is found to be unenforceable, the remaining provisions will continue in full force and effect.

### Waiver

Our failure to enforce any right or provision of this Agreement will not be deemed a waiver of such right or provision.

### Assignment

You may not assign or transfer this Agreement without our prior written consent. We may assign this Agreement at any time without notice.

### Notices

Any notices under this Agreement shall be sent to:

**{company_name}**
{company_address if company_address else "[Company Address]"}
Email: {contact_email if contact_email else "[Contact Email]"}

### Force Majeure

We shall not be liable for any failure to perform due to causes beyond our reasonable control, including natural disasters, war, terrorism, or infrastructure failures.

### Headings

Section headings are for convenience only and do not affect the interpretation of this Agreement.""")

    # Contact Information
    sections.append(f"""
## Contact Information

If you have any questions about this Agreement, please contact us:

**{company_name}**
{f"Address: {company_address}" if company_address else ""}
{f"Email: {contact_email}" if contact_email else ""}
{f"Website: {website_url}" if website_url else ""}

---

**BY INSTALLING OR USING THE SOFTWARE, YOU ACKNOWLEDGE THAT YOU HAVE READ THIS AGREEMENT, UNDERSTAND IT, AND AGREE TO BE BOUND BY ITS TERMS AND CONDITIONS.**""")

    # Combine all sections
    content = "\n".join(sections)

    if output_format == "html":
        return convert_to_html(content, f"EULA - {app_name}")

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

    # Convert lists
    lines = html_content.split('\n')
    in_list = False
    result = []

    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)

    if in_list:
        result.append('</ul>')

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
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        h3 {{ color: #7f8c8d; margin-top: 20px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 5px 0; }}
        strong {{ color: #2c3e50; }}
        p {{ margin: 10px 0; text-align: justify; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
