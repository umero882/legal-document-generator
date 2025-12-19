"""
Terms of Service Generator Module
Contains templates and logic for generating comprehensive Terms of Service documents.
"""

from datetime import datetime
from typing import Any


def generate_tos(config: dict[str, Any], output_format: str = "markdown") -> str:
    """
    Generate Terms of Service based on the provided configuration.

    Args:
        config: Dictionary containing all ToS configuration
        output_format: Either 'markdown' or 'html'

    Returns:
        Generated Terms of Service as a string
    """
    sections = []

    # Header
    sections.append(_generate_header(config))

    # Agreement to Terms
    sections.append(_generate_agreement_section(config))

    # Definitions
    sections.append(_generate_definitions(config))

    # Account Terms
    if config.get("requires_account"):
        sections.append(_generate_account_terms(config))

    # Subscription and Payments
    if config.get("has_paid_services"):
        sections.append(_generate_payment_terms(config))

    # User Content
    if config.get("allows_user_content"):
        sections.append(_generate_user_content_section(config))

    # Acceptable Use
    sections.append(_generate_acceptable_use(config))

    # Intellectual Property
    sections.append(_generate_intellectual_property(config))

    # Third-Party Links and Services
    if config.get("has_third_party_links"):
        sections.append(_generate_third_party_section(config))

    # API Terms
    if config.get("provides_api"):
        sections.append(_generate_api_terms(config))

    # Disclaimers and Warranties
    sections.append(_generate_disclaimers(config))

    # Limitation of Liability
    sections.append(_generate_liability_limitation(config))

    # Indemnification
    sections.append(_generate_indemnification(config))

    # Termination
    sections.append(_generate_termination(config))

    # Governing Law
    sections.append(_generate_governing_law(config))

    # Dispute Resolution
    if config.get("has_arbitration") or config.get("dispute_resolution"):
        sections.append(_generate_dispute_resolution(config))

    # Changes to Terms
    sections.append(_generate_changes_section(config))

    # Severability
    sections.append(_generate_severability(config))

    # Contact Information
    sections.append(_generate_contact_section(config))

    # Combine all sections
    tos_text = "\n\n".join(sections)

    if output_format == "html":
        return _convert_to_html(tos_text, config)

    return tos_text


def _generate_header(config: dict[str, Any]) -> str:
    """Generate the ToS header."""
    company = config.get("company_name") or config.get("website_name") or config.get("app_name") or "Our Company"
    date = config.get("effective_date") or datetime.now().strftime("%B %d, %Y")

    return f"""# Terms of Service

**{company}**

**Effective Date:** {date}

**Last Updated:** {datetime.now().strftime("%B %d, %Y")}"""


def _generate_agreement_section(config: dict[str, Any]) -> str:
    """Generate the agreement to terms section."""
    company = config.get("company_name") or "We"
    service = _get_service_type(config)

    return f"""## Agreement to Terms

Welcome to {company}. These Terms of Service ("Terms", "Terms of Service") govern your use of our {service} and any related services provided by {company} (collectively, the "Service").

By accessing or using our Service, you agree to be bound by these Terms. If you disagree with any part of the terms, then you may not access the Service.

{"You must be at least " + str(config.get('minimum_age', 18)) + " years old to use this Service." if config.get('minimum_age') else "You must be at least 18 years old to use this Service. If you are under 18, you may use the Service only with the involvement of a parent or guardian."}

By using this Service, you represent and warrant that you meet all of the eligibility requirements outlined in these Terms. If you do not meet these requirements, you must not access or use the Service."""


def _generate_definitions(config: dict[str, Any]) -> str:
    """Generate definitions section."""
    company = config.get("company_name") or "Company"
    service = _get_service_type(config)

    return f"""## Definitions

For the purposes of these Terms of Service:

- **"Company"** (referred to as either "the Company", "We", "Us" or "Our" in this Agreement) refers to {company}{', located at ' + config.get('company_address') if config.get('company_address') else ''}.

- **"Service"** refers to the {service}.

- **"Terms"** (also referred to as "Terms of Service") means these Terms of Service that form the entire agreement between You and the Company regarding the use of the Service.

- **"User"**, **"You"**, and **"Your"** refers to the individual accessing or using the Service, or the company, or other legal entity on behalf of which such individual is accessing or using the Service.

- **"Account"** means a unique account created for You to access our Service or parts of our Service.

- **"Content"** refers to text, images, videos, audio, or other material that can be posted, uploaded, linked to, or otherwise made available through the Service.

- **"User Content"** means any Content that You or other users submit, post, or transmit through the Service."""


