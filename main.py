"""
Legal Document Generator Agent
A full-featured agent that generates comprehensive Privacy Policies, Terms of Service,
and Cookie Policies. Similar to Termify.io's generators.
"""

import asyncio
import os
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Any

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'buffer') and sys.stdout.buffer is not None:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'buffer') and sys.stderr.buffer is not None:
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # Skip encoding wrapper if it fails

from dotenv import load_dotenv
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)

# Load environment variables
load_dotenv()

# Privacy policy configuration storage
policy_config: dict[str, Any] = {
    # Business Information
    "platform_type": None,  # "website", "app", "both"
    "website_url": None,
    "website_name": None,
    "app_name": None,
    "business_type": None,  # "business", "individual"
    "company_name": None,
    "company_address": None,
    "country": None,
    "effective_date": None,
    "contact_email": None,
    "contact_phone": None,
    "contact_address": None,

    # Data Collection - Personal Information
    "collects_name": False,
    "collects_email": False,
    "collects_phone": False,
    "collects_address": False,
    "collects_billing_address": False,
    "collects_job_title": False,
    "collects_payment_info": False,
    "collects_age": False,
    "collects_password": False,
    "collects_username": False,

    # Tracking Technologies
    "uses_cookies": False,
    "uses_web_beacons": False,
    "uses_local_storage": False,
    "uses_sessions": False,
    "uses_google_maps": False,

    # Social Media Login
    "social_login_facebook": False,
    "social_login_google": False,
    "social_login_twitter": False,
    "social_login_github": False,
    "social_login_linkedin": False,

    # Marketing & Advertising
    "has_email_newsletter": False,
    "uses_analytics": False,
    "analytics_provider": None,  # e.g., "Google Analytics"
    "displays_ads": False,
    "uses_facebook_pixel": False,
    "uses_retargeting": False,

    # Mobile App Permissions
    "requests_geolocation": False,
    "requests_contacts": False,
    "requests_camera": False,
    "requests_photo_gallery": False,
    "requests_microphone": False,
    "requests_push_notifications": False,

    # Payment Processing
    "accepts_payments": False,
    "payment_type": None,  # "one_time", "recurring", "both"
    "payment_processors": [],  # e.g., ["Stripe", "PayPal"]

    # Compliance
    "gdpr_compliant": False,
    "ccpa_compliant": False,
    "caloppa_compliant": False,
    "coppa_compliant": False,  # Children's privacy
    "allows_children_under_13": False,

    # Data Sharing
    "shares_with_third_parties": False,
    "third_party_categories": [],
    "sells_data": False,

    # User Rights
    "allows_data_access": True,
    "allows_data_deletion": True,
    "allows_data_portability": False,
    "allows_opt_out": True,

    # Data Retention
    "data_retention_period": None,  # e.g., "2 years", "until account deletion"

    # Security
    "uses_encryption": False,
    "uses_ssl": False,
    "has_security_measures": False,
}

# Terms of Service configuration storage
tos_config: dict[str, Any] = {
    # Business Information (shared with privacy policy)
    "platform_type": None,
    "website_url": None,
    "website_name": None,
    "app_name": None,
    "company_name": None,
    "company_address": None,
    "country": None,
    "contact_email": None,
    "effective_date": None,

    # Service Details
    "service_description": None,
    "minimum_age": 18,
    "requires_account": False,

    # Payment and Subscriptions
    "has_paid_services": False,
    "has_subscriptions": False,
    "has_free_trial": False,
    "offers_refunds": False,
    "refund_period": None,
    "payment_processors": [],

    # User Content
    "allows_user_content": False,
    "user_content_types": [],  # e.g., ["text", "images", "videos"]
    "moderates_content": False,

    # Features
    "has_third_party_links": False,
    "provides_api": False,
    "has_mobile_app": False,

    # Legal
    "jurisdiction": None,
    "governing_state": None,
    "has_arbitration": False,
    "dispute_resolution": None,

    # Liability
    "liability_cap": None,
    "disclaims_warranties": True,
}

# Cookie Policy configuration storage
cookie_config: dict[str, Any] = {
    # Business Information (shared)
    "company_name": None,
    "website_url": None,
    "website_name": None,
    "company_address": None,
    "contact_email": None,
    "privacy_email": None,

    # Cookie Types Used
    "uses_essential_cookies": True,
    "uses_functional_cookies": False,
    "uses_performance_cookies": False,
    "uses_analytics": False,
    "uses_advertising_cookies": False,
    "uses_social_cookies": False,

    # Analytics Providers
    "uses_google_analytics": False,
    "uses_hotjar": False,
    "uses_mixpanel": False,
    "analytics_provider": None,

    # Advertising/Marketing
    "uses_facebook_pixel": False,
    "uses_google_ads": False,
    "uses_linkedin_insight": False,
    "uses_twitter_pixel": False,
    "uses_tiktok_pixel": False,

    # Social Media
    "uses_facebook_cookies": False,
    "uses_twitter_cookies": False,
    "uses_linkedin_cookies": False,
    "uses_instagram_cookies": False,
    "uses_youtube_cookies": False,
    "uses_pinterest_cookies": False,
    "social_sharing_enabled": False,

    # Third-Party Services
    "uses_hubspot": False,
    "uses_intercom": False,
    "third_party_cookies": [],

    # Cookie Details (optional list of specific cookies)
    "cookie_details": [],

    # Consent & Compliance
    "has_cookie_consent": True,
    "honors_dnt": False,
    "gdpr_compliant": False,
    "allows_children": False,
}

# EULA configuration storage
eula_config: dict[str, Any] = {
    # Business Information (shared)
    "company_name": None,
    "website_url": None,
    "website_name": None,
    "app_name": None,
    "company_address": None,
    "contact_email": None,

    # License Terms
    "license_type": "subscription",  # perpetual, subscription, freemium
    "is_transferable": False,
    "is_subscription": True,
    "billing_cycle": "monthly",
    "auto_renewal": True,
    "has_free_trial": False,
    "trial_period": "14 days",

    # Restrictions
    "no_reverse_engineering": True,
    "no_modification": True,
    "no_redistribution": True,
    "no_commercial_use": False,

    # Features
    "requires_account": True,
    "collects_data": True,
    "uses_third_party": True,
    "has_export_restrictions": True,

    # Warranty & Liability
    "has_warranty": False,
    "warranty_period": None,
    "liability_cap": "amount paid for the Software in the 12 months preceding the claim",

    # Legal
    "jurisdiction": "the State of Delaware",
    "dispute_resolution": "binding arbitration",
}

