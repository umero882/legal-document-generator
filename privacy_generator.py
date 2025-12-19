"""
Privacy Policy Generator Module
Contains templates and logic for generating comprehensive privacy policies.
"""

from datetime import datetime
from typing import Any


def generate_policy(config: dict[str, Any], output_format: str = "markdown") -> str:
    """
    Generate a privacy policy based on the provided configuration.

    Args:
        config: Dictionary containing all privacy policy configuration
        output_format: Either 'markdown' or 'html'

    Returns:
        Generated privacy policy as a string
    """
    sections = []

    # Header
    sections.append(_generate_header(config))

    # Introduction
    sections.append(_generate_introduction(config))

    # Information We Collect
    sections.append(_generate_information_collection(config))

    # Tracking Technologies
    if _uses_tracking(config):
        sections.append(_generate_tracking_section(config))

    # Social Media Login
    if _uses_social_login(config):
        sections.append(_generate_social_login_section(config))

    # How We Use Information
    sections.append(_generate_use_of_information(config))

    # Marketing and Advertising
    if _has_marketing(config):
        sections.append(_generate_marketing_section(config))

    # Mobile App Permissions
    if config.get("platform_type") in ["app", "both"] and _has_app_permissions(config):
        sections.append(_generate_app_permissions_section(config))

    # Payment Processing
    if config.get("accepts_payments"):
        sections.append(_generate_payment_section(config))

    # Data Sharing
    sections.append(_generate_data_sharing_section(config))

    # Data Retention
    sections.append(_generate_data_retention_section(config))

    # Data Security
    sections.append(_generate_security_section(config))

    # Your Rights
    sections.append(_generate_user_rights_section(config))

    # Children's Privacy
    sections.append(_generate_children_privacy_section(config))

    # Compliance Sections
    if config.get("gdpr_compliant"):
        sections.append(_generate_gdpr_section(config))

    if config.get("ccpa_compliant"):
        sections.append(_generate_ccpa_section(config))

    if config.get("caloppa_compliant"):
        sections.append(_generate_caloppa_section(config))

    # Policy Updates
    sections.append(_generate_updates_section(config))

    # Contact Information
    sections.append(_generate_contact_section(config))

    # Combine all sections
    policy_text = "\n\n".join(sections)

    if output_format == "html":
        return _convert_to_html(policy_text, config)

    return policy_text


def _generate_header(config: dict[str, Any]) -> str:
    """Generate the policy header."""
    company = config.get("company_name") or config.get("website_name") or config.get("app_name") or "Our Company"
    date = config.get("effective_date") or datetime.now().strftime("%B %d, %Y")

    return f"""# Privacy Policy

**{company}**

**Effective Date:** {date}

**Last Updated:** {datetime.now().strftime("%B %d, %Y")}"""


def _generate_introduction(config: dict[str, Any]) -> str:
    """Generate the introduction section."""
    company = config.get("company_name") or "We"
    platform = _get_platform_text(config)

    return f"""## Introduction

{company} ("we," "us," or "our") operates {platform}. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our {_get_service_type(config)}.

Please read this Privacy Policy carefully. If you do not agree with the terms of this Privacy Policy, please do not access the {_get_service_type(config)}.

We reserve the right to make changes to this Privacy Policy at any time and for any reason. We will alert you about any changes by updating the "Last Updated" date of this Privacy Policy. You are encouraged to periodically review this Privacy Policy to stay informed of updates."""


