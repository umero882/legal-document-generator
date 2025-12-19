import { create } from 'zustand';
import type { DocumentType, WizardStep } from '../types';

// Define wizard steps for each document type
const WIZARD_STEPS: Record<DocumentType, WizardStep[]> = {
  privacy: [
    { id: 'business', title: 'Business Info', description: 'Company details', fields: ['company_name', 'website_url', 'contact_email'] },
    { id: 'data', title: 'Data Collection', description: 'What data you collect', fields: ['collects_name', 'collects_email'] },
    { id: 'tracking', title: 'Tracking', description: 'Tracking technologies', fields: ['uses_cookies', 'uses_analytics'] },
    { id: 'social', title: 'Social Login', description: 'Social media options', fields: ['social_login_google', 'social_login_facebook'] },
    { id: 'marketing', title: 'Marketing', description: 'Marketing practices', fields: ['has_email_newsletter', 'displays_ads'] },
    { id: 'compliance', title: 'Compliance', description: 'Legal compliance', fields: ['gdpr_compliant', 'ccpa_compliant'] },
    { id: 'review', title: 'Review', description: 'Review and generate', fields: [] },
  ],
  tos: [
    { id: 'business', title: 'Business Info', description: 'Company details', fields: ['company_name', 'website_url', 'contact_email'] },
    { id: 'service', title: 'Service Details', description: 'About your service', fields: ['service_description', 'minimum_age'] },
    { id: 'payment', title: 'Payments', description: 'Payment terms', fields: ['has_paid_services', 'has_subscriptions'] },
    { id: 'content', title: 'User Content', description: 'Content policies', fields: ['allows_user_content', 'moderates_content'] },
    { id: 'legal', title: 'Legal', description: 'Legal settings', fields: ['jurisdiction', 'has_arbitration'] },
    { id: 'review', title: 'Review', description: 'Review and generate', fields: [] },
  ],
  cookie: [
    { id: 'business', title: 'Business Info', description: 'Company details', fields: ['company_name', 'website_url', 'contact_email'] },
    { id: 'types', title: 'Cookie Types', description: 'Types of cookies used', fields: ['uses_essential_cookies', 'uses_functional_cookies'] },
    { id: 'analytics', title: 'Analytics', description: 'Analytics providers', fields: ['uses_google_analytics', 'uses_mixpanel'] },
    { id: 'consent', title: 'Consent', description: 'Cookie consent', fields: ['has_cookie_consent', 'honors_dnt'] },
    { id: 'review', title: 'Review', description: 'Review and generate', fields: [] },
  ],
  eula: [
    { id: 'business', title: 'Business Info', description: 'Company details', fields: ['company_name', 'app_name', 'contact_email'] },
    { id: 'license', title: 'License Terms', description: 'License details', fields: ['license_type', 'is_subscription'] },
    { id: 'restrictions', title: 'Restrictions', description: 'Usage restrictions', fields: ['no_reverse_engineering', 'no_modification'] },
    { id: 'warranty', title: 'Warranty', description: 'Warranty terms', fields: ['has_warranty', 'has_export_restrictions'] },
    { id: 'review', title: 'Review', description: 'Review and generate', fields: [] },
  ],
  refund: [
    { id: 'business', title: 'Business Info', description: 'Company details', fields: ['company_name', 'website_url', 'contact_email'] },
    { id: 'settings', title: 'Refund Settings', description: 'General refund policy', fields: ['refund_business_type', 'refund_period_days'] },
    { id: 'returns', title: 'Returns', description: 'Return details', fields: ['return_period', 'requires_receipt'] },
    { id: 'review', title: 'Review', description: 'Review and generate', fields: [] },
  ],
};

interface WizardState {
  docType: DocumentType | null;
  currentStep: number;
  completedSteps: Set<number>;
  steps: WizardStep[];

  // Actions
  setDocType: (type: DocumentType) => void;
  nextStep: () => void;
  prevStep: () => void;
  goToStep: (step: number) => void;
  markStepComplete: (step: number) => void;
  reset: () => void;
}

export const useWizardStore = create<WizardState>((set, get) => ({
  docType: null,
  currentStep: 0,
  completedSteps: new Set(),
  steps: [],

  setDocType: (type: DocumentType) => {
    set({
      docType: type,
      currentStep: 0,
      completedSteps: new Set(),
      steps: WIZARD_STEPS[type],
    });
  },

  nextStep: () => {
    const { currentStep, steps } = get();
    if (currentStep < steps.length - 1) {
      set((state) => ({
        currentStep: state.currentStep + 1,
        completedSteps: new Set([...state.completedSteps, currentStep]),
      }));
    }
  },

  prevStep: () => {
    const { currentStep } = get();
    if (currentStep > 0) {
      set({ currentStep: currentStep - 1 });
    }
  },

  goToStep: (step: number) => {
    const { steps, completedSteps, currentStep } = get();
    // Can only go to completed steps or the next step
    if (step >= 0 && step < steps.length && (completedSteps.has(step) || step === currentStep || step === currentStep + 1)) {
      set({ currentStep: step });
    }
  },

  markStepComplete: (step: number) => {
    set((state) => ({
      completedSteps: new Set([...state.completedSteps, step]),
    }));
  },

  reset: () => {
    set({
      docType: null,
      currentStep: 0,
      completedSteps: new Set(),
      steps: [],
    });
  },
}));

export { WIZARD_STEPS };