# Refund Policy configuration storage
refund_config: dict[str, Any] = {
    # Business Information (shared)
    "company_name": None,
    "website_url": None,
    "website_name": None,
    "company_address": None,
    "contact_email": None,

    # Business Type
    "business_type": "services",  # products, services, digital, subscription

    # General Refund Settings
    "has_satisfaction_guarantee": False,
    "guarantee_period": "30 days",
    "refund_period": "14 days",
    "refund_processing_time": "5-10 business days",

    # Physical Products
    "return_period": "30 days",
    "requires_receipt": True,
    "requires_original_packaging": True,
    "offers_exchanges": True,
    "restocking_fee": None,
    "return_shipping": "customer",  # customer, company, prepaid

    # Digital/Subscription
    "has_subscriptions": False,
    "subscription_refund_policy": "prorated",  # full, prorated, none
    "offers_prorated_refunds": True,

    # Sale Items
    "sale_items_refundable": True,
}


# ============================================================================
# PRIVACY POLICY TOOLS
# ============================================================================

@tool(
    "set_business_info",
    "Set core business information for all legal documents",
    {
        "platform_type": str,
        "business_type": str,
        "company_name": str,
        "country": str,
        "website_url": str,
        "website_name": str,
        "app_name": str,
        "company_address": str,
        "contact_email": str,
    }
)
async def set_business_info(args: dict[str, Any]) -> dict[str, Any]:
    """Set business information for all configs."""
    for key in ["platform_type", "business_type", "company_name", "country",
                "website_url", "website_name", "app_name", "company_address", "contact_email"]:
        if key in args and args[key]:
            policy_config[key] = args[key]
            if key in tos_config:
                tos_config[key] = args[key]
            if key in cookie_config:
                cookie_config[key] = args[key]
            if key in eula_config:
                eula_config[key] = args[key]
            if key in refund_config:
                refund_config[key] = args[key]

    return {
        "content": [{
            "type": "text",
            "text": f"Business information saved: {args.get('company_name', 'N/A')} ({args.get('platform_type', 'N/A')})"
        }]
    }


@tool(
    "set_data_collection",
    "Configure what personal data is collected",
    {
        "collects_name": bool,
        "collects_email": bool,
        "collects_phone": bool,
        "collects_address": bool,
        "collects_billing_address": bool,
        "collects_payment_info": bool,
        "collects_age": bool,
        "collects_username": bool,
        "collects_password": bool,
    }
)
async def set_data_collection(args: dict[str, Any]) -> dict[str, Any]:
    """Set data collection preferences."""
    for key, value in args.items():
        if key in policy_config:
            policy_config[key] = value

    collected = [k.replace("collects_", "") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"Data collection configured. Collecting: {', '.join(collected) if collected else 'None specified'}"
        }]
    }


@tool(
    "set_tracking_technologies",
    "Configure tracking technologies used",
    {
        "uses_cookies": bool,
        "uses_web_beacons": bool,
        "uses_local_storage": bool,
        "uses_sessions": bool,
        "uses_google_maps": bool,
    }
)
async def set_tracking_technologies(args: dict[str, Any]) -> dict[str, Any]:
    """Set tracking technologies."""
    for key, value in args.items():
        if key in policy_config:
            policy_config[key] = value

    used = [k.replace("uses_", "") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"Tracking technologies configured: {', '.join(used) if used else 'None'}"
        }]
    }


@tool(
    "set_social_logins",
    "Configure social media login options",
    {
        "facebook": bool,
        "google": bool,
        "twitter": bool,
        "github": bool,
        "linkedin": bool,
    }
)
async def set_social_logins(args: dict[str, Any]) -> dict[str, Any]:
    """Set social login options."""
    mapping = {
        "facebook": "social_login_facebook",
        "google": "social_login_google",
        "twitter": "social_login_twitter",
        "github": "social_login_github",
        "linkedin": "social_login_linkedin",
    }
    for key, config_key in mapping.items():
        if key in args:
            policy_config[config_key] = args[key]

    enabled = [k for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"Social logins configured: {', '.join(enabled) if enabled else 'None'}"
        }]
    }


@tool(
    "set_marketing_settings",
    "Configure marketing and advertising settings",
    {
        "has_email_newsletter": bool,
        "uses_analytics": bool,
        "analytics_provider": str,
        "displays_ads": bool,
        "uses_facebook_pixel": bool,
        "uses_retargeting": bool,
    }
)
async def set_marketing_settings(args: dict[str, Any]) -> dict[str, Any]:
    """Set marketing settings."""
    for key, value in args.items():
        if key in policy_config:
            policy_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Marketing settings configured. Analytics: {args.get('analytics_provider', 'None')}"
        }]
    }


@tool(
    "set_app_permissions",
    "Configure mobile app permissions (for apps)",
    {
        "requests_geolocation": bool,
        "requests_contacts": bool,
        "requests_camera": bool,
        "requests_photo_gallery": bool,
        "requests_microphone": bool,
        "requests_push_notifications": bool,
    }
)
async def set_app_permissions(args: dict[str, Any]) -> dict[str, Any]:
    """Set app permissions."""
    for key, value in args.items():
        if key in policy_config:
            policy_config[key] = value

    requested = [k.replace("requests_", "") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"App permissions configured: {', '.join(requested) if requested else 'None'}"
        }]
    }


@tool(
    "set_payment_settings",
    "Configure payment processing settings for privacy policy",
    {
        "accepts_payments": bool,
        "payment_type": str,
        "payment_processors": str,
    }
)
async def set_payment_settings(args: dict[str, Any]) -> dict[str, Any]:
    """Set payment settings."""
    policy_config["accepts_payments"] = args.get("accepts_payments", False)
    policy_config["payment_type"] = args.get("payment_type")
    if args.get("payment_processors"):
        processors = [p.strip() for p in args["payment_processors"].split(",")]
        policy_config["payment_processors"] = processors
        tos_config["payment_processors"] = processors

    return {
        "content": [{
            "type": "text",
            "text": f"Payment settings configured. Processors: {args.get('payment_processors', 'None')}"
        }]
    }


@tool(
    "set_compliance_options",
    "Configure regulatory compliance options",
    {
        "gdpr_compliant": bool,
        "ccpa_compliant": bool,
        "caloppa_compliant": bool,
        "coppa_compliant": bool,
        "allows_children_under_13": bool,
    }
)
async def set_compliance_options(args: dict[str, Any]) -> dict[str, Any]:
    """Set compliance options."""
    for key, value in args.items():
        if key in policy_config:
            policy_config[key] = value

    compliant = []
    if args.get("gdpr_compliant"):
        compliant.append("GDPR")
    if args.get("ccpa_compliant"):
        compliant.append("CCPA")
    if args.get("caloppa_compliant"):
        compliant.append("CalOPPA")
    if args.get("coppa_compliant"):
        compliant.append("COPPA")

    return {
        "content": [{
            "type": "text",
            "text": f"Compliance configured: {', '.join(compliant) if compliant else 'None specified'}"
        }]
    }