def _generate_information_collection(config: dict[str, Any]) -> str:
    """Generate the information collection section."""
    personal_data = []

    if config.get("collects_name"):
        personal_data.append("Name and username")
    if config.get("collects_email"):
        personal_data.append("Email address")
    if config.get("collects_phone"):
        personal_data.append("Phone number")
    if config.get("collects_address"):
        personal_data.append("Mailing address")
    if config.get("collects_billing_address"):
        personal_data.append("Billing address")
    if config.get("collects_job_title"):
        personal_data.append("Job title and employer information")
    if config.get("collects_payment_info"):
        personal_data.append("Payment information (credit card numbers, billing details)")
    if config.get("collects_age"):
        personal_data.append("Age and date of birth")
    if config.get("collects_password"):
        personal_data.append("Account credentials (passwords are encrypted)")
    if config.get("collects_username"):
        personal_data.append("Username")

    personal_list = "\n".join([f"- {item}" for item in personal_data]) if personal_data else "- Basic contact information as needed"

    return f"""## Information We Collect

### Personal Data

We may collect personally identifiable information that you voluntarily provide to us when you:
- Register on our {_get_service_type(config)}
- Express interest in obtaining information about us or our products
- Participate in activities on our {_get_service_type(config)}
- Contact us

The personal information we collect may include:

{personal_list}

### Automatically Collected Information

When you access our {_get_service_type(config)}, we may automatically collect certain information, including:
- Your IP address
- Browser type and version
- Operating system
- Access times and dates
- Pages viewed and links clicked
- The page you visited before navigating to our {_get_service_type(config)}"""


def _uses_tracking(config: dict[str, Any]) -> bool:
    """Check if any tracking technologies are used."""
    return any([
        config.get("uses_cookies"),
        config.get("uses_web_beacons"),
        config.get("uses_local_storage"),
        config.get("uses_sessions"),
        config.get("uses_google_maps"),
    ])


def _generate_tracking_section(config: dict[str, Any]) -> str:
    """Generate the tracking technologies section."""
    technologies = []

    if config.get("uses_cookies"):
        technologies.append("""### Cookies

We use cookies and similar tracking technologies to track activity on our {service} and hold certain information. Cookies are files with a small amount of data that are sent to your browser from a website and stored on your device.

You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. However, if you do not accept cookies, you may not be able to use some portions of our {service}.""")

    if config.get("uses_web_beacons"):
        technologies.append("""### Web Beacons

We may use web beacons (also known as pixel tags or clear GIFs) to track user activity and gather usage data. These are tiny graphics with a unique identifier that help us understand how you interact with our {service}.""")

    if config.get("uses_local_storage"):
        technologies.append("""### Local Storage

We use local storage technologies (such as HTML5 local storage) to store content information and preferences. These are similar to cookies but can store larger amounts of data.""")

    if config.get("uses_sessions"):
        technologies.append("""### Session Data

We use session cookies and tokens to maintain your session while you use our {service}. These are temporary and are deleted when you close your browser or log out.""")

    if config.get("uses_google_maps"):
        technologies.append("""### Google Maps API

We may use Google Maps API to provide location-based features. This means Google may collect certain information about your device and location. Please refer to Google's Privacy Policy for more information about how they handle data.""")

    service = _get_service_type(config)
    content = "\n\n".join([t.format(service=service) for t in technologies])

    return f"""## Tracking Technologies

{content}"""


def _uses_social_login(config: dict[str, Any]) -> bool:
    """Check if any social login is enabled."""
    return any([
        config.get("social_login_facebook"),
        config.get("social_login_google"),
        config.get("social_login_twitter"),
        config.get("social_login_github"),
        config.get("social_login_linkedin"),
    ])


def _generate_social_login_section(config: dict[str, Any]) -> str:
    """Generate the social login section."""
    providers = []
    if config.get("social_login_facebook"):
        providers.append("Facebook")
    if config.get("social_login_google"):
        providers.append("Google")
    if config.get("social_login_twitter"):
        providers.append("Twitter/X")
    if config.get("social_login_github"):
        providers.append("GitHub")
    if config.get("social_login_linkedin"):
        providers.append("LinkedIn")

    provider_list = ", ".join(providers)

    return f"""## Social Media Login

We offer you the ability to register and login using your third-party social media account details (like {provider_list}). When you choose to do this, we will receive certain profile information about you from your social media provider.

The profile information we receive may vary depending on the social media provider concerned, but will often include:
- Your name
- Email address
- Profile picture
- Any other information you choose to make public

We will use the information we receive only for the purposes that are described in this Privacy Policy or that are otherwise made clear to you. Please note that we do not control, and are not responsible for, other uses of your personal information by your third-party social media provider. We recommend that you review their privacy policy to understand how they collect, use, and share your personal information."""


