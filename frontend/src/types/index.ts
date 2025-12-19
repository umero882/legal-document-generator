// Document types
export type DocumentType = 'privacy' | 'tos' | 'cookie' | 'eula' | 'refund';
export type OutputFormat = 'markdown' | 'html';

// Configuration types
export interface DocumentConfig {
  // Business Information
  platform_type: 'website' | 'app' | 'both';
  website_url: string;
  website_name: string;
  app_name: string;
  business_type: string;
  company_name: string;
  company_address: string;
  country: string;
  contact_email: string;
  contact_phone: string;

  // Data Collection
  collects_name: boolean;
  collects_email: boolean;
  collects_phone: boolean;
  collects_address: boolean;
  collects_billing_address: boolean;
  collects_payment_info: boolean;
  collects_age: boolean;
  collects_username: boolean;
  collects_password: boolean;

  // Tracking
  uses_cookies: boolean;
  uses_web_beacons: boolean;
  uses_local_storage: boolean;
  uses_sessions: boolean;
  uses_google_maps: boolean;

  // Social Login
  social_login_facebook: boolean;
  social_login_google: boolean;
  social_login_twitter: boolean;
  social_login_github: boolean;
  social_login_linkedin: boolean;

  // Marketing
  has_email_newsletter: boolean;
  uses_analytics: boolean;
  analytics_provider: string;
  displays_ads: boolean;
  uses_facebook_pixel: boolean;
  uses_retargeting: boolean;

  // App Permissions
  requests_geolocation: boolean;
  requests_contacts: boolean;
  requests_camera: boolean;
  requests_photo_gallery: boolean;
  requests_microphone: boolean;
  requests_push_notifications: boolean;

  // Payment
  accepts_payments: boolean;
  payment_type: string;
  payment_processors: string[];

  // Compliance
  gdpr_compliant: boolean;
  ccpa_compliant: boolean;
  caloppa_compliant: boolean;
  coppa_compliant: boolean;
  allows_children_under_13: boolean;

  // Data Sharing
  shares_with_third_parties: boolean;
  third_party_categories: string[];
  sells_data: boolean;

  // User Rights
  allows_data_access: boolean;
  allows_data_deletion: boolean;
  allows_data_portability: boolean;
  allows_opt_out: boolean;

  // Security
  uses_encryption: boolean;
  uses_ssl: boolean;
  has_security_measures: boolean;
  data_retention_period: string;

  // ToS specific
  service_description: string;
  minimum_age: number;
  requires_account: boolean;
  has_paid_services: boolean;
  has_subscriptions: boolean;
  has_free_trial: boolean;
  offers_refunds: boolean;
  refund_period: string;
  allows_user_content: boolean;
  user_content_types: string[];
  moderates_content: boolean;
  has_third_party_links: boolean;
  provides_api: boolean;
  has_mobile_app: boolean;
  jurisdiction: string;
  governing_state: string;
  has_arbitration: boolean;
  dispute_resolution: string;
  liability_cap: string;
  disclaims_warranties: boolean;

  // Cookie specific
  uses_essential_cookies: boolean;
  uses_functional_cookies: boolean;
  uses_performance_cookies: boolean;
  uses_advertising_cookies: boolean;
  uses_social_cookies: boolean;
  uses_google_analytics: boolean;
  uses_hotjar: boolean;
  uses_mixpanel: boolean;
  uses_google_ads: boolean;
  uses_linkedin_insight: boolean;
  uses_twitter_pixel: boolean;
  uses_tiktok_pixel: boolean;
  uses_facebook_cookies: boolean;
  uses_twitter_cookies: boolean;
  uses_linkedin_cookies: boolean;
  uses_instagram_cookies: boolean;
  uses_youtube_cookies: boolean;
  uses_pinterest_cookies: boolean;
  social_sharing_enabled: boolean;
  uses_hubspot: boolean;
  uses_intercom: boolean;
  third_party_cookies: string[];
  has_cookie_consent: boolean;
  honors_dnt: boolean;

  // EULA specific
  license_type: string;
  is_transferable: boolean;
  is_subscription: boolean;
  billing_cycle: string;
  auto_renewal: boolean;
  trial_period: string;
  no_reverse_engineering: boolean;
  no_modification: boolean;
  no_redistribution: boolean;
  no_commercial_use: boolean;
  collects_data: boolean;
  uses_third_party: boolean;
  has_export_restrictions: boolean;
  has_warranty: boolean;
  warranty_period: string;
  eula_liability_cap: string;

  // Refund specific
  refund_business_type: string;
  has_satisfaction_guarantee: boolean;
  guarantee_period: string;
  refund_period_days: string;
  refund_processing_time: string;
  return_period: string;
  requires_receipt: boolean;
  requires_original_packaging: boolean;
  offers_exchanges: boolean;
  restocking_fee: string;
  return_shipping: string;
  subscription_refund_policy: string;
  offers_prorated_refunds: boolean;
  sale_items_refundable: boolean;
}

// Session types
export interface Session {
  session_id: string;
  config: DocumentConfig;
  created_at?: string;
}

// Generated document types
export interface GeneratedDocument {
  doc_type: DocumentType;
  filename: string;
  content: string;
  format: OutputFormat;
}

// API Response types
export interface GenerateResponse {
  status: string;
  documents: GeneratedDocument[];
}

export interface PreviewResponse {
  doc_type: DocumentType;
  content: string;
  format: OutputFormat;
}

// Wizard types
export interface WizardStep {
  id: string;
  title: string;
  description?: string;
  fields: string[];
}

export interface WizardConfig {
  docType: DocumentType;
  steps: WizardStep[];
}

// Document info for display
export interface DocumentInfo {
  type: DocumentType;
  title: string;
  description: string;
  icon: string;
  color: string;
}

export const DOCUMENT_INFO: Record<DocumentType, DocumentInfo> = {
  privacy: {
    type: 'privacy',
    title: 'Privacy Policy',
    description: 'How you collect, use, and protect user data',
    icon: 'shield',
    color: 'blue',
  },
  tos: {
    type: 'tos',
    title: 'Terms of Service',
    description: 'Rules and guidelines for using your service',
    icon: 'document',
    color: 'purple',
  },
  cookie: {
    type: 'cookie',
    title: 'Cookie Policy',
    description: 'Cookie usage and tracking technologies',
    icon: 'cookie',
    color: 'yellow',
  },
  eula: {
    type: 'eula',
    title: 'EULA',
    description: 'End User License Agreement for software',
    icon: 'code',
    color: 'green',
  },
  refund: {
    type: 'refund',
    title: 'Refund Policy',
    description: 'Return, refund, and exchange policies',
    icon: 'currency',
    color: 'red',
  },
};
