"""
Test script for generating BOTH Privacy Policy and Terms of Service
"""

import asyncio
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
    # Privacy tools
    set_business_info,
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
    # Utility
    get_current_config,
    reset_config,
    generate_both_documents,
    SYSTEM_PROMPT,
)

load_dotenv()

# Sample conversation for BOTH documents
SAMPLE_CONVERSATION = [
    "I need both a Privacy Policy and Terms of Service for my SaaS platform called CloudSync. Website is https://cloudsync.io. We're CloudSync Inc based in Delaware, USA. Address is 500 Tech Park, Wilmington, DE 19801. Contact: legal@cloudsync.io",
    "We collect names, emails, and payment info. Users create accounts with usernames and passwords.",
    "We use cookies, sessions, local storage, and Google Analytics.",
    "We offer Google login.",
    "We have a newsletter and use Google Analytics. No ads.",
    "We accept recurring subscription payments via Stripe.",
    "GDPR and CCPA compliant. No children under 13.",
    "We share data with payment processors only. We don't sell data.",
    "Users can access, delete, and export their data. They can opt out of marketing.",
    "We use SSL encryption and have security measures. Data retained for 5 years.",
    "For ToS: It's a cloud sync and backup service. Minimum age 18. Account required.",
    "We have monthly and annual subscriptions with a 14-day free trial. We offer pro-rated refunds within 30 days.",
    "Users can upload files and share them. We moderate for illegal content.",
    "We have third-party integrations but no public API.",
    "Governed by Delaware law. We use binding arbitration for disputes.",
    "Standard liability caps. We disclaim warranties.",
    "Generate both documents in markdown format please.",
]


async def run_test():
    """Run the test to generate both documents."""
    print("=" * 60)
    print("  Legal Document Generator - FULL TEST")
    print("  Generating Privacy Policy + Terms of Service")
    print("=" * 60)
    print()

    # Create MCP server with all tools
    legal_tools = create_sdk_mcp_server(
        name="legal_docs",
        version="1.0.0",
        tools=[
            set_business_info,
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
            set_tos_service_details,
            set_tos_payment_options,
            set_tos_user_content,
            set_tos_features,
            set_tos_legal_options,
            set_tos_liability,
            generate_terms_of_service,
            get_current_config,
            reset_config,
            generate_both_documents,
        ]
    )

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"legal": legal_tools},
        allowed_tools=[
            "mcp__legal__set_business_info",
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
            "mcp__legal__set_tos_service_details",
            "mcp__legal__set_tos_payment_options",
            "mcp__legal__set_tos_user_content",
            "mcp__legal__set_tos_features",
            "mcp__legal__set_tos_legal_options",
            "mcp__legal__set_tos_liability",
            "mcp__legal__generate_terms_of_service",
            "mcp__legal__get_current_config",
            "mcp__legal__reset_config",
            "mcp__legal__generate_both_documents",
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
                                if len(text) > 1000:
                                    text = text[:1000] + "\n... [output truncated]"
                                print(f"Assistant: {text}")
                                print()
                    elif isinstance(message, ResultMessage):
                        if hasattr(message, 'total_cost_usd') and message.total_cost_usd:
                            print(f"[Cost so far: ${message.total_cost_usd:.4f}]")
                        print()

            print("=" * 60)
            print("  TEST COMPLETED!")
            print("=" * 60)
            print()
            print("Check 'generated_policies' folder for output files.")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_test())