def _generate_use_of_information(config: dict[str, Any]) -> str:
    """Generate the use of information section."""
    return f"""## How We Use Your Information

We may use the information we collect about you for various purposes, including to:

- Provide, operate, and maintain our {_get_service_type(config)}
- Improve, personalize, and expand our {_get_service_type(config)}
- Understand and analyze how you use our {_get_service_type(config)}
- Develop new products, services, features, and functionality
- Communicate with you, including for customer service and support
- Send you updates and other information relating to the {_get_service_type(config)}
- Process transactions and send related information
- Find and prevent fraud
- Comply with legal obligations"""


def _has_marketing(config: dict[str, Any]) -> bool:
    """Check if marketing features are enabled."""
    return any([
        config.get("has_email_newsletter"),
        config.get("uses_analytics"),
        config.get("displays_ads"),
        config.get("uses_facebook_pixel"),
        config.get("uses_retargeting"),
    ])


def _generate_marketing_section(config: dict[str, Any]) -> str:
    """Generate the marketing section."""
    content = ["## Marketing and Advertising"]

    if config.get("has_email_newsletter"):
        content.append("""### Email Marketing

With your consent, we may send you emails about our products, services, and promotions. You can opt out of receiving marketing emails at any time by:
- Clicking the unsubscribe link in any marketing email
- Contacting us directly to request removal from our mailing list

Please note that even if you opt out of marketing emails, we may still send you transactional or administrative emails related to your account.""")

    if config.get("uses_analytics"):
        provider = config.get("analytics_provider") or "analytics tools"
        content.append(f"""### Analytics

We use {provider} to help us understand how our users engage with our {_get_service_type(config)}. This helps us improve our services and user experience. Analytics data collected may include:
- Pages visited and time spent on each page
- Links clicked
- Search queries
- Device and browser information
- Geographic location (country/city level)""")

    if config.get("displays_ads"):
        content.append("""### Advertising

We may display advertisements on our {service}. These ads may be targeted based on your interests or browsing behavior. We work with third-party advertising partners who may use cookies and similar technologies to collect information about your activities on our site and other websites.""".format(service=_get_service_type(config)))

    if config.get("uses_facebook_pixel"):
        content.append("""### Facebook Pixel

We use Facebook Pixel to measure the effectiveness of our advertising and to deliver targeted advertisements on Facebook. Facebook may collect information about your browsing behavior across websites. For more information about Facebook's data practices, please review Facebook's Data Policy.""")

    if config.get("uses_retargeting"):
        content.append("""### Retargeting

We may use retargeting technologies to serve ads to you on other websites after you have visited our {service}. This is done through cookies that track your browsing activity. You can opt out of retargeting by adjusting your browser settings or visiting industry opt-out pages.""".format(service=_get_service_type(config)))

    return "\n\n".join(content)


def _has_app_permissions(config: dict[str, Any]) -> bool:
    """Check if any app permissions are requested."""
    return any([
        config.get("requests_geolocation"),
        config.get("requests_contacts"),
        config.get("requests_camera"),
        config.get("requests_photo_gallery"),
        config.get("requests_microphone"),
        config.get("requests_push_notifications"),
    ])


def _generate_app_permissions_section(config: dict[str, Any]) -> str:
    """Generate the app permissions section."""
    permissions = []

    if config.get("requests_geolocation"):
        permissions.append("**Location Data:** We may request access to your device's location to provide location-based services and features.")

    if config.get("requests_contacts"):
        permissions.append("**Contacts:** We may request access to your contacts to help you connect with friends or share content.")

    if config.get("requests_camera"):
        permissions.append("**Camera:** We may request access to your camera to allow you to take photos or videos within the app.")

    if config.get("requests_photo_gallery"):
        permissions.append("**Photo Gallery:** We may request access to your photo gallery to allow you to upload or share images.")

    if config.get("requests_microphone"):
        permissions.append("**Microphone:** We may request access to your microphone for voice features or audio recording.")

    if config.get("requests_push_notifications"):
        permissions.append("**Push Notifications:** We may request permission to send you push notifications about updates, messages, or promotions.")

    permission_list = "\n\n".join(permissions)

    return f"""## Mobile Application Permissions

When using our mobile application, we may request certain permissions from your device:

{permission_list}

You can revoke these permissions at any time through your device settings. Please note that revoking certain permissions may limit the functionality of our app."""


