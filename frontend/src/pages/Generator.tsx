import { useParams, useNavigate, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useSessionStore } from '../store/sessionStore';
import { useWizardStore, WIZARD_STEPS } from '../store/wizardStore';
import { documentsApi } from '../api/client';
import { DocumentType, DOCUMENT_INFO, DocumentConfig, OutputFormat } from '../types';
import clsx from 'clsx';

// Form field components
function TextField({ label, name, value, onChange, placeholder, required }: {
  label: string;
  name: string;
  value: string;
  onChange: (name: string, value: string) => void;
  placeholder?: string;
  required?: boolean;
}) {
  return (
    <div>
      <label className="form-label">{label} {required && <span className="text-red-500">*</span>}</label>
      <input
        type="text"
        className="form-input"
        value={value || ''}
        onChange={(e) => onChange(name, e.target.value)}
        placeholder={placeholder}
        required={required}
      />
    </div>
  );
}

function CheckboxField({ label, name, checked, onChange, description }: {
  label: string;
  name: string;
  checked: boolean;
  onChange: (name: string, value: boolean) => void;
  description?: string;
}) {
  return (
    <label className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
      <input
        type="checkbox"
        className="form-checkbox mt-1"
        checked={checked || false}
        onChange={(e) => onChange(name, e.target.checked)}
      />
      <div>
        <span className="text-gray-700 font-medium">{label}</span>
        {description && <p className="text-sm text-gray-500">{description}</p>}
      </div>
    </label>
  );
}

function SelectField({ label, name, value, onChange, options }: {
  label: string;
  name: string;
  value: string;
  onChange: (name: string, value: string) => void;
  options: { value: string; label: string }[];
}) {
  return (
    <div>
      <label className="form-label">{label}</label>
      <select
        className="form-input"
        value={value || ''}
        onChange={(e) => onChange(name, e.target.value)}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  );
}

// Step form components
function BusinessInfoStep({ config, onChange }: { config: DocumentConfig; onChange: (name: string, value: any) => void }) {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="grid md:grid-cols-2 gap-6">
        <TextField label="Company Name" name="company_name" value={config.company_name} onChange={onChange} placeholder="Acme Inc." required />
        <SelectField
          label="Platform Type"
          name="platform_type"
          value={config.platform_type}
          onChange={onChange}
          options={[
            { value: 'website', label: 'Website' },
            { value: 'app', label: 'Mobile App' },
            { value: 'both', label: 'Both Website & App' },
          ]}
        />
        <TextField label="Website URL" name="website_url" value={config.website_url} onChange={onChange} placeholder="https://example.com" />
        <TextField label="Website Name" name="website_name" value={config.website_name} onChange={onChange} placeholder="Example.com" />
        <TextField label="App Name" name="app_name" value={config.app_name} onChange={onChange} placeholder="My App" />
        <TextField label="Country" name="country" value={config.country} onChange={onChange} placeholder="United States" />
      </div>
      <TextField label="Company Address" name="company_address" value={config.company_address} onChange={onChange} placeholder="123 Main St, City, State, ZIP" />
      <div className="grid md:grid-cols-2 gap-6">
        <TextField label="Contact Email" name="contact_email" value={config.contact_email} onChange={onChange} placeholder="legal@example.com" required />
        <TextField label="Contact Phone" name="contact_phone" value={config.contact_phone} onChange={onChange} placeholder="+1 (555) 123-4567" />
      </div>
    </div>
  );
}

function DataCollectionStep({ config, onChange }: { config: DocumentConfig; onChange: (name: string, value: any) => void }) {
  return (
    <div className="space-y-4 animate-fade-in">
      <p className="text-gray-600 mb-4">What personal information do you collect from users?</p>
      <div className="grid md:grid-cols-3 gap-4">
        <CheckboxField label="Name" name="collects_name" checked={config.collects_name} onChange={onChange} />
        <CheckboxField label="Email Address" name="collects_email" checked={config.collects_email} onChange={onChange} />
        <CheckboxField label="Phone Number" name="collects_phone" checked={config.collects_phone} onChange={onChange} />
        <CheckboxField label="Physical Address" name="collects_address" checked={config.collects_address} onChange={onChange} />
        <CheckboxField label="Billing Address" name="collects_billing_address" checked={config.collects_billing_address} onChange={onChange} />
        <CheckboxField label="Payment Info" name="collects_payment_info" checked={config.collects_payment_info} onChange={onChange} />
        <CheckboxField label="Age/DOB" name="collects_age" checked={config.collects_age} onChange={onChange} />
        <CheckboxField label="Username" name="collects_username" checked={config.collects_username} onChange={onChange} />
        <CheckboxField label="Password" name="collects_password" checked={config.collects_password} onChange={onChange} />
      </div>
    </div>
  );
}