def _generate_account_terms(config: dict[str, Any]) -> str:
    """Generate account terms section."""
    return """## Account Registration and Security

### Creating an Account

To access certain features of our Service, you may be required to register for an account. When you register, you agree to:

- Provide accurate, current, and complete information during the registration process
- Maintain and promptly update your account information to keep it accurate, current, and complete
- Maintain the security and confidentiality of your login credentials
- Accept all responsibility for all activities that occur under your account
- Notify us immediately of any unauthorized use of your account or any other breach of security

### Account Responsibilities

You are responsible for:

- All activities that occur under your account
- Maintaining the confidentiality of your account password
- Restricting access to your account
- Ensuring that all use of your account complies with these Terms

### Account Termination

We reserve the right to:

- Refuse service to anyone for any reason at any time
- Terminate or suspend your account immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms
- Remove or refuse to post any User Content for any or no reason"""


def _generate_payment_terms(config: dict[str, Any]) -> str:
    """Generate payment and subscription terms."""
    sections = ["## Payments and Subscriptions"]

    sections.append("""### Fees and Payment

Certain features of the Service may be offered for a fee. Before you pay any fees, you will have an opportunity to review and accept the fees that you will be charged. All fees are in US dollars and are non-refundable unless otherwise stated.

### Payment Methods

We accept the following payment methods:""")

    processors = config.get("payment_processors") or ["major credit cards"]
    if isinstance(processors, list):
        for p in processors:
            sections.append(f"- {p}")
    else:
        sections.append(f"- {processors}")

    if config.get("has_subscriptions"):
        sections.append("""
### Subscription Terms

Some parts of the Service are billed on a subscription basis. You will be billed in advance on a recurring basis (monthly or annually, depending on your subscription plan).

**Automatic Renewal:** Your subscription will automatically renew at the end of each billing period unless you cancel it before the renewal date.

**Cancellation:** You may cancel your subscription at any time. Cancellation will take effect at the end of the current billing period. You will retain access to the Service until the end of your current billing period.

**Price Changes:** We reserve the right to modify subscription fees at any time. We will provide you with reasonable prior notice of any change in fees.""")

    if config.get("has_free_trial"):
        sections.append("""
### Free Trial

We may offer a free trial period for certain subscription plans. At the end of the free trial, you will be automatically charged for the subscription unless you cancel before the trial ends. We reserve the right to modify or cancel free trial offers at any time.""")

    if config.get("offers_refunds"):
        refund_period = config.get("refund_period") or "30 days"
        sections.append(f"""
### Refund Policy

If you are not satisfied with the Service, you may request a refund within {refund_period} of your purchase. Refund requests should be submitted to our support team. Refunds are issued at our sole discretion and may be prorated based on usage.""")
    else:
        sections.append("""
### No Refunds

All fees are non-refundable. This includes subscription fees, one-time purchases, and any other charges. By using the Service, you agree to this no-refund policy.""")

    return "\n".join(sections)


def _generate_user_content_section(config: dict[str, Any]) -> str:
    """Generate user content section."""
    return """## User Content

### Your Content

Our Service may allow you to post, link, store, share, and otherwise make available certain information, text, graphics, videos, or other material ("User Content"). You are responsible for the User Content that you post on or through the Service, including its legality, reliability, and appropriateness.

### Rights You Grant Us

By posting User Content on or through the Service, you grant us a worldwide, non-exclusive, royalty-free, sublicensable, and transferable license to use, reproduce, modify, adapt, publish, translate, create derivative works from, distribute, perform, and display such User Content in connection with operating and providing the Service.

### Content Standards

You agree that your User Content will not:

- Contain any material that is defamatory, obscene, indecent, abusive, offensive, harassing, violent, hateful, inflammatory, or otherwise objectionable
- Promote sexually explicit or pornographic material, violence, or discrimination
- Infringe any patent, trademark, trade secret, copyright, or other intellectual property rights
- Violate the legal rights (including rights of publicity and privacy) of others
- Contain any material that could give rise to criminal or civil liability
- Be likely to deceive any person
- Promote any illegal activity or advocate, promote, or assist any unlawful act
- Impersonate any person or misrepresent your identity or affiliation with any person or organization
- Involve commercial activities or sales without our prior written consent

### Content Moderation

We reserve the right, but not the obligation, to:

- Monitor User Content
- Remove or refuse to post any User Content for any or no reason
- Take any action with respect to any User Content that we deem necessary or appropriate"""