@tool(
    "set_data_sharing",
    "Configure data sharing and third-party settings",
    {
        "shares_with_third_parties": bool,
        "third_party_categories": str,
        "sells_data": bool,
    }
)
async def set_data_sharing(args: dict[str, Any]) -> dict[str, Any]:
    """Set data sharing preferences."""
    policy_config["shares_with_third_parties"] = args.get("shares_with_third_parties", False)
    policy_config["sells_data"] = args.get("sells_data", False)
    if args.get("third_party_categories"):
        policy_config["third_party_categories"] = [c.strip() for c in args["third_party_categories"].split(",")]

    return {
        "content": [{
            "type": "text",
            "text": f"Data sharing configured. Shares with third parties: {args.get('shares_with_third_parties', False)}"
        }]
    }


@tool(
    "set_user_rights",
    "Configure user rights and data control options",
    {
        "allows_data_access": bool,
        "allows_data_deletion": bool,
        "allows_data_portability": bool,
        "allows_opt_out": bool,
    }
)
async def set_user_rights(args: dict[str, Any]) -> dict[str, Any]:
    """Set user rights."""
    for key, value in args.items():
        if key in policy_config:
            policy_config[key] = value

    rights = [k.replace("allows_", "") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"User rights configured: {', '.join(rights) if rights else 'None'}"
        }]
    }


@tool(
    "set_security_settings",
    "Configure security and data retention settings",
    {
        "uses_encryption": bool,
        "uses_ssl": bool,
        "has_security_measures": bool,
        "data_retention_period": str,
    }
)
async def set_security_settings(args: dict[str, Any]) -> dict[str, Any]:
    """Set security settings."""
    for key, value in args.items():
        if key in policy_config:
            policy_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Security settings configured. Retention: {args.get('data_retention_period', 'Not specified')}"
        }]
    }


@tool(
    "get_current_config",
    "Get the current configuration for all documents",
    {}
)
async def get_current_config(args: dict[str, Any]) -> dict[str, Any]:
    """Get current configuration."""
    import json
    return {
        "content": [{
            "type": "text",
            "text": f"Privacy Policy Config:\n{json.dumps(policy_config, indent=2)}\n\nToS Config:\n{json.dumps(tos_config, indent=2)}\n\nCookie Policy Config:\n{json.dumps(cookie_config, indent=2)}\n\nEULA Config:\n{json.dumps(eula_config, indent=2)}\n\nRefund Policy Config:\n{json.dumps(refund_config, indent=2)}"
        }]
    }


@tool(
    "generate_privacy_policy",
    "Generate the final privacy policy document based on collected configuration",
    {
        "output_format": str,
    }
)
async def generate_privacy_policy(args: dict[str, Any]) -> dict[str, Any]:
    """Generate the privacy policy document."""
    from privacy_generator import generate_policy

    output_format = args.get("output_format", "markdown")
    policy_text = generate_policy(policy_config, output_format)

    # Save to file
    output_dir = Path("generated_policies")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (policy_config.get("company_name") or "policy").lower().replace(" ", "_")

    if output_format == "html":
        filename = f"{company_slug}_privacy_policy_{timestamp}.html"
    else:
        filename = f"{company_slug}_privacy_policy_{timestamp}.md"

    output_path = output_dir / filename
    output_path.write_text(policy_text, encoding="utf-8")

    return {
        "content": [{
            "type": "text",
            "text": f"Privacy policy generated and saved to: {output_path}\n\n{policy_text}"
        }]
    }


@tool(
    "reset_config",
    "Reset all configurations to start over",
    {}
)
async def reset_config(args: dict[str, Any]) -> dict[str, Any]:
    """Reset all configuration."""
    global policy_config, tos_config, cookie_config, eula_config, refund_config

    for key in policy_config:
        if isinstance(policy_config[key], bool):
            policy_config[key] = False
        elif isinstance(policy_config[key], list):
            policy_config[key] = []
        else:
            policy_config[key] = None

    for key in tos_config:
        if isinstance(tos_config[key], bool):
            tos_config[key] = False
        elif isinstance(tos_config[key], list):
            tos_config[key] = []
        elif key == "minimum_age":
            tos_config[key] = 18
        elif key == "disclaims_warranties":
            tos_config[key] = True
        else:
            tos_config[key] = None

    for key in cookie_config:
        if isinstance(cookie_config[key], bool):
            if key == "uses_essential_cookies":
                cookie_config[key] = True
            elif key == "has_cookie_consent":
                cookie_config[key] = True
            else:
                cookie_config[key] = False
        elif isinstance(cookie_config[key], list):
            cookie_config[key] = []
        else:
            cookie_config[key] = None

    for key in eula_config:
        if isinstance(eula_config[key], bool):
            if key in ["no_reverse_engineering", "no_modification", "no_redistribution",
                       "requires_account", "collects_data", "uses_third_party",
                       "has_export_restrictions", "is_subscription", "auto_renewal"]:
                eula_config[key] = True
            else:
                eula_config[key] = False
        elif isinstance(eula_config[key], list):
            eula_config[key] = []
        elif key == "license_type":
            eula_config[key] = "subscription"
        elif key == "billing_cycle":
            eula_config[key] = "monthly"
        elif key == "trial_period":
            eula_config[key] = "14 days"
        elif key == "liability_cap":
            eula_config[key] = "amount paid for the Software in the 12 months preceding the claim"
        elif key == "jurisdiction":
            eula_config[key] = "the State of Delaware"
        elif key == "dispute_resolution":
            eula_config[key] = "binding arbitration"
        else:
            eula_config[key] = None

    for key in refund_config:
        if isinstance(refund_config[key], bool):
            if key in ["requires_receipt", "requires_original_packaging", "offers_exchanges",
                       "offers_prorated_refunds", "sale_items_refundable"]:
                refund_config[key] = True
            else:
                refund_config[key] = False
        elif isinstance(refund_config[key], list):
            refund_config[key] = []
        elif key == "business_type":
            refund_config[key] = "services"
        elif key == "guarantee_period":
            refund_config[key] = "30 days"
        elif key == "refund_period":
            refund_config[key] = "14 days"
        elif key == "refund_processing_time":
            refund_config[key] = "5-10 business days"
        elif key == "return_period":
            refund_config[key] = "30 days"
        elif key == "return_shipping":
            refund_config[key] = "customer"
        elif key == "subscription_refund_policy":
            refund_config[key] = "prorated"
        else:
            refund_config[key] = None

    return {
        "content": [{
            "type": "text",
            "text": "All configurations reset. Ready to start new documents."
        }]
    }


# ============================================================================
# TERMS OF SERVICE TOOLS
# ============================================================================

@tool(
    "set_tos_service_details",
    "Configure service details for Terms of Service",
    {
        "service_description": str,
        "minimum_age": int,
        "requires_account": bool,
    }
)
async def set_tos_service_details(args: dict[str, Any]) -> dict[str, Any]:
    """Set ToS service details."""
    for key, value in args.items():
        if key in tos_config:
            tos_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Service details configured. Min age: {args.get('minimum_age', 18)}, Account required: {args.get('requires_account', False)}"
        }]
    }


