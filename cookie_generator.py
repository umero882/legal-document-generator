"""
Cookie Policy Generator Module
Contains templates and logic for generating comprehensive Cookie Policies.
"""

from datetime import datetime
from typing import Any


def generate_cookie_policy(config: dict[str, Any], output_format: str = "markdown") -> str:
    """
    Generate a Cookie Policy based on the provided configuration.

    Args:
        config: Dictionary containing all cookie policy configuration
        output_format: Either 'markdown' or 'html'

    Returns:
        Generated Cookie Policy as a string
    """
    sections = []

    # Header
    sections.append(_generate_header(config))

    # Introduction
    sections.append(_generate_introduction(config))

    # What Are Cookies
    sections.append(_generate_what_are_cookies(config))

    # How We Use Cookies
    sections.append(_generate_how_we_use_cookies(config))

    # Types of Cookies We Use
    sections.append(_generate_cookie_types(config))

    # Specific Cookies Used
    if config.get("cookie_details"):
        sections.append(_generate_cookie_details(config))

    # Third-Party Cookies
    if _has_third_party_cookies(config):
        sections.append(_generate_third_party_cookies(config))

    # Analytics Cookies
    if config.get("uses_analytics"):
        sections.append(_generate_analytics_section(config))

    # Advertising Cookies
    if config.get("uses_advertising_cookies"):
        sections.append(_generate_advertising_section(config))

    # Social Media Cookies
    if _has_social_cookies(config):
        sections.append(_generate_social_media_section(config))

    # Managing Cookies
    sections.append(_generate_managing_cookies(config))

    # Cookie Consent
    if config.get("has_cookie_consent"):
        sections.append(_generate_cookie_consent(config))

    # GDPR/EU Compliance
    if config.get("gdpr_compliant"):
        sections.append(_generate_gdpr_section(config))

    # Changes to Policy
    sections.append(_generate_changes_section(config))

    # Contact Information
    sections.append(_generate_contact_section(config))

    # Combine all sections
    policy_text = "\n\n".join(sections)

    if output_format == "html":
        return _convert_to_html(policy_text, config)

    return policy_text


def _generate_header(config: dict[str, Any]) -> str:
    """Generate the policy header."""
    company = config.get("company_name") or config.get("website_name") or "Our Company"
    date = config.get("effective_date") or datetime.now().strftime("%B %d, %Y")

    return f"""# Cookie Policy

**{company}**

**Effective Date:** {date}

**Last Updated:** {datetime.now().strftime("%B %d, %Y")}"""


def _generate_introduction(config: dict[str, Any]) -> str:
    """Generate the introduction section."""
    company = config.get("company_name") or "We"
    website = config.get("website_url") or "our website"

    return f"""## Introduction

This Cookie Policy explains how {company} ("we", "us", or "our") uses cookies and similar technologies when you visit {website}. It explains what these technologies are and why we use them, as well as your rights to control our use of them.

By using our website, you consent to the use of cookies in accordance with this Cookie Policy. If you do not agree to our use of cookies, you should set your browser settings accordingly or not use our website."""


def _generate_what_are_cookies(config: dict[str, Any]) -> str:
    """Generate the what are cookies section."""
    return """## What Are Cookies?

Cookies are small text files that are stored on your computer or mobile device when you visit a website. They are widely used to make websites work more efficiently and provide information to website owners.

Cookies can be "persistent" or "session" cookies:
- **Persistent cookies** remain on your device for a set period of time or until you delete them
- **Session cookies** are deleted when you close your web browser

Cookies can also be "first-party" or "third-party" cookies:
- **First-party cookies** are set by the website you are visiting
- **Third-party cookies** are set by a third party, such as an analytics or advertising partner

### Similar Technologies

In addition to cookies, we may use similar technologies such as:
- **Web beacons** (also known as pixel tags or clear GIFs) - Small graphic images that track user behavior
- **Local storage** - Allows websites to store data locally on your device
- **Session storage** - Similar to local storage but data is cleared when the browser session ends
- **Fingerprinting** - Collecting information about your device configuration"""


