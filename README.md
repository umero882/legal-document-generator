# Legal Document Generator

A comprehensive legal document generator powered by Claude Agent SDK. This interactive agent helps you create legally-compliant **Privacy Policies**, **Terms of Service**, **Cookie Policies**, **EULAs**, and **Refund Policies** for your website, application, or business through a conversational interface.

## Features

### Privacy Policy Generator
- **Interactive conversation**: The agent guides you through the entire process
- **Comprehensive coverage**: Supports all major privacy policy sections
  - Business information
  - Data collection practices
  - Tracking technologies (cookies, analytics, etc.)
  - Social media integrations
  - Marketing and advertising disclosures
  - Mobile app permissions
  - Payment processing
  - Data sharing and third-party practices
  - User rights and data control
  - Security measures
- **Compliance options**: GDPR, CCPA, CalOPPA, and COPPA support

### Terms of Service Generator
- **Service terms**: Account requirements, acceptable use policies
- **Payment terms**: Subscriptions, refunds, free trials
- **User content**: Content policies, licensing, moderation
- **Legal protections**: Liability limitations, disclaimers, indemnification
- **Dispute resolution**: Arbitration clauses, governing law
- **Intellectual property**: Copyright, trademark protections

### Cookie Policy Generator
- **Cookie types**: Essential, functional, performance, analytics, advertising, social
- **Analytics providers**: Google Analytics, Hotjar, Mixpanel
- **Advertising cookies**: Facebook Pixel, Google Ads, LinkedIn, Twitter, TikTok
- **Social media cookies**: Facebook, Twitter, LinkedIn, Instagram, YouTube, Pinterest
- **Third-party services**: HubSpot, Intercom, and more
- **Consent mechanisms**: Cookie consent banners, GDPR compliance
- **Do Not Track**: Honor browser DNT settings

### EULA (End User License Agreement) Generator
- **License types**: Perpetual, subscription, freemium
- **Usage restrictions**: Reverse engineering, modification, redistribution
- **Account requirements**: Registration, authentication
- **Subscription terms**: Billing cycles, auto-renewal, free trials
- **Warranty and liability**: Disclaimer of warranties, liability caps
- **Intellectual property**: Software ownership, user feedback
- **Export compliance**: Export control restrictions

### Refund Policy Generator
- **Business types**: Physical products, digital goods, services, subscriptions
- **Return periods**: Customizable timeframes
- **Refund conditions**: Receipt requirements, original packaging
- **Exchanges**: Product exchange options
- **Restocking fees**: Optional fees for returns
- **Subscription refunds**: Full, prorated, or no refund options
- **Sale items**: Policies for discounted items

### Shared Features
- **Multiple output formats**: Markdown and HTML
- **Automatic file saving**: Documents saved to `generated_policies/` directory
- **Generate all at once**: Create all five legal documents together
- **Business info sharing**: Enter company details once, reuse across all documents

## Requirements

- Python 3.10 or higher
- Anthropic API key

## Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

   Get your API key from: https://console.anthropic.com/

## Usage

Run the application:
```bash
python main.py
```

The agent will greet you and ask what documents you need:
- **Privacy Policy**
- **Terms of Service**
- **Cookie Policy**
- **EULA**
- **Refund Policy**
- **Any combination**
- **All five documents**

### Commands

- Type `quit`, `exit`, or `bye` to end the session
- Press `Ctrl+C` to interrupt at any time

## Output

Generated documents are saved to the `generated_policies/` directory with filenames like:
- `company_name_privacy_policy_20251219_143052.md`
- `company_name_terms_of_service_20251219_143052.md`
- `company_name_cookie_policy_20251219_143052.md`
- `company_name_eula_20251219_143052.md`
- `company_name_refund_policy_20251219_143052.md`
- HTML versions with `.html` extension

## Project Structure

```
legal-document-generator/
├── main.py               # Main application with agent logic
├── privacy_generator.py  # Privacy policy templates and logic
├── tos_generator.py      # Terms of service templates and logic
├── cookie_generator.py   # Cookie policy templates and logic
├── eula_generator.py     # EULA templates and logic
├── refund_generator.py   # Refund policy templates and logic
├── test_run.py           # Test script for privacy policy
├── test_tos.py           # Test script for ToS
├── test_both.py          # Test script for privacy + ToS
├── test_cookies.py       # Test script for cookie policy
├── test_all.py           # Test script for all documents
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment configuration
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── generated_policies/  # Output directory (created automatically)
```

