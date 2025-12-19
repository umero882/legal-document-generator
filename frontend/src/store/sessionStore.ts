import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { DocumentConfig, GeneratedDocument } from '../types';
import { sessionApi } from '../api/client';

// Generated docs state - maps doc type to its generated files
export interface GeneratedDocsState {
  [key: string]: {
    markdown?: string;
    html?: string;
    content?: string;
  };
}

interface SessionState {
  sessionId: string | null;
  config: DocumentConfig | null;
  isLoading: boolean;
  error: string | null;
  lastSaved: Date | null;
  generatedDocs: GeneratedDocsState;

  // Actions
  createSession: () => Promise<void>;
  loadSession: (sessionId: string) => Promise<void>;
  updateConfig: (updates: Partial<DocumentConfig>) => void;
  saveConfig: () => Promise<void>;
  resetConfig: () => Promise<void>;
  clearError: () => void;
  setGeneratedDocs: (docs: GeneratedDocument[]) => void;
  clearGeneratedDocs: () => void;
}

export const useSessionStore = create<SessionState>()(
  persist(
    (set, get) => ({
      sessionId: null,
      config: null,
      isLoading: false,
      error: null,
      lastSaved: null,
      generatedDocs: {},

      createSession: async () => {
        set({ isLoading: true, error: null });
        try {
          const session = await sessionApi.create();
          set({
            sessionId: session.session_id,
            config: session.config,
            isLoading: false,
            lastSaved: new Date(),
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to create session',
            isLoading: false,
          });
        }
      },

      loadSession: async (sessionId: string) => {
        set({ isLoading: true, error: null });
        try {
          const session = await sessionApi.get(sessionId);
          set({
            sessionId: session.session_id,
            config: session.config,
            isLoading: false,
          });
        } catch (error) {
          // Session not found, create new one
          await get().createSession();
        }
      },

      updateConfig: (updates: Partial<DocumentConfig>) => {
        const currentConfig = get().config;
        if (currentConfig) {
          set({
            config: { ...currentConfig, ...updates },
          });
        }
      },

      saveConfig: async () => {
        const { sessionId, config } = get();
        if (!sessionId || !config) return;

        set({ isLoading: true, error: null });
        try {
          await sessionApi.updateConfig(sessionId, config);
          set({ isLoading: false, lastSaved: new Date() });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to save config',
            isLoading: false,
          });
        }
      },

      resetConfig: async () => {
        const { sessionId } = get();
        if (!sessionId) return;

        set({ isLoading: true, error: null });
        try {
          const result = await sessionApi.reset(sessionId);
          set({
            config: result.config,
            isLoading: false,
            lastSaved: new Date(),
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to reset config',
            isLoading: false,
          });
        }
      },

      clearError: () => set({ error: null }),

      setGeneratedDocs: (docs: GeneratedDocument[]) => {
        const generatedDocs: GeneratedDocsState = {};
        docs.forEach((doc) => {
          if (!generatedDocs[doc.doc_type]) {
            generatedDocs[doc.doc_type] = {};
          }
          if (doc.format === 'markdown') {
            generatedDocs[doc.doc_type].markdown = doc.filename;
            generatedDocs[doc.doc_type].content = doc.content;
          } else {
            generatedDocs[doc.doc_type].html = doc.filename;
          }
        });
        set({ generatedDocs });
      },

      clearGeneratedDocs: () => set({ generatedDocs: {} }),
    }),
    {
      name: 'legal-doc-session',
      partialize: (state) => ({ sessionId: state.sessionId }),
    }
  )
);