def _generate_payment_section(config: dict[str, Any]) -> str:
    """Generate the payment processing section."""
    payment_type = config.get("payment_type") or "one-time and recurring"
    processors = config.get("payment_processors") or ["third-party payment processors"]
    processor_list = ", ".join(processors) if isinstance(processors, list) else processors

    return f"""## Payment Processing

We may accept {payment_type} payments for our products and services. We use {processor_list} to process payments.

### Payment Information

When you make a purchase, you may be required to provide:
- Credit or debit card information
- Billing address
- Contact information

### Security of Payment Data

We do not store your complete payment card information on our servers. Payment data is processed directly by our payment processors, who are PCI-DSS compliant. We may store:
- Last four digits of your card number
- Card type and expiration date
- Billing address
- Transaction history

### Recurring Payments

{"If you subscribe to a recurring service, your payment information will be stored by our payment processor to process future charges. You can cancel your subscription at any time through your account settings or by contacting us." if payment_type in ["recurring", "both"] else "We process one-time payments only and do not store your payment information for future transactions unless you explicitly authorize us to do so."}"""


def _generate_data_sharing_section(config: dict[str, Any]) -> str:
    """Generate the data sharing section."""
    content = ["""## Sharing Your Information

We may share your information in the following situations:"""]

    sharing_scenarios = [
        "**Service Providers:** We may share your information with third-party vendors, service providers, contractors, or agents who perform services for us.",
        "**Business Transfers:** We may share or transfer your information in connection with, or during negotiations of, any merger, sale of company assets, financing, or acquisition of all or a portion of our business.",
        "**Legal Requirements:** We may disclose your information where required to do so by law or in response to valid requests by public authorities.",
        "**Protection of Rights:** We may disclose your information to protect the rights, property, or safety of our company, our customers, or others.",
    ]

    if config.get("shares_with_third_parties"):
        categories = config.get("third_party_categories") or ["business partners"]
        category_list = ", ".join(categories) if isinstance(categories, list) else categories
        sharing_scenarios.append(f"**Third-Party Partners:** We may share your information with {category_list} for purposes described in this policy.")

    if config.get("sells_data"):
        content.append("""### Sale of Personal Information

We may sell certain categories of personal information to third parties. You have the right to opt out of the sale of your personal information. Please see the "Your Rights" section below for more information.""")
    else:
        sharing_scenarios.append("**No Sale of Data:** We do not sell your personal information to third parties.")

    scenario_list = "\n".join([f"- {s}" for s in sharing_scenarios])
    content.insert(1, scenario_list)

    return "\n\n".join(content)


def _generate_data_retention_section(config: dict[str, Any]) -> str:
    """Generate the data retention section."""
    retention = config.get("data_retention_period") or "as long as necessary to fulfill the purposes outlined in this Privacy Policy"

    return f"""## Data Retention

We will retain your personal information only for as long as is necessary for the purposes set out in this Privacy Policy. We will retain and use your information to the extent necessary to:

- Comply with our legal obligations
- Resolve disputes
- Enforce our policies
- Fulfill the purposes for which we collected the information

**Retention Period:** We retain your personal data for {retention}, unless a longer retention period is required or permitted by law.

When your personal data is no longer needed, we will securely delete or anonymize it."""


def _generate_security_section(config: dict[str, Any]) -> str:
    """Generate the security section."""
    measures = ["We use administrative, technical, and physical security measures to protect your personal information."]

    if config.get("uses_encryption"):
        measures.append("We use encryption to protect data transmitted to and from our {service}.".format(service=_get_service_type(config)))

    if config.get("uses_ssl"):
        measures.append("Our {service} uses SSL/TLS encryption to secure data transmission.".format(service=_get_service_type(config)))

    if config.get("has_security_measures"):
        measures.append("We implement industry-standard security measures including firewalls, intrusion detection systems, and regular security audits.")

    security_content = " ".join(measures)

    return f"""## Data Security

{security_content}

While we strive to use commercially acceptable means to protect your personal information, no method of transmission over the Internet or electronic storage is 100% secure. We cannot guarantee absolute security, but we are committed to protecting your information to the best of our ability.

If you have reason to believe that your interaction with us is no longer secure, please contact us immediately."""


