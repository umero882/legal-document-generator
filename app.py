"""
Legal Document Generator - Web Application
A FastAPI web app that generates Privacy Policies, Terms of Service,
Cookie Policies, EULAs, and Refund Policies.

Production-ready with environment configuration.
"""

import os
import uuid
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from functools import lru_cache

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings
from typing import List, Literal

# Import generators
from privacy_generator import generate_policy
from tos_generator import generate_tos
from cookie_generator import generate_cookie_policy
from eula_generator import generate_eula
from refund_generator import generate_refund_policy


# ============================================================================
# Environment Configuration
# ============================================================================

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    app_env: str = "production"
    host: str = "0.0.0.0"
    port: int = 8001
    cors_origins: str = "*"
    secret_key: str = "change-in-production"
    rate_limit: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

# Determine if running in production
IS_PRODUCTION = settings.app_env.lower() == "production"

# Create FastAPI app
app = FastAPI(
    title="Legal Document Generator",
    description="Generate Privacy Policies, Terms of Service, Cookie Policies, EULAs, and Refund Policies",
    version="1.0.0",
    docs_url="/api/docs" if not IS_PRODUCTION else None,  # Disable docs in production
    redoc_url="/api/redoc" if not IS_PRODUCTION else None,
)

# Configure CORS
cors_origins = settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Pydantic Models for API
# ============================================================================

class CreateSessionRequest(BaseModel):
    doc_types: List[Literal["privacy", "tos", "cookie", "eula", "refund", "all"]] = ["privacy"]


class SessionResponse(BaseModel):
    session_id: str
    config: dict
    created_at: str


class UpdateConfigRequest(BaseModel):
    config: dict

    @field_validator('config')
    @classmethod
    def validate_config(cls, v):
        """Validate config doesn't contain dangerous keys."""
        dangerous_keys = ['__proto__', 'constructor', 'prototype']
        for key in v.keys():
            if key in dangerous_keys:
                raise ValueError(f"Invalid config key: {key}")
        return v


class GenerateRequest(BaseModel):
    session_id: str
    doc_types: List[Literal["privacy", "tos", "cookie", "eula", "refund"]]
    output_format: Literal["markdown", "html"] = "markdown"

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v):
        """Validate session_id is a valid UUID format."""
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        if not uuid_pattern.match(v):
            raise ValueError("Invalid session ID format")
        return v


class GeneratedDocument(BaseModel):
    doc_type: str
    filename: str
    content: str
    format: str


class GenerateResponse(BaseModel):
    status: str
    documents: List[GeneratedDocument]

# Create directories
output_dir = Path(__file__).parent / "generated_policies"
output_dir.mkdir(exist_ok=True)

# Frontend dist directory
frontend_dist = Path(__file__).parent / "frontend" / "dist"

# In-memory session storage (for production, use Redis or database)
sessions: dict[str, dict[str, Any]] = {}