function TrackingStep({ config, onChange }: { config: DocumentConfig; onChange: (name: string, value: any) => void }) {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h3 className="text-lg font-medium mb-4">Tracking Technologies</h3>
        <div className="grid md:grid-cols-3 gap-4">
          <CheckboxField label="Cookies" name="uses_cookies" checked={config.uses_cookies} onChange={onChange} />
          <CheckboxField label="Sessions" name="uses_sessions" checked={config.uses_sessions} onChange={onChange} />
          <CheckboxField label="Local Storage" name="uses_local_storage" checked={config.uses_local_storage} onChange={onChange} />
          <CheckboxField label="Web Beacons" name="uses_web_beacons" checked={config.uses_web_beacons} onChange={onChange} />
          <CheckboxField label="Google Maps" name="uses_google_maps" checked={config.uses_google_maps} onChange={onChange} />
        </div>
      </div>
      <div>
        <h3 className="text-lg font-medium mb-4">Analytics</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <CheckboxField label="Uses Analytics" name="uses_analytics" checked={config.uses_analytics} onChange={onChange} />
          <TextField label="Analytics Provider" name="analytics_provider" value={config.analytics_provider} onChange={onChange} placeholder="Google Analytics" />
        </div>
      </div>
    </div>
  );
}

function SocialLoginStep({ config, onChange }: { config: DocumentConfig; onChange: (name: string, value: any) => void }) {
  return (
    <div className="space-y-4 animate-fade-in">
      <p className="text-gray-600 mb-4">Which social login options do you offer?</p>
      <div className="grid md:grid-cols-3 gap-4">
        <CheckboxField label="Google" name="social_login_google" checked={config.social_login_google} onChange={onChange} />
        <CheckboxField label="Facebook" name="social_login_facebook" checked={config.social_login_facebook} onChange={onChange} />
        <CheckboxField label="Twitter" name="social_login_twitter" checked={config.social_login_twitter} onChange={onChange} />
        <CheckboxField label="GitHub" name="social_login_github" checked={config.social_login_github} onChange={onChange} />
        <CheckboxField label="LinkedIn" name="social_login_linkedin" checked={config.social_login_linkedin} onChange={onChange} />
      </div>
    </div>
  );
}

function MarketingStep({ config, onChange }: { config: DocumentConfig; onChange: (name: string, value: any) => void }) {
  return (
    <div className="space-y-4 animate-fade-in">
      <p className="text-gray-600 mb-4">Marketing and advertising settings</p>
      <div className="grid md:grid-cols-2 gap-4">
        <CheckboxField label="Email Newsletter" name="has_email_newsletter" checked={config.has_email_newsletter} onChange={onChange} description="Do you send marketing emails?" />
        <CheckboxField label="Display Ads" name="displays_ads" checked={config.displays_ads} onChange={onChange} description="Do you show advertisements?" />
        <CheckboxField label="Facebook Pixel" name="uses_facebook_pixel" checked={config.uses_facebook_pixel} onChange={onChange} />
        <CheckboxField label="Retargeting" name="uses_retargeting" checked={config.uses_retargeting} onChange={onChange} />
      </div>
    </div>
  );
}

function ComplianceStep({ config, onChange }: { config: DocumentConfig; onChange: (name: string, value: any) => void }) {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h3 className="text-lg font-medium mb-4">Compliance Frameworks</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <CheckboxField label="GDPR Compliant" name="gdpr_compliant" checked={config.gdpr_compliant} onChange={onChange} description="European data protection" />
          <CheckboxField label="CCPA Compliant" name="ccpa_compliant" checked={config.ccpa_compliant} onChange={onChange} description="California privacy law" />
          <CheckboxField label="CalOPPA Compliant" name="caloppa_compliant" checked={config.caloppa_compliant} onChange={onChange} />
          <CheckboxField label="COPPA Compliant" name="coppa_compliant" checked={config.coppa_compliant} onChange={onChange} description="Children's privacy" />
        </div>
      </div>
      <div>
        <h3 className="text-lg font-medium mb-4">User Rights</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <CheckboxField label="Data Access" name="allows_data_access" checked={config.allows_data_access} onChange={onChange} />
          <CheckboxField label="Data Deletion" name="allows_data_deletion" checked={config.allows_data_deletion} onChange={onChange} />
          <CheckboxField label="Data Portability" name="allows_data_portability" checked={config.allows_data_portability} onChange={onChange} />
          <CheckboxField label="Opt Out" name="allows_opt_out" checked={config.allows_opt_out} onChange={onChange} />
        </div>
      </div>
    </div>
  );
}

function ReviewStep({ config, docType, onGenerate, isGenerating }: {
  config: DocumentConfig;
  docType: DocumentType;
  onGenerate: (format: OutputFormat) => void;
  isGenerating: boolean;
}) {
  const [format, setFormat] = useState<OutputFormat>('markdown');
  const info = DOCUMENT_INFO[docType];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="bg-gray-50 rounded-xl p-6">
        <h3 className="text-lg font-semibold mb-4">Configuration Summary</h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Company:</span>
            <span className="ml-2 font-medium">{config.company_name || 'Not set'}</span>
          </div>
          <div>
            <span className="text-gray-500">Website:</span>
            <span className="ml-2 font-medium">{config.website_url || 'Not set'}</span>
          </div>
          <div>
            <span className="text-gray-500">Contact:</span>
            <span className="ml-2 font-medium">{config.contact_email || 'Not set'}</span>
          </div>
          <div>
            <span className="text-gray-500">Platform:</span>
            <span className="ml-2 font-medium capitalize">{config.platform_type}</span>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <label className="text-gray-700 font-medium">Output Format:</label>
        <select
          className="form-input w-40"
          value={format}
          onChange={(e) => setFormat(e.target.value as OutputFormat)}
        >
          <option value="markdown">Markdown</option>
          <option value="html">HTML</option>
        </select>
      </div>

      <button
        onClick={() => onGenerate(format)}
        disabled={isGenerating}
        className="btn-primary w-full py-4 text-lg"
      >
        {isGenerating ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Generating...
          </span>
        ) : (
          `Generate ${info.title}`
        )}
      </button>
    </div>
  );
}