def _generate_user_rights_section(config: dict[str, Any]) -> str:
    """Generate the user rights section."""
    rights = []

    if config.get("allows_data_access"):
        rights.append("**Right to Access:** You have the right to request copies of your personal data.")

    if config.get("allows_data_deletion"):
        rights.append("**Right to Deletion:** You have the right to request that we delete your personal data, under certain conditions.")

    if config.get("allows_data_portability"):
        rights.append("**Right to Data Portability:** You have the right to request that we transfer the data we have collected to another organization, or directly to you, under certain conditions.")

    if config.get("allows_opt_out"):
        rights.append("**Right to Opt Out:** You have the right to opt out of certain data processing activities, including marketing communications.")

    rights.extend([
        "**Right to Rectification:** You have the right to request that we correct any information you believe is inaccurate.",
        "**Right to Restrict Processing:** You have the right to request that we restrict the processing of your personal data, under certain conditions.",
    ])

    rights_list = "\n".join([f"- {r}" for r in rights])

    return f"""## Your Privacy Rights

Depending on your location, you may have certain rights regarding your personal information:

{rights_list}

### Exercising Your Rights

To exercise any of these rights, please contact us using the contact information provided below. We will respond to your request within a reasonable timeframe and in accordance with applicable law.

We may need to verify your identity before processing your request. In some cases, we may be unable to fulfill your request if it would infringe on the rights of others, if there is a legal obligation to retain the data, or if the request is unfounded or excessive."""


def _generate_children_privacy_section(config: dict[str, Any]) -> str:
    """Generate the children's privacy section."""
    if config.get("allows_children_under_13") or config.get("coppa_compliant"):
        return """## Children's Privacy

We are committed to protecting the privacy of children. Our {service} may be used by children under the age of 13 with parental consent.

### Parental Consent

If your child is under 13, we require verifiable parental consent before collecting any personal information. Parents or guardians can:
- Review their child's personal information
- Request deletion of their child's data
- Refuse to allow further collection of their child's data

### Contact for Parents

If you are a parent or guardian and believe that your child has provided us with personal information without your consent, please contact us immediately so that we can take appropriate action.

We comply with the Children's Online Privacy Protection Act (COPPA) and other applicable laws regarding children's privacy.""".format(service=_get_service_type(config))

    return """## Children's Privacy

Our {service} is not intended for children under the age of 13. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and believe that your child has provided us with personal information, please contact us immediately.

If we become aware that we have collected personal information from a child under 13 without verification of parental consent, we will take steps to remove that information from our servers.""".format(service=_get_service_type(config))


def _generate_gdpr_section(config: dict[str, Any]) -> str:
    """Generate GDPR-specific section."""
    return """## GDPR Privacy Rights (European Economic Area)

If you are a resident of the European Economic Area (EEA), you have certain data protection rights under the General Data Protection Regulation (GDPR):

### Legal Basis for Processing

We process your personal data based on one or more of the following legal grounds:
- **Consent:** You have given us permission to process your data for specific purposes
- **Contract:** Processing is necessary to fulfill a contract with you
- **Legal Obligation:** Processing is necessary to comply with the law
- **Legitimate Interests:** Processing is necessary for our legitimate interests, provided those interests are not overridden by your rights

### Your GDPR Rights

In addition to the rights listed above, under GDPR you also have:
- The right to lodge a complaint with a supervisory authority
- The right to withdraw consent at any time
- The right to object to processing based on legitimate interests
- The right not to be subject to automated decision-making

### Data Transfers

If we transfer your data outside the EEA, we ensure appropriate safeguards are in place, such as Standard Contractual Clauses approved by the European Commission.

### Data Protection Officer

For any questions about our data practices or to exercise your rights, you may contact us using the information provided below."""