def _generate_how_we_use_cookies(config: dict[str, Any]) -> str:
    """Generate how we use cookies section."""
    purposes = []

    if config.get("uses_essential_cookies"):
        purposes.append("- **Essential operations** - To make our website function properly")

    if config.get("uses_functional_cookies"):
        purposes.append("- **Functionality** - To remember your preferences and settings")

    if config.get("uses_analytics"):
        purposes.append("- **Analytics** - To understand how visitors use our website")

    if config.get("uses_advertising_cookies"):
        purposes.append("- **Advertising** - To deliver relevant advertisements")

    if config.get("uses_social_cookies"):
        purposes.append("- **Social media** - To enable social sharing and integration")

    if config.get("uses_performance_cookies"):
        purposes.append("- **Performance** - To improve website speed and performance")

    purpose_list = "\n".join(purposes) if purposes else "- To provide and improve our services"

    return f"""## How We Use Cookies

We use cookies and similar technologies for several purposes, including:

{purpose_list}

Cookies help us:
- Keep you signed in to your account
- Remember your preferences and settings
- Understand how you use our website
- Improve your experience on our website
- Deliver content relevant to your interests
- Measure the effectiveness of our marketing campaigns"""


def _generate_cookie_types(config: dict[str, Any]) -> str:
    """Generate the types of cookies section."""
    sections = ["## Types of Cookies We Use"]

    if config.get("uses_essential_cookies"):
        sections.append("""### Essential Cookies

These cookies are necessary for the website to function properly and cannot be switched off in our systems. They are usually only set in response to actions made by you, such as:
- Setting your privacy preferences
- Logging in to your account
- Filling in forms
- Using the shopping cart

You can set your browser to block or alert you about these cookies, but some parts of the website may not work properly without them.

**Duration:** Session or up to 1 year
**Type:** First-party""")

    if config.get("uses_functional_cookies"):
        sections.append("""### Functional Cookies

These cookies enable the website to provide enhanced functionality and personalization. They may be set by us or by third-party providers whose services we have added to our pages.

Examples include:
- Remembering your language preference
- Remembering your region or location
- Remembering your display preferences (e.g., dark mode)
- Providing live chat support

If you do not allow these cookies, some or all of these features may not function properly.

**Duration:** Up to 1 year
**Type:** First-party and third-party""")

    if config.get("uses_performance_cookies"):
        sections.append("""### Performance Cookies

These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our website. They help us understand:
- Which pages are the most and least popular
- How visitors move around the site
- If users encounter error messages

All information these cookies collect is aggregated and anonymous. If you do not allow these cookies, we will not be able to monitor our website's performance.

**Duration:** Up to 2 years
**Type:** First-party and third-party""")

    if config.get("uses_analytics"):
        sections.append("""### Analytics Cookies

These cookies help us understand how visitors interact with our website by collecting and reporting information anonymously. We use this data to:
- Improve our website and services
- Understand user behavior and preferences
- Measure the effectiveness of our content

**Duration:** Up to 2 years
**Type:** First-party and third-party""")

    if config.get("uses_advertising_cookies"):
        sections.append("""### Advertising/Targeting Cookies

These cookies may be set through our website by our advertising partners. They may be used to:
- Build a profile of your interests
- Show you relevant advertisements on other websites
- Measure the effectiveness of advertising campaigns
- Limit the number of times you see an advertisement

They do not directly store personal information but are based on uniquely identifying your browser and device.

**Duration:** Up to 2 years
**Type:** Third-party""")

    if config.get("uses_social_cookies"):
        sections.append("""### Social Media Cookies

These cookies are set by social media services that we have added to the website to enable you to share our content with your friends and networks. They are capable of:
- Tracking your browser across other sites
- Building a profile of your interests
- Affecting the content and messages you see on other websites

**Duration:** Varies by platform
**Type:** Third-party""")

    return "\n\n".join(sections)


def _generate_cookie_details(config: dict[str, Any]) -> str:
    """Generate specific cookie details table."""
    cookies = config.get("cookie_details", [])

    if not cookies:
        return ""

    table = """## Specific Cookies Used

The following table lists the specific cookies used on our website:

| Cookie Name | Provider | Purpose | Duration | Type |
|-------------|----------|---------|----------|------|"""

    for cookie in cookies:
        name = cookie.get("name", "Unknown")
        provider = cookie.get("provider", "First-party")
        purpose = cookie.get("purpose", "Functionality")
        duration = cookie.get("duration", "Session")
        cookie_type = cookie.get("type", "Essential")
        table += f"\n| {name} | {provider} | {purpose} | {duration} | {cookie_type} |"

    return table


def _has_third_party_cookies(config: dict[str, Any]) -> bool:
    """Check if third-party cookies are used."""
    return any([
        config.get("uses_google_analytics"),
        config.get("uses_facebook_pixel"),
        config.get("uses_hotjar"),
        config.get("uses_hubspot"),
        config.get("uses_intercom"),
        config.get("uses_advertising_cookies"),
        config.get("third_party_cookies"),
    ])


