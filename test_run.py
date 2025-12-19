"""
Test script for Privacy Policy Generator
Runs the agent with sample data to verify functionality.
"""

import asyncio
import os
import sys
import io

# Fix Windows console encoding for Unicode/emoji support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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

# Import the tools and config from main
from main import (
    policy_config,
    set_business_info,
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
    get_current_config,
    generate_privacy_policy,
    reset_config,
    SYSTEM_PROMPT,
)

load_dotenv()

# Sample test data for an e-commerce website
SAMPLE_CONVERSATION = [
    "I need a privacy policy for my e-commerce website called ShopMax. It's at https://shopmax.com. We're a business based in the United States, California. Our company name is ShopMax Inc and we're located at 123 Commerce Street, San Francisco, CA 94102. Contact email is privacy@shopmax.com",
    "We collect customer names, email addresses, phone numbers, mailing addresses, billing addresses, and payment information like credit cards. We also collect usernames and passwords for accounts.",
    "Yes, we use cookies, sessions, and Google Analytics for tracking. We also use local storage.",
    "We offer Google and Facebook login options for our customers.",
    "We have an email newsletter, we use Google Analytics, and we display some ads. We also use Facebook Pixel for advertising.",
    "We accept both one-time and recurring payments through Stripe and PayPal.",
    "Yes, we need GDPR compliance since we have European customers, and CCPA compliance for California. We also want CalOPPA compliance. We don't allow children under 13.",
    "We share data with our shipping partners and payment processors. We don't sell customer data.",
    "Customers can access their data, request deletion, and opt out of marketing. We also offer data portability.",
    "We use SSL encryption and have security measures in place. We retain data for 3 years after account deletion.",
    "Please generate the privacy policy in markdown format.",
]


async def run_test():
    """Run the privacy policy generator with sample data."""
    print("=" * 60)
    print("  Privacy Policy Generator - TEST RUN")
    print("  Testing with sample e-commerce data")
    print("=" * 60)
    print()

    # Create MCP server with all tools
    privacy_tools = create_sdk_mcp_server(
        name="privacy_policy",
        version="1.0.0",
        tools=[
            set_business_info,
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
            get_current_config,
            generate_privacy_policy,
            reset_config,
        ]
    )

    # Configure the agent
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"privacy": privacy_tools},
        allowed_tools=[
            "mcp__privacy__set_business_info",
            "mcp__privacy__set_data_collection",
            "mcp__privacy__set_tracking_technologies",
            "mcp__privacy__set_social_logins",
            "mcp__privacy__set_marketing_settings",
            "mcp__privacy__set_app_permissions",
            "mcp__privacy__set_payment_settings",
            "mcp__privacy__set_compliance_options",
            "mcp__privacy__set_data_sharing",
            "mcp__privacy__set_user_rights",
            "mcp__privacy__set_security_settings",
            "mcp__privacy__get_current_config",
            "mcp__privacy__generate_privacy_policy",
            "mcp__privacy__reset_config",
        ],
        permission_mode="bypassPermissions",
    )

    try:
        async with ClaudeSDKClient(options=options) as client:
            # Initial greeting
            print("[Starting conversation...]")
            print()
            await client.query("Start the privacy policy generation process. Greet the user briefly and ask for their business information.")

            # Process greeting
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Assistant: {block.text}")
                            print()

            # Send sample data through conversation
            for i, user_input in enumerate(SAMPLE_CONVERSATION, 1):
                print(f"[Step {i}/{len(SAMPLE_CONVERSATION)}]")
                print(f"User: {user_input}")
                print()

                await client.query(user_input)

                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                print(f"Assistant: {block.text}")
                                print()
                    elif isinstance(message, ResultMessage):
                        if message.is_error:
                            print(f"[Error: {message.result}]")
                        else:
                            print(f"[Completed - Cost: ${message.total_cost_usd:.4f}]" if message.total_cost_usd else "[Completed]")
                        print()

            print("=" * 60)
            print("  TEST COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print()
            print("Check the 'generated_policies' folder for the output file.")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_test())