def get_default_config() -> dict[str, Any]:
    """Get default configuration for all documents."""
    return {
        # Business Information
        "platform_type": "website",
        "website_url": "",
        "website_name": "",
        "app_name": "",
        "business_type": "business",
        "company_name": "",
        "company_address": "",
        "country": "",
        "contact_email": "",
        "contact_phone": "",

        # Data Collection
        "collects_name": True,
        "collects_email": True,
        "collects_phone": False,
        "collects_address": False,
        "collects_billing_address": False,
        "collects_payment_info": False,
        "collects_age": False,
        "collects_username": True,
        "collects_password": True,

        # Tracking
        "uses_cookies": True,
        "uses_web_beacons": False,
        "uses_local_storage": False,
        "uses_sessions": True,
        "uses_google_maps": False,

        # Social Login
        "social_login_facebook": False,
        "social_login_google": False,
        "social_login_twitter": False,
        "social_login_github": False,
        "social_login_linkedin": False,

        # Marketing
        "has_email_newsletter": False,
        "uses_analytics": False,
        "analytics_provider": "",
        "displays_ads": False,
        "uses_facebook_pixel": False,
        "uses_retargeting": False,

        # App Permissions
        "requests_geolocation": False,
        "requests_contacts": False,
        "requests_camera": False,
        "requests_photo_gallery": False,
        "requests_microphone": False,
        "requests_push_notifications": False,

        # Payment
        "accepts_payments": False,
        "payment_type": "one_time",
        "payment_processors": [],

        # Compliance
        "gdpr_compliant": False,
        "ccpa_compliant": False,
        "caloppa_compliant": False,
        "coppa_compliant": False,
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

        # Security
        "uses_encryption": True,
        "uses_ssl": True,
        "has_security_measures": True,
        "data_retention_period": "",

        # ToS specific
        "service_description": "",
        "minimum_age": 18,
        "requires_account": True,
        "has_paid_services": False,
        "has_subscriptions": False,
        "has_free_trial": False,
        "offers_refunds": False,
        "refund_period": "",
        "allows_user_content": False,
        "user_content_types": [],
        "moderates_content": False,
        "has_third_party_links": False,
        "provides_api": False,
        "has_mobile_app": False,
        "jurisdiction": "",
        "governing_state": "",
        "has_arbitration": False,
        "dispute_resolution": "",
        "liability_cap": "",
        "disclaims_warranties": True,

        # Cookie specific
        "uses_essential_cookies": True,
        "uses_functional_cookies": False,
        "uses_performance_cookies": False,
        "uses_advertising_cookies": False,
        "uses_social_cookies": False,
        "uses_google_analytics": False,
        "uses_hotjar": False,
        "uses_mixpanel": False,
        "uses_google_ads": False,
        "uses_linkedin_insight": False,
        "uses_twitter_pixel": False,
        "uses_tiktok_pixel": False,
        "uses_facebook_cookies": False,
        "uses_twitter_cookies": False,
        "uses_linkedin_cookies": False,
        "uses_instagram_cookies": False,
        "uses_youtube_cookies": False,
        "uses_pinterest_cookies": False,
        "social_sharing_enabled": False,
        "uses_hubspot": False,
        "uses_intercom": False,
        "third_party_cookies": [],
        "has_cookie_consent": True,
        "honors_dnt": False,

        # EULA specific
        "license_type": "subscription",
        "is_transferable": False,
        "is_subscription": True,
        "billing_cycle": "monthly",
        "auto_renewal": True,
        "trial_period": "14 days",
        "no_reverse_engineering": True,
        "no_modification": True,
        "no_redistribution": True,
        "no_commercial_use": False,
        "collects_data": True,
        "uses_third_party": True,
        "has_export_restrictions": False,
        "has_warranty": False,
        "warranty_period": "",
        "eula_liability_cap": "",

        # Refund specific
        "refund_business_type": "services",
        "has_satisfaction_guarantee": False,
        "guarantee_period": "30 days",
        "refund_period_days": "14 days",
        "refund_processing_time": "5-10 business days",
        "return_period": "30 days",
        "requires_receipt": True,
        "requires_original_packaging": True,
        "offers_exchanges": True,
        "restocking_fee": "",
        "return_shipping": "customer",
        "subscription_refund_policy": "prorated",
        "offers_prorated_refunds": True,
        "sale_items_refundable": True,
    }


def get_or_create_session(session_id: Optional[str] = None) -> tuple[str, dict[str, Any]]:
    """Get existing session or create a new one."""
    if session_id and session_id in sessions:
        return session_id, sessions[session_id]

    new_id = str(uuid.uuid4())
    sessions[new_id] = get_default_config()
    return new_id, sessions[new_id]




# ============================================================================
# REST API v1 Routes (for React frontend)
# ============================================================================

@app.post("/api/v1/sessions")
async def create_session_v1(request: CreateSessionRequest = None):
    """Create a new session."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = get_default_config()
    return {
        "session_id": session_id,
        "config": sessions[session_id],
        "created_at": datetime.now().isoformat()
    }


@app.get("/api/v1/sessions/{session_id}")
async def get_session_v1(session_id: str):
    """Get session configuration."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session_id,
        "config": sessions[session_id]
    }