@tool(
    "set_tos_payment_options",
    "Configure payment and subscription options for Terms of Service",
    {
        "has_paid_services": bool,
        "has_subscriptions": bool,
        "has_free_trial": bool,
        "offers_refunds": bool,
        "refund_period": str,
        "payment_processors": str,
    }
)
async def set_tos_payment_options(args: dict[str, Any]) -> dict[str, Any]:
    """Set ToS payment options."""
    for key in ["has_paid_services", "has_subscriptions", "has_free_trial", "offers_refunds", "refund_period"]:
        if key in args:
            tos_config[key] = args[key]

    if args.get("payment_processors"):
        processors = [p.strip() for p in args["payment_processors"].split(",")]
        tos_config["payment_processors"] = processors
        policy_config["payment_processors"] = processors

    return {
        "content": [{
            "type": "text",
            "text": f"Payment options configured. Subscriptions: {args.get('has_subscriptions', False)}, Refunds: {args.get('offers_refunds', False)}"
        }]
    }


@tool(
    "set_tos_user_content",
    "Configure user content settings for Terms of Service",
    {
        "allows_user_content": bool,
        "user_content_types": str,
        "moderates_content": bool,
    }
)
async def set_tos_user_content(args: dict[str, Any]) -> dict[str, Any]:
    """Set ToS user content settings."""
    tos_config["allows_user_content"] = args.get("allows_user_content", False)
    tos_config["moderates_content"] = args.get("moderates_content", False)

    if args.get("user_content_types"):
        tos_config["user_content_types"] = [t.strip() for t in args["user_content_types"].split(",")]

    return {
        "content": [{
            "type": "text",
            "text": f"User content settings configured. Allows content: {args.get('allows_user_content', False)}"
        }]
    }


@tool(
    "set_tos_features",
    "Configure feature settings for Terms of Service",
    {
        "has_third_party_links": bool,
        "provides_api": bool,
        "has_mobile_app": bool,
    }
)
async def set_tos_features(args: dict[str, Any]) -> dict[str, Any]:
    """Set ToS feature settings."""
    for key, value in args.items():
        if key in tos_config:
            tos_config[key] = value

    features = [k.replace("has_", "").replace("provides_", "") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"Features configured: {', '.join(features) if features else 'None'}"
        }]
    }


@tool(
    "set_tos_legal_options",
    "Configure legal and jurisdiction settings for Terms of Service",
    {
        "jurisdiction": str,
        "governing_state": str,
        "has_arbitration": bool,
        "dispute_resolution": str,
    }
)
async def set_tos_legal_options(args: dict[str, Any]) -> dict[str, Any]:
    """Set ToS legal options."""
    for key, value in args.items():
        if key in tos_config:
            tos_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Legal options configured. Jurisdiction: {args.get('jurisdiction', 'Not specified')}, Arbitration: {args.get('has_arbitration', False)}"
        }]
    }


@tool(
    "set_tos_liability",
    "Configure liability and warranty settings for Terms of Service",
    {
        "liability_cap": str,
        "disclaims_warranties": bool,
    }
)
async def set_tos_liability(args: dict[str, Any]) -> dict[str, Any]:
    """Set ToS liability settings."""
    for key, value in args.items():
        if key in tos_config:
            tos_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Liability configured. Cap: {args.get('liability_cap', 'Standard')}, Disclaims warranties: {args.get('disclaims_warranties', True)}"
        }]
    }


@tool(
    "generate_terms_of_service",
    "Generate the final Terms of Service document based on collected configuration",
    {
        "output_format": str,
    }
)
async def generate_terms_of_service(args: dict[str, Any]) -> dict[str, Any]:
    """Generate the Terms of Service document."""
    from tos_generator import generate_tos

    # Merge business info from policy_config to tos_config
    for key in ["platform_type", "website_url", "website_name", "app_name",
                "company_name", "company_address", "country", "contact_email"]:
        if policy_config.get(key) and not tos_config.get(key):
            tos_config[key] = policy_config[key]

    output_format = args.get("output_format", "markdown")
    tos_text = generate_tos(tos_config, output_format)

    # Save to file
    output_dir = Path("generated_policies")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (tos_config.get("company_name") or "tos").lower().replace(" ", "_")

    if output_format == "html":
        filename = f"{company_slug}_terms_of_service_{timestamp}.html"
    else:
        filename = f"{company_slug}_terms_of_service_{timestamp}.md"

    output_path = output_dir / filename
    output_path.write_text(tos_text, encoding="utf-8")

    return {
        "content": [{
            "type": "text",
            "text": f"Terms of Service generated and saved to: {output_path}\n\n{tos_text}"
        }]
    }


@tool(
    "generate_both_documents",
    "Generate both Privacy Policy and Terms of Service documents",
    {
        "output_format": str,
    }
)
async def generate_both_documents(args: dict[str, Any]) -> dict[str, Any]:
    """Generate both Privacy Policy and Terms of Service."""
    from privacy_generator import generate_policy
    from tos_generator import generate_tos

    output_format = args.get("output_format", "markdown")
    output_dir = Path("generated_policies")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (policy_config.get("company_name") or "company").lower().replace(" ", "_")

    # Merge business info
    for key in ["platform_type", "website_url", "website_name", "app_name",
                "company_name", "company_address", "country", "contact_email"]:
        if policy_config.get(key) and not tos_config.get(key):
            tos_config[key] = policy_config[key]

    # Generate Privacy Policy
    policy_text = generate_policy(policy_config, output_format)
    ext = "html" if output_format == "html" else "md"
    policy_path = output_dir / f"{company_slug}_privacy_policy_{timestamp}.{ext}"
    policy_path.write_text(policy_text, encoding="utf-8")

    # Generate Terms of Service
    tos_text = generate_tos(tos_config, output_format)
    tos_path = output_dir / f"{company_slug}_terms_of_service_{timestamp}.{ext}"
    tos_path.write_text(tos_text, encoding="utf-8")

    return {
        "content": [{
            "type": "text",
            "text": f"Both documents generated!\n\nPrivacy Policy saved to: {policy_path}\nTerms of Service saved to: {tos_path}"
        }]
    }


# ============================================================================
# COOKIE POLICY TOOLS
# ============================================================================

@tool(
    "set_cookie_types",
    "Configure cookie types used on the website",
    {
        "uses_essential_cookies": bool,
        "uses_functional_cookies": bool,
        "uses_performance_cookies": bool,
        "uses_analytics": bool,
        "uses_advertising_cookies": bool,
        "uses_social_cookies": bool,
    }
)
async def set_cookie_types(args: dict[str, Any]) -> dict[str, Any]:
    """Set cookie types configuration."""
    for key, value in args.items():
        if key in cookie_config:
            cookie_config[key] = value

    used = [k.replace("uses_", "").replace("_cookies", "") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"Cookie types configured: {', '.join(used) if used else 'Essential only'}"
        }]
    }