## Customization

### System Prompt

The agent's behavior is controlled by the `SYSTEM_PROMPT` variable in `main.py`. You can modify it to change how the agent interacts with users.

### Templates

The document generation logic is in separate modules:
- `privacy_generator.py` - Privacy policy sections and formatting
- `tos_generator.py` - Terms of service sections and formatting
- `cookie_generator.py` - Cookie policy sections and formatting
- `eula_generator.py` - EULA sections and formatting
- `refund_generator.py` - Refund policy sections and formatting

You can customize:
- Section content and wording
- HTML styling
- Additional compliance frameworks
- Output formatting

## Tools Available

### Privacy Policy Tools (12 tools)
| Tool | Description |
|------|-------------|
| `set_business_info` | Company details (shared with all documents) |
| `set_data_collection` | Personal data collected |
| `set_tracking_technologies` | Cookies, analytics, etc. |
| `set_social_logins` | Social media login options |
| `set_marketing_settings` | Newsletter, ads, analytics |
| `set_app_permissions` | Mobile app permissions |
| `set_payment_settings` | Payment processing |
| `set_compliance_options` | GDPR, CCPA, etc. |
| `set_data_sharing` | Third-party sharing |
| `set_user_rights` | User data rights |
| `set_security_settings` | Security measures |
| `generate_privacy_policy` | Create the document |

### Terms of Service Tools (7 tools)
| Tool | Description |
|------|-------------|
| `set_tos_service_details` | Service description, age requirements |
| `set_tos_payment_options` | Subscriptions, refunds, trials |
| `set_tos_user_content` | User-generated content rules |
| `set_tos_features` | Third-party links, API, mobile app |
| `set_tos_legal_options` | Jurisdiction, arbitration |
| `set_tos_liability` | Liability caps, warranties |
| `generate_terms_of_service` | Create the document |

### Cookie Policy Tools (7 tools)
| Tool | Description |
|------|-------------|
| `set_cookie_types` | Cookie types (essential, functional, analytics, etc.) |
| `set_cookie_analytics` | Analytics providers (Google Analytics, Hotjar, etc.) |
| `set_cookie_advertising` | Advertising cookies (Facebook Pixel, Google Ads, etc.) |
| `set_cookie_social` | Social media cookies (Facebook, Twitter, etc.) |
| `set_cookie_third_party` | Third-party services (HubSpot, Intercom) |
| `set_cookie_consent` | Consent and compliance settings |
| `generate_cookie_policy` | Create the document |

### EULA Tools (6 tools)
| Tool | Description |
|------|-------------|
| `set_eula_license_terms` | License type, subscription, billing |
| `set_eula_restrictions` | Usage restrictions |
| `set_eula_features` | Account, data collection, third-party |
| `set_eula_warranty` | Warranty and liability settings |
| `set_eula_legal` | Jurisdiction and dispute resolution |
| `generate_eula` | Create the document |

### Refund Policy Tools (5 tools)
| Tool | Description |
|------|-------------|
| `set_refund_general` | Business type, refund period, processing time |
| `set_refund_physical_products` | Return period, packaging, exchanges |
| `set_refund_digital_subscription` | Subscription refund policy |
| `set_refund_sale_items` | Sale items policy |
| `generate_refund_policy` | Create the document |

### Utility Tools (4 tools)
| Tool | Description |
|------|-------------|
| `get_current_config` | View current settings |
| `reset_config` | Start over |
| `generate_both_documents` | Generate Privacy Policy and ToS |
| `generate_all_documents` | Generate all five documents |

## Total: 41 Tools

## Resources

- [Claude Agent SDK Documentation](https://platform.claude.com/docs/en/api/agent-sdk/python)
- [Anthropic Console](https://console.anthropic.com/) - Get your API key
- [Termify.io](https://termify.io/) - Reference for features

## License

MIT License