def _generate_third_party_cookies(config: dict[str, Any]) -> str:
    """Generate third-party cookies section."""
    sections = ["## Third-Party Cookies"]

    sections.append("""We use cookies from third-party services on our website. These cookies are controlled by third parties, and you should refer to their privacy policies to understand how they use your data.

### Third-Party Services We Use""")

    services = []

    if config.get("uses_google_analytics"):
        services.append("""**Google Analytics**
- Purpose: Website analytics and performance measurement
- Privacy Policy: https://policies.google.com/privacy
- Opt-out: https://tools.google.com/dlpage/gaoptout""")

    if config.get("uses_facebook_pixel"):
        services.append("""**Facebook Pixel**
- Purpose: Advertising measurement and optimization
- Privacy Policy: https://www.facebook.com/privacy/explanation
- Opt-out: https://www.facebook.com/settings?tab=ads""")

    if config.get("uses_google_ads"):
        services.append("""**Google Ads**
- Purpose: Advertising and remarketing
- Privacy Policy: https://policies.google.com/privacy
- Opt-out: https://adssettings.google.com""")

    if config.get("uses_hotjar"):
        services.append("""**Hotjar**
- Purpose: User behavior analytics (heatmaps, recordings)
- Privacy Policy: https://www.hotjar.com/legal/policies/privacy/
- Opt-out: https://www.hotjar.com/policies/do-not-track/""")

    if config.get("uses_hubspot"):
        services.append("""**HubSpot**
- Purpose: Marketing automation and CRM
- Privacy Policy: https://legal.hubspot.com/privacy-policy""")

    if config.get("uses_intercom"):
        services.append("""**Intercom**
- Purpose: Customer messaging and support
- Privacy Policy: https://www.intercom.com/legal/privacy""")

    if config.get("uses_linkedin_insight"):
        services.append("""**LinkedIn Insight Tag**
- Purpose: Advertising and analytics
- Privacy Policy: https://www.linkedin.com/legal/privacy-policy
- Opt-out: https://www.linkedin.com/psettings/guest-controls/retargeting-opt-out""")

    if config.get("uses_twitter_pixel"):
        services.append("""**Twitter/X Pixel**
- Purpose: Advertising measurement
- Privacy Policy: https://twitter.com/en/privacy""")

    if config.get("uses_tiktok_pixel"):
        services.append("""**TikTok Pixel**
- Purpose: Advertising measurement
- Privacy Policy: https://www.tiktok.com/legal/privacy-policy""")

    if services:
        sections.append("\n\n".join(services))
    else:
        sections.append("We work with various third-party service providers. Please contact us for a complete list of third-party cookies used on our website.")

    return "\n\n".join(sections)


def _generate_analytics_section(config: dict[str, Any]) -> str:
    """Generate analytics cookies section."""
    provider = config.get("analytics_provider") or "analytics services"

    return f"""## Analytics

We use {provider} to analyze how visitors use our website. These services use cookies to collect information such as:

- How often users visit our website
- What pages they visit
- What other sites they used prior to coming to our website
- How long they spend on each page
- Technical information about their device and browser

This information is used to improve our website and understand our audience better. The data collected is aggregated and anonymous.

### Google Analytics (if applicable)

If we use Google Analytics, we have implemented the following privacy-enhancing measures:
- IP anonymization is enabled
- Data sharing with Google is limited
- Advertising features are {"enabled" if config.get("uses_advertising_cookies") else "disabled"}

You can opt out of Google Analytics by installing the Google Analytics opt-out browser add-on: https://tools.google.com/dlpage/gaoptout"""


def _generate_advertising_section(config: dict[str, Any]) -> str:
    """Generate advertising cookies section."""
    return """## Advertising and Targeting

We use advertising cookies to:
- Deliver advertisements relevant to your interests
- Limit the number of times you see an advertisement
- Measure the effectiveness of advertising campaigns
- Understand how you interact with advertisements

### How Targeted Advertising Works

When you visit our website, advertising partners may place cookies on your device to:
1. Collect information about your browsing behavior
2. Create a profile of your interests
3. Show you relevant ads on other websites you visit

### Remarketing

We may use remarketing services to show you advertisements on third-party websites after you have visited our website. This is based on cookies that track your previous visits.

### Opting Out of Targeted Advertising

You can opt out of targeted advertising through:
- **Your browser settings** - Block third-party cookies
- **Industry opt-out tools:**
  - Digital Advertising Alliance: https://optout.aboutads.info
  - Network Advertising Initiative: https://optout.networkadvertising.org
  - European Interactive Digital Advertising Alliance: https://www.youronlinechoices.eu
- **Platform-specific settings** - Adjust ad preferences on Google, Facebook, etc."""