@tool(
    "set_cookie_analytics",
    "Configure analytics and performance cookie providers",
    {
        "uses_google_analytics": bool,
        "uses_hotjar": bool,
        "uses_mixpanel": bool,
        "analytics_provider": str,
    }
)
async def set_cookie_analytics(args: dict[str, Any]) -> dict[str, Any]:
    """Set analytics cookie configuration."""
    for key, value in args.items():
        if key in cookie_config:
            cookie_config[key] = value

    # Also update main config for consistency
    if args.get("uses_google_analytics"):
        cookie_config["uses_analytics"] = True

    providers = []
    if args.get("uses_google_analytics"):
        providers.append("Google Analytics")
    if args.get("uses_hotjar"):
        providers.append("Hotjar")
    if args.get("uses_mixpanel"):
        providers.append("Mixpanel")
    if args.get("analytics_provider"):
        providers.append(args["analytics_provider"])

    return {
        "content": [{
            "type": "text",
            "text": f"Analytics cookies configured: {', '.join(providers) if providers else 'None'}"
        }]
    }


@tool(
    "set_cookie_advertising",
    "Configure advertising and marketing cookie providers",
    {
        "uses_facebook_pixel": bool,
        "uses_google_ads": bool,
        "uses_linkedin_insight": bool,
        "uses_twitter_pixel": bool,
        "uses_tiktok_pixel": bool,
    }
)
async def set_cookie_advertising(args: dict[str, Any]) -> dict[str, Any]:
    """Set advertising cookie configuration."""
    for key, value in args.items():
        if key in cookie_config:
            cookie_config[key] = value

    # If any advertising cookies, mark advertising as used
    if any(args.values()):
        cookie_config["uses_advertising_cookies"] = True

    providers = []
    if args.get("uses_facebook_pixel"):
        providers.append("Facebook Pixel")
    if args.get("uses_google_ads"):
        providers.append("Google Ads")
    if args.get("uses_linkedin_insight"):
        providers.append("LinkedIn Insight")
    if args.get("uses_twitter_pixel"):
        providers.append("Twitter Pixel")
    if args.get("uses_tiktok_pixel"):
        providers.append("TikTok Pixel")

    return {
        "content": [{
            "type": "text",
            "text": f"Advertising cookies configured: {', '.join(providers) if providers else 'None'}"
        }]
    }


@tool(
    "set_cookie_social",
    "Configure social media cookies and sharing features",
    {
        "uses_facebook_cookies": bool,
        "uses_twitter_cookies": bool,
        "uses_linkedin_cookies": bool,
        "uses_instagram_cookies": bool,
        "uses_youtube_cookies": bool,
        "uses_pinterest_cookies": bool,
        "social_sharing_enabled": bool,
    }
)
async def set_cookie_social(args: dict[str, Any]) -> dict[str, Any]:
    """Set social media cookie configuration."""
    for key, value in args.items():
        if key in cookie_config:
            cookie_config[key] = value

    # If any social cookies, mark social as used
    social_cookies = ["uses_facebook_cookies", "uses_twitter_cookies", "uses_linkedin_cookies",
                      "uses_instagram_cookies", "uses_youtube_cookies", "uses_pinterest_cookies"]
    if any(args.get(k) for k in social_cookies):
        cookie_config["uses_social_cookies"] = True

    providers = []
    if args.get("uses_facebook_cookies"):
        providers.append("Facebook")
    if args.get("uses_twitter_cookies"):
        providers.append("Twitter/X")
    if args.get("uses_linkedin_cookies"):
        providers.append("LinkedIn")
    if args.get("uses_instagram_cookies"):
        providers.append("Instagram")
    if args.get("uses_youtube_cookies"):
        providers.append("YouTube")
    if args.get("uses_pinterest_cookies"):
        providers.append("Pinterest")

    return {
        "content": [{
            "type": "text",
            "text": f"Social media cookies configured: {', '.join(providers) if providers else 'None'}. Sharing: {args.get('social_sharing_enabled', False)}"
        }]
    }


@tool(
    "set_cookie_consent",
    "Configure cookie consent and compliance settings",
    {
        "has_cookie_consent": bool,
        "honors_dnt": bool,
        "gdpr_compliant": bool,
        "allows_children": bool,
    }
)
async def set_cookie_consent(args: dict[str, Any]) -> dict[str, Any]:
    """Set cookie consent configuration."""
    for key, value in args.items():
        if key in cookie_config:
            cookie_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Cookie consent configured. Consent banner: {args.get('has_cookie_consent', True)}, GDPR compliant: {args.get('gdpr_compliant', False)}"
        }]
    }


@tool(
    "set_cookie_third_party",
    "Configure third-party service cookies",
    {
        "uses_hubspot": bool,
        "uses_intercom": bool,
        "third_party_cookies": str,
    }
)
async def set_cookie_third_party(args: dict[str, Any]) -> dict[str, Any]:
    """Set third-party cookie configuration."""
    cookie_config["uses_hubspot"] = args.get("uses_hubspot", False)
    cookie_config["uses_intercom"] = args.get("uses_intercom", False)

    if args.get("third_party_cookies"):
        cookie_config["third_party_cookies"] = [c.strip() for c in args["third_party_cookies"].split(",")]

    services = []
    if args.get("uses_hubspot"):
        services.append("HubSpot")
    if args.get("uses_intercom"):
        services.append("Intercom")
    if args.get("third_party_cookies"):
        services.extend(cookie_config["third_party_cookies"])

    return {
        "content": [{
            "type": "text",
            "text": f"Third-party cookies configured: {', '.join(services) if services else 'None'}"
        }]
    }


@tool(
    "generate_cookie_policy",
    "Generate the Cookie Policy document based on collected configuration",
    {
        "output_format": str,
    }
)
async def generate_cookie_policy(args: dict[str, Any]) -> dict[str, Any]:
    """Generate the Cookie Policy document."""
    from cookie_generator import generate_cookie_policy as gen_cookie

    # Merge business info from policy_config to cookie_config
    for key in ["company_name", "website_url", "website_name", "company_address", "contact_email"]:
        if policy_config.get(key) and not cookie_config.get(key):
            cookie_config[key] = policy_config[key]

    output_format = args.get("output_format", "markdown")
    cookie_text = gen_cookie(cookie_config, output_format)

    # Save to file
    output_dir = Path("generated_policies")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (cookie_config.get("company_name") or "cookie").lower().replace(" ", "_")

    if output_format == "html":
        filename = f"{company_slug}_cookie_policy_{timestamp}.html"
    else:
        filename = f"{company_slug}_cookie_policy_{timestamp}.md"

    output_path = output_dir / filename
    output_path.write_text(cookie_text, encoding="utf-8")

    return {
        "content": [{
            "type": "text",
            "text": f"Cookie Policy generated and saved to: {output_path}\n\n{cookie_text}"
        }]
    }


# ============================================================================
# EULA TOOLS
# ============================================================================