def _generate_acceptable_use(config: dict[str, Any]) -> str:
    """Generate acceptable use section."""
    return """## Acceptable Use Policy

You agree not to use the Service in any way that:

### Prohibited Activities

- Violates any applicable federal, state, local, or international law or regulation
- Exploits, harms, or attempts to exploit or harm minors in any way
- Sends, knowingly receives, uploads, downloads, uses, or re-uses any material that does not comply with these Terms
- Transmits any advertising or promotional material without our prior written consent
- Impersonates or attempts to impersonate the Company, a Company employee, another user, or any other person or entity
- Engages in any other conduct that restricts or inhibits anyone's use or enjoyment of the Service
- Uses the Service in any manner that could disable, overburden, damage, or impair the site
- Uses any robot, spider, or other automatic device, process, or means to access the Service for any purpose
- Introduces any viruses, Trojan horses, worms, logic bombs, or other malicious or technologically harmful material
- Attempts to gain unauthorized access to, interfere with, damage, or disrupt any parts of the Service

### Consequences of Violation

Violation of this Acceptable Use Policy may result in:

- Termination or suspension of your access to the Service
- Legal action against you
- Cooperation with law enforcement authorities"""


def _generate_intellectual_property(config: dict[str, Any]) -> str:
    """Generate intellectual property section."""
    company = config.get("company_name") or "the Company"

    return f"""## Intellectual Property Rights

### Our Intellectual Property

The Service and its original content (excluding User Content), features, and functionality are and will remain the exclusive property of {company} and its licensors. The Service is protected by copyright, trademark, and other laws of both the United States and foreign countries. Our trademarks and trade dress may not be used in connection with any product or service without the prior written consent of {company}.

### Copyright and Trademarks

All text, graphics, user interfaces, visual interfaces, photographs, trademarks, logos, sounds, music, artwork, and computer code (collectively, "Content"), including but not limited to the design, structure, selection, coordination, expression, and arrangement of such Content, is owned, controlled, or licensed by or to {company}, and is protected by trade dress, copyright, patent and trademark laws, and various other intellectual property rights.

### Your License to Use the Service

Subject to your compliance with these Terms, we grant you a limited, non-exclusive, non-transferable, non-sublicensable license to access and use the Service for your personal, non-commercial purposes.

### Restrictions

You may not:

- Copy, modify, or distribute the Service or any Content
- Use the Service or any Content for any commercial purpose without our express written consent
- Reverse engineer, decompile, or disassemble any software contained in the Service
- Remove any copyright, trademark, or other proprietary notices from any Content
- Transfer the Content to another person or "mirror" the Content on any other server"""


def _generate_third_party_section(config: dict[str, Any]) -> str:
    """Generate third-party links and services section."""
    return """## Third-Party Links and Services

### Third-Party Websites

Our Service may contain links to third-party websites or services that are not owned or controlled by us. We have no control over, and assume no responsibility for, the content, privacy policies, or practices of any third-party websites or services.

You acknowledge and agree that we shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with the use of or reliance on any such content, goods, or services available on or through any such websites or services.

### Third-Party Services

We may use third-party services to provide certain features of our Service. Your use of such third-party services may be subject to their own terms and conditions and privacy policies.

We strongly advise you to read the terms and conditions and privacy policies of any third-party websites or services that you visit or use."""


def _generate_api_terms(config: dict[str, Any]) -> str:
    """Generate API terms section."""
    return """## API Terms

### API Access

We may provide access to our Application Programming Interface ("API") to allow you to build applications and services that interact with our Service. Your use of the API is subject to these Terms and any additional API terms we may provide.

### API License

Subject to your compliance with these Terms, we grant you a limited, non-exclusive, non-transferable, revocable license to access and use the API solely to develop, test, and operate your applications.

### API Restrictions

When using the API, you agree not to:

- Use the API in any way that could harm the Service or impair others' use of it
- Use the API to create a product or service that competes with the Service
- Exceed any rate limits or usage restrictions we impose
- Use the API in a manner that violates any applicable laws or regulations
- Sell, lease, or sublicense access to the API

### API Changes and Discontinuation

We reserve the right to modify, suspend, or discontinue the API at any time without notice. We will not be liable to you or any third party for any modification, suspension, or discontinuation of the API."""