// Main Generator component
export default function Generator() {
  const { docType } = useParams<{ docType: string }>();
  const navigate = useNavigate();
  const { sessionId, config, updateConfig, saveConfig, setGeneratedDocs } = useSessionStore();
  const { currentStep, steps, setDocType, nextStep, prevStep } = useWizardStore();
  const [isGenerating, setIsGenerating] = useState(false);

  // Handle 'all' as a special case
  const isAllDocs = docType === 'all';
  const validDocType = isAllDocs ? 'privacy' : (docType as DocumentType);
  const info = !isAllDocs && validDocType ? DOCUMENT_INFO[validDocType] : null;

  useEffect(() => {
    if (validDocType && WIZARD_STEPS[validDocType]) {
      setDocType(validDocType);
    }
  }, [validDocType, setDocType]);

  const handleFieldChange = (name: string, value: any) => {
    updateConfig({ [name]: value } as Partial<DocumentConfig>);
  };

  const handleGenerate = async (format: OutputFormat) => {
    if (!sessionId || !validDocType) return;

    setIsGenerating(true);
    try {
      // Save config first
      await saveConfig();

      // Generate document(s)
      const docTypes: DocumentType[] = isAllDocs
        ? ['privacy', 'tos', 'cookie', 'eula', 'refund']
        : [validDocType];

      const response = await documentsApi.generate(sessionId, docTypes, format);
      setGeneratedDocs(response.documents);

      // Navigate to preview with doc types as query param
      const docsParam = docTypes.join(',');
      navigate(`/preview?docs=${docsParam}`);
    } catch (error) {
      console.error('Generation failed:', error);
      alert('Failed to generate document. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  if (!config || !steps.length) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  const currentStepData = steps[currentStep];

  const renderStep = () => {
    switch (currentStepData.id) {
      case 'business':
        return <BusinessInfoStep config={config} onChange={handleFieldChange} />;
      case 'data':
        return <DataCollectionStep config={config} onChange={handleFieldChange} />;
      case 'tracking':
        return <TrackingStep config={config} onChange={handleFieldChange} />;
      case 'social':
        return <SocialLoginStep config={config} onChange={handleFieldChange} />;
      case 'marketing':
        return <MarketingStep config={config} onChange={handleFieldChange} />;
      case 'compliance':
        return <ComplianceStep config={config} onChange={handleFieldChange} />;
      case 'review':
        return <ReviewStep config={config} docType={validDocType} onGenerate={handleGenerate} isGenerating={isGenerating} />;
      default:
        return <BusinessInfoStep config={config} onChange={handleFieldChange} />;
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <Link to="/" className="text-primary-600 hover:text-primary-700 flex items-center mb-4">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </Link>
        <h1 className="text-3xl font-bold text-gray-800">
          {isAllDocs ? 'Complete Legal Package' : `${info?.title || 'Document'} Generator`}
        </h1>
        {isAllDocs ? (
          <p className="text-gray-600 mt-2">Generate all 5 legal documents at once</p>
        ) : (
          info && <p className="text-gray-600 mt-2">{info.description}</p>
        )}
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <div
                className={clsx(
                  'step-indicator',
                  index < currentStep && 'completed',
                  index === currentStep && 'active',
                  index > currentStep && 'pending'
                )}
              >
                {index < currentStep ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <span>{index + 1}</span>
                )}
              </div>
              {index < steps.length - 1 && (
                <div
                  className={clsx(
                    'h-1 w-12 md:w-24 mx-2',
                    index < currentStep ? 'bg-green-500' : 'bg-gray-200'
                  )}
                />
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-between mt-2 text-sm text-gray-500">
          {steps.map((step) => (
            <span key={step.id} className="text-center w-16 md:w-24">{step.title}</span>
          ))}
        </div>
      </div>

      {/* Step Content */}
      <div className="card mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-6">
          {currentStepData.title}
        </h2>
        {renderStep()}
      </div>

      {/* Navigation */}
      {currentStepData.id !== 'review' && (
        <div className="flex justify-between">
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className={clsx(
              'btn-secondary',
              currentStep === 0 && 'opacity-50 cursor-not-allowed'
            )}
          >
            <svg className="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Previous
          </button>
          <button
            onClick={() => {
              saveConfig();
              nextStep();
            }}
            className="btn-primary"
          >
            Next
            <svg className="w-5 h-5 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
}