@tool(
    "set_eula_license_terms",
    "Configure EULA license terms and type",
    {
        "license_type": str,
        "is_transferable": bool,
        "is_subscription": bool,
        "billing_cycle": str,
        "auto_renewal": bool,
        "has_free_trial": bool,
        "trial_period": str,
    }
)
async def set_eula_license_terms(args: dict[str, Any]) -> dict[str, Any]:
    """Set EULA license terms."""
    for key, value in args.items():
        if key in eula_config:
            eula_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"EULA license terms configured. Type: {args.get('license_type', 'subscription')}, Subscription: {args.get('is_subscription', True)}"
        }]
    }


@tool(
    "set_eula_restrictions",
    "Configure EULA usage restrictions",
    {
        "no_reverse_engineering": bool,
        "no_modification": bool,
        "no_redistribution": bool,
        "no_commercial_use": bool,
    }
)
async def set_eula_restrictions(args: dict[str, Any]) -> dict[str, Any]:
    """Set EULA restrictions."""
    for key, value in args.items():
        if key in eula_config:
            eula_config[key] = value

    restrictions = [k.replace("no_", "") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"EULA restrictions configured. Prohibited: {', '.join(restrictions) if restrictions else 'None specified'}"
        }]
    }


@tool(
    "set_eula_features",
    "Configure EULA software features and requirements",
    {
        "requires_account": bool,
        "collects_data": bool,
        "uses_third_party": bool,
        "has_export_restrictions": bool,
    }
)
async def set_eula_features(args: dict[str, Any]) -> dict[str, Any]:
    """Set EULA feature settings."""
    for key, value in args.items():
        if key in eula_config:
            eula_config[key] = value

    features = [k.replace("_", " ") for k, v in args.items() if v]
    return {
        "content": [{
            "type": "text",
            "text": f"EULA features configured: {', '.join(features) if features else 'None specified'}"
        }]
    }


@tool(
    "set_eula_warranty",
    "Configure EULA warranty and liability settings",
    {
        "has_warranty": bool,
        "warranty_period": str,
        "liability_cap": str,
    }
)
async def set_eula_warranty(args: dict[str, Any]) -> dict[str, Any]:
    """Set EULA warranty settings."""
    for key, value in args.items():
        if key in eula_config:
            eula_config[key] = value

    warranty_text = f"{args.get('warranty_period')}" if args.get('has_warranty') else "No warranty (as-is)"
    return {
        "content": [{
            "type": "text",
            "text": f"EULA warranty configured. Warranty: {warranty_text}, Liability cap: {args.get('liability_cap', 'Standard')}"
        }]
    }


@tool(
    "set_eula_legal",
    "Configure EULA jurisdiction and dispute resolution",
    {
        "jurisdiction": str,
        "dispute_resolution": str,
    }
)
async def set_eula_legal(args: dict[str, Any]) -> dict[str, Any]:
    """Set EULA legal settings."""
    for key, value in args.items():
        if key in eula_config:
            eula_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"EULA legal settings configured. Jurisdiction: {args.get('jurisdiction', 'Not specified')}, Disputes: {args.get('dispute_resolution', 'binding arbitration')}"
        }]
    }


@tool(
    "generate_eula",
    "Generate the EULA document based on collected configuration",
    {
        "output_format": str,
    }
)
async def generate_eula(args: dict[str, Any]) -> dict[str, Any]:
    """Generate the EULA document."""
    from eula_generator import generate_eula as gen_eula

    # Merge business info from policy_config to eula_config
    for key in ["company_name", "website_url", "website_name", "app_name", "company_address", "contact_email"]:
        if policy_config.get(key) and not eula_config.get(key):
            eula_config[key] = policy_config[key]

    output_format = args.get("output_format", "markdown")
    eula_text = gen_eula(eula_config, output_format)

    # Save to file
    output_dir = Path("generated_policies")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (eula_config.get("company_name") or "eula").lower().replace(" ", "_")

    if output_format == "html":
        filename = f"{company_slug}_eula_{timestamp}.html"
    else:
        filename = f"{company_slug}_eula_{timestamp}.md"

    output_path = output_dir / filename
    output_path.write_text(eula_text, encoding="utf-8")

    return {
        "content": [{
            "type": "text",
            "text": f"EULA generated and saved to: {output_path}\n\n{eula_text}"
        }]
    }


# ============================================================================
# REFUND POLICY TOOLS
# ============================================================================

@tool(
    "set_refund_general",
    "Configure general refund policy settings",
    {
        "business_type": str,
        "has_satisfaction_guarantee": bool,
        "guarantee_period": str,
        "refund_period": str,
        "refund_processing_time": str,
    }
)
async def set_refund_general(args: dict[str, Any]) -> dict[str, Any]:
    """Set general refund policy settings."""
    for key, value in args.items():
        if key in refund_config:
            refund_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Refund policy configured. Type: {args.get('business_type', 'services')}, Refund period: {args.get('refund_period', '14 days')}"
        }]
    }


@tool(
    "set_refund_physical_products",
    "Configure refund settings for physical products",
    {
        "return_period": str,
        "requires_receipt": bool,
        "requires_original_packaging": bool,
        "offers_exchanges": bool,
        "restocking_fee": str,
        "return_shipping": str,
    }
)
async def set_refund_physical_products(args: dict[str, Any]) -> dict[str, Any]:
    """Set refund settings for physical products."""
    for key, value in args.items():
        if key in refund_config:
            refund_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Physical product returns configured. Period: {args.get('return_period', '30 days')}, Exchanges: {args.get('offers_exchanges', True)}"
        }]
    }


@tool(
    "set_refund_digital_subscription",
    "Configure refund settings for digital products and subscriptions",
    {
        "has_subscriptions": bool,
        "subscription_refund_policy": str,
        "offers_prorated_refunds": bool,
    }
)
async def set_refund_digital_subscription(args: dict[str, Any]) -> dict[str, Any]:
    """Set refund settings for digital products/subscriptions."""
    for key, value in args.items():
        if key in refund_config:
            refund_config[key] = value

    return {
        "content": [{
            "type": "text",
            "text": f"Digital/subscription refunds configured. Policy: {args.get('subscription_refund_policy', 'prorated')}, Pro-rated: {args.get('offers_prorated_refunds', True)}"
        }]
    }


@tool(
    "set_refund_sale_items",
    "Configure refund policy for sale and promotional items",
    {
        "sale_items_refundable": bool,
    }
)
async def set_refund_sale_items(args: dict[str, Any]) -> dict[str, Any]:
    """Set refund policy for sale items."""
    refund_config["sale_items_refundable"] = args.get("sale_items_refundable", True)

    return {
        "content": [{
            "type": "text",
            "text": f"Sale items refund policy configured. Refundable: {args.get('sale_items_refundable', True)}"
        }]
    }