@app.patch("/api/v1/sessions/{session_id}/config")
async def update_config_v1(session_id: str, request: UpdateConfigRequest):
    """Update session configuration (JSON)."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    # Merge new config with existing
    current_config = sessions[session_id]
    for key, value in request.config.items():
        if key in current_config:
            current_config[key] = value

    sessions[session_id] = current_config
    return {"status": "success", "config": current_config}


@app.post("/api/v1/sessions/{session_id}/reset")
async def reset_session_v1(session_id: str):
    """Reset session to defaults."""
    sessions[session_id] = get_default_config()
    return {"status": "success", "config": sessions[session_id]}


@app.post("/api/v1/documents/generate")
async def generate_documents_v1(request: GenerateRequest):
    """Generate documents (JSON API)."""
    if request.session_id not in sessions:
        raise HTTPException(status_code=400, detail="Invalid session")

    config = sessions[request.session_id]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_slug = (config.get("company_name") or "document").lower().replace(" ", "_")[:20]
    ext = "html" if request.output_format == "html" else "md"

    generated_docs = []

    try:
        for doc_type in request.doc_types:
            if doc_type == "privacy":
                content = generate_policy(config, request.output_format)
                filename = f"{company_slug}_privacy_policy_{timestamp}.{ext}"
            elif doc_type == "tos":
                content = generate_tos(config, request.output_format)
                filename = f"{company_slug}_terms_of_service_{timestamp}.{ext}"
            elif doc_type == "cookie":
                content = generate_cookie_policy(config, request.output_format)
                filename = f"{company_slug}_cookie_policy_{timestamp}.{ext}"
            elif doc_type == "eula":
                content = generate_eula(config, request.output_format)
                filename = f"{company_slug}_eula_{timestamp}.{ext}"
            elif doc_type == "refund":
                content = generate_refund_policy(config, request.output_format)
                filename = f"{company_slug}_refund_policy_{timestamp}.{ext}"
            else:
                continue

            # Save file
            filepath = output_dir / filename
            filepath.write_text(content, encoding="utf-8")

            generated_docs.append({
                "doc_type": doc_type,
                "filename": filename,
                "content": content,
                "format": request.output_format
            })

        return {"status": "success", "documents": generated_docs}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/preview/{session_id}/{doc_type}")
async def preview_document_v1(session_id: str, doc_type: str, format: str = "markdown"):
    """Preview a document without saving."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    valid_types = ["privacy", "tos", "cookie", "eula", "refund"]
    if doc_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid document type")

    config = sessions[session_id]

    try:
        if doc_type == "privacy":
            content = generate_policy(config, format)
        elif doc_type == "tos":
            content = generate_tos(config, format)
        elif doc_type == "cookie":
            content = generate_cookie_policy(config, format)
        elif doc_type == "eula":
            content = generate_eula(config, format)
        elif doc_type == "refund":
            content = generate_refund_policy(config, format)

        return {"doc_type": doc_type, "content": content, "format": format}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/download/{filename}")
async def download_document_v1(filename: str):
    """Download a generated document."""
    filepath = output_dir / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="application/octet-stream"
    )


@app.get("/api/v1/config/defaults")
async def get_default_config_v1():
    """Get default configuration values."""
    return get_default_config()


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


# ============================================================================
# Serve React Frontend (Production)
# ============================================================================

# Serve static assets if frontend is built
if frontend_dist.exists() and (frontend_dist / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="frontend_assets")


@app.get("/")
async def serve_root():
    """Serve React frontend root."""
    if frontend_dist.exists():
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file), media_type="text/html")
    raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in frontend directory.")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve React frontend for all non-API routes (SPA catch-all)."""
    # Don't serve frontend for API routes
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")

    # Check if it's a static file request
    if frontend_dist.exists():
        # Try to serve the exact file first
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))

        # For all other routes, serve index.html (SPA routing)
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file), media_type="text/html")

    raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in frontend directory.")


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=not IS_PRODUCTION
    )