def _has_social_cookies(config: dict[str, Any]) -> bool:
    """Check if social media cookies are used."""
    return any([
        config.get("uses_facebook_cookies"),
        config.get("uses_twitter_cookies"),
        config.get("uses_linkedin_cookies"),
        config.get("uses_instagram_cookies"),
        config.get("uses_youtube_cookies"),
        config.get("uses_social_cookies"),
        config.get("social_sharing_enabled"),
    ])


def _generate_social_media_section(config: dict[str, Any]) -> str:
    """Generate social media cookies section."""
    platforms = []

    if config.get("uses_facebook_cookies") or config.get("social_sharing_enabled"):
        platforms.append("- **Facebook** - Social sharing, like buttons, and login")

    if config.get("uses_twitter_cookies") or config.get("social_sharing_enabled"):
        platforms.append("- **Twitter/X** - Tweet buttons and embedded content")

    if config.get("uses_linkedin_cookies"):
        platforms.append("- **LinkedIn** - Share buttons and professional networking")

    if config.get("uses_instagram_cookies"):
        platforms.append("- **Instagram** - Embedded posts and sharing")

    if config.get("uses_youtube_cookies"):
        platforms.append("- **YouTube** - Embedded videos and watch history")

    if config.get("uses_pinterest_cookies"):
        platforms.append("- **Pinterest** - Pin buttons and embedded content")

    platform_list = "\n".join(platforms) if platforms else "- Various social media platforms"

    return f"""## Social Media Cookies

We integrate with social media platforms to allow you to share our content and connect with us. These platforms may set cookies when you:
- Use social sharing buttons on our website
- Log in using social media credentials
- View embedded social media content

### Platforms We Integrate With

{platform_list}

### What These Cookies Do

Social media cookies allow the respective platforms to:
- Recognize that you have an account with them
- Track your browsing activity across websites
- Personalize advertisements shown to you
- Measure the effectiveness of their advertising

### Managing Social Media Cookies

To control social media cookies, you should adjust your privacy settings directly on each platform:
- Facebook: https://www.facebook.com/settings?tab=privacy
- Twitter: https://twitter.com/settings/privacy
- LinkedIn: https://www.linkedin.com/psettings/
- Google: https://myaccount.google.com/privacy"""


def _generate_managing_cookies(config: dict[str, Any]) -> str:
    """Generate managing cookies section."""
    return """## Managing Cookies

You have the right to decide whether to accept or reject cookies. You can manage your cookie preferences in several ways:

### Browser Settings

Most web browsers allow you to control cookies through their settings. You can:
- **View cookies** stored on your device
- **Delete cookies** individually or all at once
- **Block cookies** from being set
- **Allow cookies** from specific websites only

Here's how to manage cookies in popular browsers:
- **Chrome**: Settings > Privacy and Security > Cookies
- **Firefox**: Options > Privacy & Security > Cookies
- **Safari**: Preferences > Privacy > Cookies
- **Edge**: Settings > Privacy & Security > Cookies

### Cookie Consent Tool

{"We provide a cookie consent banner when you first visit our website. You can change your preferences at any time by clicking the 'Cookie Settings' link in the footer of our website." if config.get("has_cookie_consent") else "You can manage cookies through your browser settings."}

### Do Not Track

Some browsers have a "Do Not Track" feature that signals to websites that you do not want to be tracked. {"We honor Do Not Track signals." if config.get("honors_dnt") else "Please note that we may not respond to Do Not Track signals, but you can still manage cookies through other methods."}

### Impact of Disabling Cookies

If you choose to disable cookies, please be aware that:
- Some features of our website may not function properly
- You may not be able to stay logged in to your account
- Your preferences may not be remembered
- You may still see advertisements, but they will be less relevant"""