@tool(
    "generate_refund_policy",
    "Generate the Refund Policy document based on collected configuration",
    {
        "output_format": str,
    }
)
async def generate_refund_policy(args: dict[str, Any]) -> dict[str, Any]:
    """Generate the Refund Policy document."""
    from refund_generator import generate_refund_policy as gen_refund

    # Merge business info from policy_config to refund_config
    for key in ["company_name", "website_url", "website_name", "company_address", "contact_email"]:
        if policy_config.get(key) and not refund_config.get(key):
            refund_config[key] = policy_config[key]

    output_format = args.get("output_format", "markdown")
    refund_text = gen_refund(refund_config, output_format)

    # Save to file
    output_dir = Path("generated_policies")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (refund_config.get("company_name") or "refund").lower().replace(" ", "_")

    if output_format == "html":
        filename = f"{company_slug}_refund_policy_{timestamp}.html"
    else:
        filename = f"{company_slug}_refund_policy_{timestamp}.md"

    output_path = output_dir / filename
    output_path.write_text(refund_text, encoding="utf-8")

    return {
        "content": [{
            "type": "text",
            "text": f"Refund Policy generated and saved to: {output_path}\n\n{refund_text}"
        }]
    }


# ============================================================================
# UTILITY TOOLS
# ============================================================================

@tool(
    "generate_all_documents",
    "Generate all five documents: Privacy Policy, Terms of Service, Cookie Policy, EULA, and Refund Policy",
    {
        "output_format": str,
    }
)
async def generate_all_documents(args: dict[str, Any]) -> dict[str, Any]:
    """Generate all five legal documents."""
    from privacy_generator import generate_policy
    from tos_generator import generate_tos
    from cookie_generator import generate_cookie_policy as gen_cookie
    from eula_generator import generate_eula as gen_eula
    from refund_generator import generate_refund_policy as gen_refund

    output_format = args.get("output_format", "markdown")
    output_dir = Path("generated_policies")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (policy_config.get("company_name") or "company").lower().replace(" ", "_")
    ext = "html" if output_format == "html" else "md"

    # Merge business info to all configs
    for key in ["platform_type", "website_url", "website_name", "app_name",
                "company_name", "company_address", "country", "contact_email"]:
        if policy_config.get(key):
            if key in tos_config and not tos_config.get(key):
                tos_config[key] = policy_config[key]
            if key in cookie_config and not cookie_config.get(key):
                cookie_config[key] = policy_config[key]
            if key in eula_config and not eula_config.get(key):
                eula_config[key] = policy_config[key]
            if key in refund_config and not refund_config.get(key):
                refund_config[key] = policy_config[key]

    # Generate Privacy Policy
    policy_text = generate_policy(policy_config, output_format)
    policy_path = output_dir / f"{company_slug}_privacy_policy_{timestamp}.{ext}"
    policy_path.write_text(policy_text, encoding="utf-8")

    # Generate Terms of Service
    tos_text = generate_tos(tos_config, output_format)
    tos_path = output_dir / f"{company_slug}_terms_of_service_{timestamp}.{ext}"
    tos_path.write_text(tos_text, encoding="utf-8")

    # Generate Cookie Policy
    cookie_text = gen_cookie(cookie_config, output_format)
    cookie_path = output_dir / f"{company_slug}_cookie_policy_{timestamp}.{ext}"
    cookie_path.write_text(cookie_text, encoding="utf-8")

    # Generate EULA
    eula_text = gen_eula(eula_config, output_format)
    eula_path = output_dir / f"{company_slug}_eula_{timestamp}.{ext}"
    eula_path.write_text(eula_text, encoding="utf-8")

    # Generate Refund Policy
    refund_text = gen_refund(refund_config, output_format)
    refund_path = output_dir / f"{company_slug}_refund_policy_{timestamp}.{ext}"
    refund_path.write_text(refund_text, encoding="utf-8")

    return {
        "content": [{
            "type": "text",
            "text": f"All five documents generated!\n\nPrivacy Policy: {policy_path}\nTerms of Service: {tos_path}\nCookie Policy: {cookie_path}\nEULA: {eula_path}\nRefund Policy: {refund_path}"
        }]
    }


# System prompt for the legal document generator agent
SYSTEM_PROMPT = """You are a Legal Document Generator Agent. You help users create comprehensive, legally-compliant legal documents for websites, applications, and businesses.

## Your Capabilities

You can generate FIVE types of legal documents:

1. **Privacy Policy** - Explains how user data is collected, used, and protected
2. **Terms of Service** - Defines the rules and guidelines for using the service
3. **Cookie Policy** - Explains what cookies are used and how they work
4. **EULA (End User License Agreement)** - Software licensing terms and conditions
5. **Refund Policy** - Return, refund, and exchange policies

## Your Workflow

1. **Greet the user** and ask what they need:
   - Individual documents (Privacy Policy, ToS, Cookie Policy, EULA, Refund Policy)
   - Any combination of documents
   - All five documents

2. **Gather business information first** (used for all documents):
   - Company name, website/app, country, address
   - Contact email

3. **For Privacy Policy, ask about:**
   - What personal data is collected
   - Tracking technologies (cookies, analytics)
   - Social media integrations
   - Marketing practices
   - Payment processing
   - Mobile app permissions (if applicable)
   - Compliance requirements (GDPR, CCPA, etc.)
   - Data sharing practices
   - User rights
   - Security measures

4. **For Terms of Service, ask about:**
   - Service description and minimum age requirement
   - Account requirements
   - Payment and subscription options (if paid service)
   - User content policies (if users can post content)
   - Third-party links and API access
   - Legal jurisdiction and dispute resolution
   - Liability and warranty disclaimers

5. **For Cookie Policy, ask about:**
   - Cookie types used (essential, functional, analytics, advertising, social)
   - Analytics providers (Google Analytics, Hotjar, Mixpanel)
   - Advertising cookies (Facebook Pixel, Google Ads, LinkedIn, Twitter, TikTok)
   - Social media cookies (Facebook, Twitter, LinkedIn, Instagram, YouTube)
   - Third-party services (HubSpot, Intercom)
   - Cookie consent mechanism
   - GDPR compliance

6. **For EULA, ask about:**
   - License type (perpetual, subscription, freemium)
   - License restrictions (reverse engineering, modification, redistribution)
   - Account requirements
   - Subscription/billing terms
   - Free trial details
   - Warranty and liability
   - Jurisdiction and dispute resolution

7. **For Refund Policy, ask about:**
   - Business type (products, services, digital, subscription)
   - Refund period and conditions
   - Return requirements (receipt, original packaging)
   - Restocking fees
   - Who pays return shipping
   - Subscription refund policy (full, prorated, none)
   - Sale items policy

8. **Generate the document(s)** once all information is collected.

## Guidelines

- Ask questions in a conversational, friendly manner
- Group related questions together
- If generating multiple documents, collect business info once and reuse it
- Explain why certain information is needed when relevant
- Suggest best practices based on the user's business type
- Always confirm key details before generating
- Offer both markdown and HTML output formats

## Available Tools

**For Privacy Policy:**
- set_business_info - Business details (shared with all documents)
- set_data_collection - Personal data collected
- set_tracking_technologies - Cookies, analytics, etc.
- set_social_logins - Social media login options
- set_marketing_settings - Newsletter, ads, analytics
- set_app_permissions - Mobile app permissions
- set_payment_settings - Payment processing
- set_compliance_options - GDPR, CCPA, etc.
- set_data_sharing - Third-party sharing
- set_user_rights - User data rights
- set_security_settings - Security measures
- generate_privacy_policy - Create the document

**For Terms of Service:**
- set_tos_service_details - Service description, age requirements
- set_tos_payment_options - Subscriptions, refunds
- set_tos_user_content - User-generated content rules
- set_tos_features - Third-party links, API, mobile app
- set_tos_legal_options - Jurisdiction, arbitration
- set_tos_liability - Liability caps, warranties
- generate_terms_of_service - Create the document

**For Cookie Policy:**
- set_cookie_types - Cookie types used (essential, functional, analytics, etc.)
- set_cookie_analytics - Analytics providers (Google Analytics, Hotjar, etc.)
- set_cookie_advertising - Advertising cookies (Facebook Pixel, Google Ads, etc.)
- set_cookie_social - Social media cookies (Facebook, Twitter, etc.)
- set_cookie_third_party - Third-party services (HubSpot, Intercom)
- set_cookie_consent - Cookie consent and compliance settings
- generate_cookie_policy - Create the document

**For EULA:**
- set_eula_license_terms - License type, subscription, billing
- set_eula_restrictions - Usage restrictions
- set_eula_features - Account, data collection, third-party
- set_eula_warranty - Warranty and liability settings
- set_eula_legal - Jurisdiction and dispute resolution
- generate_eula - Create the document

**For Refund Policy:**
- set_refund_general - Business type, refund period, processing time
- set_refund_physical_products - Return period, packaging, exchanges
- set_refund_digital_subscription - Subscription refund policy
- set_refund_sale_items - Sale items policy
- generate_refund_policy - Create the document

**Utility:**
- get_current_config - View current settings
- reset_config - Start over
- generate_both_documents - Generate Privacy Policy and ToS
- generate_all_documents - Generate all five documents at once

## Output Formats

- `markdown` (default) - Good for documentation and websites
- `html` - Ready to embed on a website

Start by greeting the user and asking what legal documents they need!"""


