"""
Test script for generating Cookie Policy
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
    # Business info
    set_business_info,
    # Cookie tools
    set_cookie_types,
    set_cookie_analytics,
    set_cookie_advertising,
    set_cookie_social,
    set_cookie_consent,
    set_cookie_third_party,
    generate_cookie_policy,
    # Utility
    get_current_config,
    reset_config,
    SYSTEM_PROMPT,
)

load_dotenv()

# Sample conversation for Cookie Policy
SAMPLE_CONVERSATION = [
    "I need a Cookie Policy for my e-commerce website called TechMart. Website is https://techmart.com. We're TechMart LLC based in California, USA. Address is 100 Commerce Way, San Francisco, CA 94102. Contact: privacy@techmart.com",
    "We use essential cookies for cart and checkout, functional cookies for user preferences, and performance cookies for site speed.",
    "We use Google Analytics and Hotjar for analytics.",
    "We use Facebook Pixel and Google Ads for advertising. Also LinkedIn Insight for B2B marketing.",
    "We have Facebook, Twitter, and Instagram share buttons. YouTube embedded videos too.",
    "We also use HubSpot for CRM and Intercom for customer support chat.",
    "We have a cookie consent banner. We're GDPR compliant and honor Do Not Track signals.",
    "Generate the cookie policy in markdown format please.",
]


async def run_test():
    """Run the test to generate Cookie Policy."""
    print("=" * 60)
    print("  Cookie Policy Generator - TEST")
    print("=" * 60)
    print()

    # Create MCP server with cookie tools
    legal_tools = create_sdk_mcp_server(
        name="legal_docs",
        version="1.0.0",
        tools=[
            set_business_info,
            set_cookie_types,
            set_cookie_analytics,
            set_cookie_advertising,
            set_cookie_social,
            set_cookie_consent,
            set_cookie_third_party,
            generate_cookie_policy,
            get_current_config,
            reset_config,
        ]
    )

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"legal": legal_tools},
        allowed_tools=[
            "mcp__legal__set_business_info",
            "mcp__legal__set_cookie_types",
            "mcp__legal__set_cookie_analytics",
            "mcp__legal__set_cookie_advertising",
            "mcp__legal__set_cookie_social",
            "mcp__legal__set_cookie_consent",
            "mcp__legal__set_cookie_third_party",
            "mcp__legal__generate_cookie_policy",
            "mcp__legal__get_current_config",
            "mcp__legal__reset_config",
        ],
        permission_mode="bypassPermissions",
    )

    try:
        async with ClaudeSDKClient(options=options) as client:
            print("[Starting conversation...]")
            print()
            await client.query("The user wants to generate a Cookie Policy. Greet briefly and ask about their website.")

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
