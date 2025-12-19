import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { useSessionStore } from '../store/sessionStore';
import { documentsApi } from '../api/client';
import { DOCUMENT_INFO, DocumentType } from '../types';

type ViewFormat = 'markdown' | 'html';

export default function Preview() {
  const [searchParams] = useSearchParams();
  const { sessionId, generatedDocs } = useSessionStore();
  const [activeDoc, setActiveDoc] = useState<DocumentType>('privacy');
  const [viewFormat, setViewFormat] = useState<ViewFormat>('markdown');
  const [previewContent, setPreviewContent] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [copying, setCopying] = useState(false);

  const docTypes = searchParams.get('docs')?.split(',') as DocumentType[] || ['privacy'];

  useEffect(() => {
    if (docTypes.length > 0 && !docTypes.includes(activeDoc)) {
      setActiveDoc(docTypes[0]);
    }
  }, [docTypes]);

  useEffect(() => {
    const fetchPreview = async () => {
      if (!sessionId || !activeDoc) return;

      // Check if we already have the content
      if (previewContent[activeDoc]) return;

      setLoading(true);
      try {
        const response = await documentsApi.preview(sessionId, activeDoc);
        setPreviewContent(prev => ({
          ...prev,
          [activeDoc]: response.content
        }));
      } catch (error) {
        console.error('Failed to fetch preview:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPreview();
  }, [sessionId, activeDoc]);

  const handleDownload = async (format: 'md' | 'html') => {
    if (!generatedDocs[activeDoc]) return;

    const filename = generatedDocs[activeDoc][format === 'md' ? 'markdown' : 'html'];
    if (!filename) return;

    try {
      const blob = await documentsApi.download(filename);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  const handleDownloadAll = async () => {
    for (const docType of docTypes) {
      const doc = generatedDocs[docType];
      if (doc?.markdown) {
        try {
          const blob = await documentsApi.download(doc.markdown);
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = doc.markdown;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
        } catch (error) {
          console.error(`Download failed for ${docType}:`, error);
        }
      }
    }
  };

  const handleCopy = async () => {
    const content = previewContent[activeDoc];
    if (!content) return;

    try {
      await navigator.clipboard.writeText(content);
      setCopying(true);
      setTimeout(() => setCopying(false), 2000);
    } catch (error) {
      console.error('Copy failed:', error);
    }
  };

  const currentContent = previewContent[activeDoc] || '';

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Generated Documents</h1>
          <p className="text-gray-600 mt-1">
            {docTypes.length} document{docTypes.length > 1 ? 's' : ''} generated successfully
          </p>
        </div>
        <div className="flex gap-3">
          <Link
            to="/"
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Generate More
          </Link>
          {docTypes.length > 1 && (
            <button
              onClick={handleDownloadAll}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download All
            </button>
          )}
        </div>
      </div>

      <div className="grid lg:grid-cols-4 gap-6">
        {/* Document Tabs */}
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="font-semibold text-gray-800 mb-4">Documents</h2>
            <div className="space-y-2">
              {docTypes.map((docType) => {
                const info = DOCUMENT_INFO[docType];
                const isActive = activeDoc === docType;
                return (
                  <button
                    key={docType}
                    onClick={() => setActiveDoc(docType)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-primary-100 text-primary-700 border border-primary-200'
                        : 'hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <div className="font-medium">{info.title}</div>
                    {generatedDocs[docType] && (
                      <div className="text-xs text-green-600 mt-1 flex items-center gap-1">
                        <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                        Generated
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Download Options */}
          {generatedDocs[activeDoc] && (
            <div className="card mt-4">
              <h2 className="font-semibold text-gray-800 mb-4">Download</h2>
              <div className="space-y-2">
                <button
                  onClick={() => handleDownload('md')}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Markdown (.md)
                </button>
                <button
                  onClick={() => handleDownload('html')}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  HTML (.html)
                </button>
                <button
                  onClick={handleCopy}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
                >
                  {copying ? (
                    <>
                      <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-green-600">Copied!</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      Copy to Clipboard
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Preview Area */}
        <div className="lg:col-span-3">
          <div className="card">
            {/* Format Toggle */}
            <div className="flex items-center justify-between mb-4 pb-4 border-b">
              <h2 className="font-semibold text-gray-800">
                {DOCUMENT_INFO[activeDoc]?.title || 'Document'} Preview
              </h2>
              <div className="flex bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewFormat('markdown')}
                  className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                    viewFormat === 'markdown'
                      ? 'bg-white text-gray-800 shadow-sm'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Preview
                </button>
                <button
                  onClick={() => setViewFormat('html')}
                  className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                    viewFormat === 'html'
                      ? 'bg-white text-gray-800 shadow-sm'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Raw
                </button>
              </div>
            </div>

            {/* Content */}
            {loading ? (
              <div className="flex items-center justify-center py-20">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>
            ) : currentContent ? (
              <div className="prose prose-gray max-w-none">
                {viewFormat === 'markdown' ? (
                  <ReactMarkdown>{currentContent}</ReactMarkdown>
                ) : (
                  <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{currentContent}</code>
                  </pre>
                )}
              </div>
            ) : (
              <div className="text-center py-20 text-gray-500">
                <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p>No preview available</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