async def main():
    """Main entry point for the legal document generator."""
    print("=" * 60)
    print("  Legal Document Generator")
    print("  Privacy Policy, ToS, Cookie Policy, EULA & Refund Policy")
    print("  Powered by Claude Agent SDK")
    print("=" * 60)
    print()

    # Create MCP server with all tools
    legal_tools = create_sdk_mcp_server(
        name="legal_docs",
        version="1.0.0",
        tools=[
            # Business info
            set_business_info,
            # Privacy Policy tools
            set_data_collection,
            set_tracking_technologies,
            set_social_logins,
            set_marketing_settings,
            set_app_permissions,
            set_payment_settings,
            set_compliance_options,
            set_data_sharing,
            set_user_rights,
            set_security_settings,
            generate_privacy_policy,
            # Terms of Service tools
            set_tos_service_details,
            set_tos_payment_options,
            set_tos_user_content,
            set_tos_features,
            set_tos_legal_options,
            set_tos_liability,
            generate_terms_of_service,
            # Cookie Policy tools
            set_cookie_types,
            set_cookie_analytics,
            set_cookie_advertising,
            set_cookie_social,
            set_cookie_consent,
            set_cookie_third_party,
            generate_cookie_policy,
            # EULA tools
            set_eula_license_terms,
            set_eula_restrictions,
            set_eula_features,
            set_eula_warranty,
            set_eula_legal,
            generate_eula,
            # Refund Policy tools
            set_refund_general,
            set_refund_physical_products,
            set_refund_digital_subscription,
            set_refund_sale_items,
            generate_refund_policy,
            # Utility tools
            get_current_config,
            reset_config,
            generate_both_documents,
            generate_all_documents,
        ]
    )

    # Configure the agent
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"legal": legal_tools},
        allowed_tools=[
            # Business info
            "mcp__legal__set_business_info",
            # Privacy Policy tools
            "mcp__legal__set_data_collection",
            "mcp__legal__set_tracking_technologies",
            "mcp__legal__set_social_logins",
            "mcp__legal__set_marketing_settings",
            "mcp__legal__set_app_permissions",
            "mcp__legal__set_payment_settings",
            "mcp__legal__set_compliance_options",
            "mcp__legal__set_data_sharing",
            "mcp__legal__set_user_rights",
            "mcp__legal__set_security_settings",
            "mcp__legal__generate_privacy_policy",
            # Terms of Service tools
            "mcp__legal__set_tos_service_details",
            "mcp__legal__set_tos_payment_options",
            "mcp__legal__set_tos_user_content",
            "mcp__legal__set_tos_features",
            "mcp__legal__set_tos_legal_options",
            "mcp__legal__set_tos_liability",
            "mcp__legal__generate_terms_of_service",
            # Cookie Policy tools
            "mcp__legal__set_cookie_types",
            "mcp__legal__set_cookie_analytics",
            "mcp__legal__set_cookie_advertising",
            "mcp__legal__set_cookie_social",
            "mcp__legal__set_cookie_consent",
            "mcp__legal__set_cookie_third_party",
            "mcp__legal__generate_cookie_policy",
            # EULA tools
            "mcp__legal__set_eula_license_terms",
            "mcp__legal__set_eula_restrictions",
            "mcp__legal__set_eula_features",
            "mcp__legal__set_eula_warranty",
            "mcp__legal__set_eula_legal",
            "mcp__legal__generate_eula",
            # Refund Policy tools
            "mcp__legal__set_refund_general",
            "mcp__legal__set_refund_physical_products",
            "mcp__legal__set_refund_digital_subscription",
            "mcp__legal__set_refund_sale_items",
            "mcp__legal__generate_refund_policy",
            # Utility tools
            "mcp__legal__get_current_config",
            "mcp__legal__reset_config",
            "mcp__legal__generate_both_documents",
            "mcp__legal__generate_all_documents",
        ],
        permission_mode="bypassPermissions",
    )

    # Start the interactive session
    async with ClaudeSDKClient(options=options) as client:
        # Initial greeting
        await client.query("Start the legal document generation process. Greet the user and ask what documents they need (Privacy Policy, Terms of Service, Cookie Policy, EULA, Refund Policy, or all five).")

        # Process and display the greeting
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"\nAssistant: {block.text}\n")

        # Interactive conversation loop
        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("\nThank you for using Legal Document Generator. Goodbye!")
                    break

                # Send user message
                await client.query(user_input)

                # Process and display response
                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                print(f"\nAssistant: {block.text}\n")
                    elif isinstance(message, ResultMessage):
                        if message.is_error:
                            print(f"\n[Error occurred: {message.result}]\n")

            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n[Error: {e}]\n")
                continue


if __name__ == "__main__":
    asyncio.run(main())