def _generate_ccpa_section(config: dict[str, Any]) -> str:
    """Generate CCPA-specific section."""
    return """## CCPA Privacy Rights (California Residents)

If you are a California resident, you have specific rights under the California Consumer Privacy Act (CCPA):

### Your CCPA Rights

- **Right to Know:** You can request information about the categories and specific pieces of personal information we have collected about you
- **Right to Delete:** You can request deletion of your personal information
- **Right to Opt-Out:** You can opt out of the sale of your personal information
- **Right to Non-Discrimination:** We will not discriminate against you for exercising your CCPA rights

### Categories of Information Collected

We may collect the following categories of personal information:
- Identifiers (name, email, phone number)
- Commercial information (purchase history)
- Internet or network activity (browsing history, search history)
- Geolocation data
- Professional or employment-related information

### How to Exercise Your Rights

To exercise your CCPA rights, you can:
- Submit a request through our contact form
- Email us at the address provided below
- Call our toll-free number (if applicable)

We will verify your identity before processing your request. You may designate an authorized agent to make a request on your behalf.

### Do Not Sell My Personal Information

{"We may sell certain categories of personal information. To opt out of the sale of your personal information, please contact us or use the 'Do Not Sell My Personal Information' link on our website." if config.get("sells_data") else "We do not sell your personal information."}"""


def _generate_caloppa_section(config: dict[str, Any]) -> str:
    """Generate CalOPPA-specific section."""
    return """## CalOPPA Compliance (California Online Privacy Protection Act)

In accordance with CalOPPA, we agree to the following:

- Users can visit our {service} anonymously
- This Privacy Policy link is clearly accessible on our home page
- Our Privacy Policy link includes the word 'Privacy' and can be easily found on our website
- Users will be notified of any privacy policy changes on this Privacy Policy page
- Users can change their personal information by logging into their account or contacting us

### Do Not Track Signals

We honor Do Not Track signals. When we detect a Do Not Track signal, we will not track, plant cookies, or use advertising.""".format(service=_get_service_type(config))


def _generate_updates_section(config: dict[str, Any]) -> str:
    """Generate the policy updates section."""
    return """## Changes to This Privacy Policy

We may update our Privacy Policy from time to time. We will notify you of any changes by:
- Posting the new Privacy Policy on this page
- Updating the "Last Updated" date at the top of this Privacy Policy
- Sending you an email notification (for significant changes)

You are advised to review this Privacy Policy periodically for any changes. Changes to this Privacy Policy are effective when they are posted on this page.

Your continued use of our {service} after any modifications to this Privacy Policy constitutes your acceptance of those changes.""".format(service=_get_service_type(config))


def _generate_contact_section(config: dict[str, Any]) -> str:
    """Generate the contact information section."""
    contact_info = []

    company = config.get("company_name") or config.get("website_name") or config.get("app_name") or "Us"

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

If you have any questions about this Privacy Policy or our data practices, please contact us:

**{company}**

{contact_list}

We will respond to your inquiry as soon as possible, typically within 30 days."""


def _get_platform_text(config: dict[str, Any]) -> str:
    """Get platform description text."""
    platform = config.get("platform_type")
    website = config.get("website_url") or config.get("website_name")
    app = config.get("app_name")

    if platform == "both":
        parts = []
        if website:
            parts.append(f"the website {website}")
        if app:
            parts.append(f"the {app} mobile application")
        return " and ".join(parts) if parts else "our website and mobile application"
    elif platform == "app":
        return f"the {app} mobile application" if app else "our mobile application"
    else:
        return f"the website {website}" if website else "our website"


def _get_service_type(config: dict[str, Any]) -> str:
    """Get service type text."""
    platform = config.get("platform_type")
    if platform == "both":
        return "website and application"
    elif platform == "app":
        return "application"
    else:
        return "website"


def _convert_to_html(markdown_text: str, config: dict[str, Any]) -> str:
    """Convert markdown privacy policy to HTML."""
    company = config.get("company_name") or config.get("website_name") or config.get("app_name") or "Privacy Policy"

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

    # Convert paragraphs (lines not starting with HTML tags)
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
    <title>Privacy Policy - {company}</title>
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