def _generate_disclaimers(config: dict[str, Any]) -> str:
    """Generate disclaimers and warranties section."""
    return """## Disclaimers and Warranties

### "As Is" and "As Available"

THE SERVICE IS PROVIDED ON AN "AS IS" AND "AS AVAILABLE" BASIS, WITHOUT ANY WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, OR COURSE OF PERFORMANCE.

### No Warranty

We do not warrant that:

- The Service will function uninterrupted, secure, or available at any particular time or location
- Any errors or defects will be corrected
- The Service is free of viruses or other harmful components
- The results of using the Service will meet your requirements

### Professional Advice Disclaimer

The information provided through the Service is for general informational purposes only and should not be considered professional advice. You should consult with appropriate professionals before taking any actions based on information obtained through the Service.

### Jurisdictional Limitations

Some jurisdictions do not allow the exclusion of certain warranties or the limitation or exclusion of liability for certain damages. Accordingly, some of the above limitations may not apply to you."""


def _generate_liability_limitation(config: dict[str, Any]) -> str:
    """Generate limitation of liability section."""
    company = config.get("company_name") or "THE COMPANY"

    return f"""## Limitation of Liability

### Exclusion of Damages

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL {company.upper()}, ITS AFFILIATES, DIRECTORS, EMPLOYEES, AGENTS, PARTNERS, SUPPLIERS, OR LICENSORS BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING WITHOUT LIMITATION, LOSS OF PROFITS, DATA, USE, GOODWILL, OR OTHER INTANGIBLE LOSSES, RESULTING FROM:

- Your access to or use of or inability to access or use the Service
- Any conduct or content of any third party on the Service
- Any content obtained from the Service
- Unauthorized access, use, or alteration of your transmissions or content

### Liability Cap

IN NO EVENT SHALL OUR TOTAL LIABILITY TO YOU FOR ALL DAMAGES, LOSSES, OR CAUSES OF ACTION EXCEED THE AMOUNT YOU HAVE PAID US IN THE LAST TWELVE (12) MONTHS, OR ONE HUNDRED DOLLARS ($100), WHICHEVER IS GREATER.

### Basis of the Bargain

THE LIMITATIONS OF DAMAGES SET FORTH ABOVE ARE FUNDAMENTAL ELEMENTS OF THE BASIS OF THE BARGAIN BETWEEN US AND YOU."""


def _generate_indemnification(config: dict[str, Any]) -> str:
    """Generate indemnification section."""
    company = config.get("company_name") or "the Company"

    return f"""## Indemnification

You agree to defend, indemnify, and hold harmless {company}, its affiliates, licensors, and service providers, and its and their respective officers, directors, employees, contractors, agents, licensors, suppliers, successors, and assigns from and against any claims, liabilities, damages, judgments, awards, losses, costs, expenses, or fees (including reasonable attorneys' fees) arising out of or relating to:

- Your violation of these Terms
- Your use of the Service
- Your User Content
- Your violation of any third-party rights, including intellectual property rights or privacy rights
- Any claim that your User Content caused damage to a third party

This indemnification obligation will survive the termination of these Terms and your use of the Service."""


def _generate_termination(config: dict[str, Any]) -> str:
    """Generate termination section."""
    return """## Termination

### Termination by You

You may terminate your account at any time by contacting us or using the account deletion feature in your account settings, if available.

### Termination by Us

We may terminate or suspend your account and access to the Service immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach these Terms.

### Effect of Termination

Upon termination:

- Your right to use the Service will immediately cease
- We may delete your account and all associated data
- Any provisions of these Terms which by their nature should survive termination shall survive, including ownership provisions, warranty disclaimers, indemnity, and limitations of liability

### No Refunds on Termination

If we terminate your account for breach of these Terms, you will not be entitled to any refund of fees paid."""


def _generate_governing_law(config: dict[str, Any]) -> str:
    """Generate governing law section."""
    jurisdiction = config.get("jurisdiction") or config.get("country") or "the United States"
    state = config.get("governing_state") or "California"

    return f"""## Governing Law

These Terms shall be governed and construed in accordance with the laws of {state}, {jurisdiction}, without regard to its conflict of law provisions.

Our failure to enforce any right or provision of these Terms will not be considered a waiver of those rights. If any provision of these Terms is held to be invalid or unenforceable by a court, the remaining provisions of these Terms will remain in effect.

These Terms constitute the entire agreement between us regarding our Service and supersede and replace any prior agreements we might have had between us regarding the Service."""


