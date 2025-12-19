"""
Test script for generating ALL FIVE legal documents:
Privacy Policy, Terms of Service, Cookie Policy, EULA, and Refund Policy
"""

import asyncio
import sys

from dotenv import load_dotenv
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)

from main import (
    # Business info
    set_business_info,
    # Privacy tools
    set_data_collection,
    set_tracking_technologies,
    set_social_logins,
    set_marketing_settings,
    set_payment_settings,
    set_compliance_options,
    set_data_sharing,
    set_user_rights,
    set_security_settings,
    generate_privacy_policy,
    # ToS tools
    set_tos_service_details,
    set_tos_payment_options,
    set_tos_user_content,
    set_tos_features,
    set_tos_legal_options,
    set_tos_liability,
    generate_terms_of_service,
    # Cookie tools
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
    # Utility
    get_current_config,
    reset_config,
    generate_both_documents,
    generate_all_documents,
    SYSTEM_PROMPT,
)

load_dotenv()

# Sample conversation for ALL FIVE documents
SAMPLE_CONVERSATION = [
    # Business info
    "I need all five documents - Privacy Policy, Terms of Service, Cookie Policy, EULA, and Refund Policy for my SaaS platform called DataFlow. Website is https://dataflow.io. We're DataFlow Inc based in New York, USA. Address is 250 Tech Avenue, New York, NY 10001. Contact: legal@dataflow.io",

    # Privacy Policy info
    "We collect names, emails, phone numbers, and payment info. Users create accounts with usernames and passwords.",
    "We use cookies, sessions, local storage, and web beacons.",
    "We offer Google and GitHub login options.",
    "We have a newsletter, use Google Analytics for analytics. No ads.",
    "We accept recurring subscription payments via Stripe and PayPal.",
    "GDPR and CCPA compliant. No children under 13.",
    "We share data with payment processors and cloud providers. We don't sell data.",
    "Users can access, delete, export their data and opt out of marketing.",
    "We use SSL encryption and have security measures. Data retained for 3 years.",

    # ToS info
    "For ToS: It's a data analytics and visualization platform. Minimum age 18. Account required.",
    "We have monthly ($29) and annual ($290) subscriptions with a 14-day free trial. Pro-rated refunds within 30 days.",
    "Users can upload datasets and create dashboards. We moderate for illegal content and malware.",
    "We have third-party integrations with Slack and Zapier. We provide a REST API for developers.",
    "Governed by New York law. We use binding arbitration for disputes.",
    "Liability capped at 12 months of fees. We disclaim warranties.",

    # Cookie Policy info
    "For cookies: We use essential, functional, performance, and analytics cookies.",
    "We use Google Analytics and Mixpanel for analytics.",
    "We use Google Ads for remarketing. No Facebook or social pixels.",
    "No social media cookies or sharing buttons.",
    "We use Intercom for customer support chat.",
    "We have a cookie consent banner. GDPR compliant. We honor Do Not Track. No children allowed.",

    # EULA info
    "For the EULA: It's a subscription-based license, billed monthly with auto-renewal. We offer a 14-day free trial.",
    "No reverse engineering, modification, or redistribution allowed. Commercial use is permitted.",
    "Account required, we collect usage data. We use AWS and Google Cloud as third-party services.",
    "No warranty provided. Liability capped at 12 months of subscription fees.",
    "Governed by New York law. Binding arbitration for disputes. Export restrictions apply.",

    # Refund Policy info
    "For refunds: We're a digital services business. We offer a 30-day satisfaction guarantee.",
    "Digital services are refundable within 14 days if not substantially used.",
    "Subscription cancellations get prorated refunds for unused time.",
    "Sale items follow the same refund policy. Refunds processed within 5-10 business days.",

    # Generate all
    "Generate all five documents in markdown format please.",
]


async def run_test():
    """Run the test to generate all five documents."""
    print("=" * 70)
    print("  Legal Document Generator - FULL TEST (ALL 5 DOCUMENTS)")
    print("  Privacy Policy + Terms of Service + Cookie Policy + EULA + Refund")
    print("=" * 70)
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

    try:
        async with ClaudeSDKClient(options=options) as client:
            print("[Starting conversation...]")
            print()
            await client.query("Start by greeting briefly and asking what documents are needed.")

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Assistant: {block.text}")
                            print()

            for i, user_input in enumerate(SAMPLE_CONVERSATION, 1):
                print(f"[Step {i}/{len(SAMPLE_CONVERSATION)}]")
                print(f"User: {user_input}")
                print()

                await client.query(user_input)

                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                # Truncate very long responses
                                text = block.text
                                if len(text) > 1500:
                                    text = text[:1500] + "\n... [output truncated]"
                                print(f"Assistant: {text}")
                                print()
                    elif isinstance(message, ResultMessage):
                        if hasattr(message, 'total_cost_usd') and message.total_cost_usd:
                            print(f"[Cost so far: ${message.total_cost_usd:.4f}]")
                        print()

            print("=" * 70)
            print("  TEST COMPLETED!")
            print("=" * 70)
            print()
            print("Check 'generated_policies' folder for output files.")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_test())