def _generate_cookie_consent(config: dict[str, Any]) -> str:
    """Generate cookie consent section."""
    return """## Cookie Consent

When you first visit our website, we display a cookie consent banner that allows you to:
- **Accept all cookies** - Allow all types of cookies
- **Reject non-essential cookies** - Only allow essential cookies
- **Customize preferences** - Choose which categories of cookies to allow

### Your Consent Choices

Your consent choices are stored in a cookie on your device. If you clear your cookies, you will be asked for consent again on your next visit.

### Withdrawing Consent

You can withdraw your consent at any time by:
- Clicking the "Cookie Settings" link in our website footer
- Clearing cookies from your browser
- Contacting us to request that we delete your data

### Consent for Children

{"We do not knowingly collect data from children under 13. If you believe a child has provided consent, please contact us." if not config.get("allows_children") else "Our website may be used by children with parental consent. Parents can manage cookie preferences on behalf of their children."}"""


def _generate_gdpr_section(config: dict[str, Any]) -> str:
    """Generate GDPR compliance section."""
    return """## EU/GDPR Cookie Compliance

If you are located in the European Economic Area (EEA), United Kingdom, or Switzerland, you have specific rights regarding cookies under the General Data Protection Regulation (GDPR) and ePrivacy Directive.

### Legal Basis for Cookies

We use cookies based on the following legal grounds:
- **Consent** - For non-essential cookies (analytics, advertising, etc.)
- **Legitimate interest** - For essential cookies required for website functionality

### Your Rights

Under GDPR, you have the right to:
- **Be informed** - Know what cookies we use and why
- **Give or withdraw consent** - Choose which non-essential cookies to allow
- **Access** - Request information about cookies that identify you
- **Erasure** - Request deletion of cookie data we hold about you

### Cookie Consent Requirements

In accordance with EU law:
- We obtain consent before placing non-essential cookies
- Consent is freely given, specific, informed, and unambiguous
- You can withdraw consent as easily as you gave it
- We do not use pre-ticked consent boxes

### Contact Your Data Protection Authority

If you have concerns about our use of cookies, you can contact your local data protection authority. A list of EU data protection authorities is available at: https://edpb.europa.eu/about-edpb/about-edpb/members_en"""


def _generate_changes_section(config: dict[str, Any]) -> str:
    """Generate changes to policy section."""
    return """## Changes to This Cookie Policy

We may update this Cookie Policy from time to time to reflect:
- Changes in the cookies we use
- Changes in applicable laws or regulations
- Changes in our data practices

When we make changes, we will:
- Update the "Last Updated" date at the top of this policy
- Post a notice on our website for significant changes
- Obtain new consent if required by law

We encourage you to review this Cookie Policy periodically to stay informed about our use of cookies."""


def _generate_contact_section(config: dict[str, Any]) -> str:
    """Generate contact information section."""
    company = config.get("company_name") or config.get("website_name") or "Us"
    contact_info = []

    if config.get("contact_email"):
        contact_info.append(f"**Email:** {config['contact_email']}")

    if config.get("privacy_email"):
        contact_info.append(f"**Privacy Email:** {config['privacy_email']}")

    if config.get("company_address"):
        contact_info.append(f"**Address:** {config['company_address']}")

    if config.get("website_url"):
        contact_info.append(f"**Website:** {config['website_url']}")

    contact_list = "\n".join(contact_info) if contact_info else "Please visit our website for contact information."

    return f"""## Contact Us

If you have any questions about this Cookie Policy or our use of cookies, please contact us:

**{company}**

{contact_list}

For privacy-related inquiries, you can also refer to our Privacy Policy for more information about how we handle your personal data."""


def _convert_to_html(markdown_text: str, config: dict[str, Any]) -> str:
    """Convert markdown cookie policy to HTML."""
    company = config.get("company_name") or config.get("website_name") or "Cookie Policy"

    import re
    html_content = markdown_text

    # Convert headers
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Convert bold
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

    # Convert lists
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)

    # Wrap consecutive list items
    html_content = re.sub(r'(<li>.+?</li>\n)+', lambda m: f'<ul>\n{m.group(0)}</ul>\n', html_content)

    # Convert tables
    html_content = re.sub(r'\|(.+)\|', lambda m: '<tr><td>' + '</td><td>'.join(m.group(1).split('|')) + '</td></tr>', html_content)

    # Convert paragraphs
    lines = html_content.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<') and not line.startswith('|'):
            result.append(f'<p>{line}</p>')
        else:
            result.append(line)
    html_content = '\n'.join(result)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cookie Policy - {company}</title>
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
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
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
            th {{
                background-color: #333;
            }}
            th, td {{
                border-color: #444;
            }}
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