def _generate_dispute_resolution(config: dict[str, Any]) -> str:
    """Generate dispute resolution section."""
    sections = ["## Dispute Resolution"]

    if config.get("has_arbitration"):
        sections.append("""### Binding Arbitration

Any dispute arising out of or relating to these Terms or the Service shall be resolved by binding arbitration in accordance with the rules of the American Arbitration Association. The arbitration shall be conducted in English and the arbitrator's decision shall be final and binding.

### Class Action Waiver

YOU AND THE COMPANY AGREE THAT EACH MAY BRING CLAIMS AGAINST THE OTHER ONLY IN YOUR OR ITS INDIVIDUAL CAPACITY AND NOT AS A PLAINTIFF OR CLASS MEMBER IN ANY PURPORTED CLASS OR REPRESENTATIVE PROCEEDING.

### Exceptions to Arbitration

Notwithstanding the above, either party may seek injunctive or other equitable relief in any court of competent jurisdiction.""")
    else:
        sections.append("""### Informal Resolution

Before filing a claim, you agree to try to resolve the dispute informally by contacting us. We'll try to resolve the dispute informally by contacting you via email. If a dispute is not resolved within 30 days of submission, you or we may bring a formal proceeding.

### Judicial Forum

Any legal action or proceeding arising out of or relating to these Terms or the Service shall be instituted in the courts of the jurisdiction specified in the Governing Law section.""")

    return "\n\n".join(sections)


def _generate_changes_section(config: dict[str, Any]) -> str:
    """Generate changes to terms section."""
    return """## Changes to Terms

We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days' notice prior to any new terms taking effect. What constitutes a material change will be determined at our sole discretion.

By continuing to access or use our Service after those revisions become effective, you agree to be bound by the revised terms. If you do not agree to the new terms, please stop using the Service.

We encourage you to review these Terms periodically for any changes."""


def _generate_severability(config: dict[str, Any]) -> str:
    """Generate severability and waiver section."""
    return """## Severability and Waiver

### Severability

If any provision of these Terms is held to be unenforceable or invalid, such provision will be changed and interpreted to accomplish the objectives of such provision to the greatest extent possible under applicable law, and the remaining provisions will continue in full force and effect.

### Waiver

Our failure to exercise or enforce any right or provision of these Terms shall not operate as a waiver of such right or provision. Any waiver of any provision of these Terms will be effective only if in writing and signed by an authorized representative of the Company.

### Entire Agreement

These Terms, together with the Privacy Policy and any other legal notices published by us on the Service, shall constitute the entire agreement between you and us concerning the Service."""


def _generate_contact_section(config: dict[str, Any]) -> str:
    """Generate contact information section."""
    company = config.get("company_name") or config.get("website_name") or config.get("app_name") or "Us"
    contact_info = []

    if config.get("contact_email"):
        contact_info.append(f"**Email:** {config['contact_email']}")

    if config.get("contact_phone"):
        contact_info.append(f"**Phone:** {config['contact_phone']}")

    if config.get("company_address"):
        contact_info.append(f"**Address:** {config['company_address']}")

    if config.get("website_url"):
        contact_info.append(f"**Website:** {config['website_url']}")

    contact_list = "\n".join(contact_info) if contact_info else "Please visit our website for contact information."

    return f"""## Contact Us

If you have any questions about these Terms of Service, please contact us:

**{company}**

{contact_list}

We will respond to your inquiry as soon as possible."""


def _get_service_type(config: dict[str, Any]) -> str:
    """Get service type text."""
    platform = config.get("platform_type")
    if platform == "both":
        return "website and mobile application"
    elif platform == "app":
        return "mobile application"
    else:
        return "website"


def _convert_to_html(markdown_text: str, config: dict[str, Any]) -> str:
    """Convert markdown ToS to HTML."""
    company = config.get("company_name") or config.get("website_name") or config.get("app_name") or "Terms of Service"

    # Basic markdown to HTML conversion
    html_content = markdown_text

    # Convert headers
    import re
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Convert bold
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

    # Convert lists
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)

    # Wrap consecutive list items in ul tags
    html_content = re.sub(r'(<li>.+?</li>\n)+', lambda m: f'<ul>\n{m.group(0)}</ul>\n', html_content)

    # Convert paragraphs
    lines = html_content.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<'):
            result.append(f'<p>{line}</p>')
        else:
            result.append(line)
    html_content = '\n'.join(result)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - {company}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2a2a2a;
            margin-top: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #3a3a3a;
            margin-top: 20px;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        strong {{
            color: #1a1a1a;
        }}
        p {{
            margin-bottom: 15px;
        }}
        @media (prefers-color-scheme: dark) {{
            body {{
                background-color: #1a1a1a;
                color: #e0e0e0;
            }}
            h1, h2, h3, strong {{
                color: #fff;
            }}
            h1, h2 {{
                border-color: #444;
            }}
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
