export type ThemeMode = 'light' | 'dark';

export interface QueryResponse {
  answer: string;
  sections: string[];
  documents_used: number;
  processing_time: number;
  timestamp: string;
}

export interface Settings {
  maxSections: number;
  maxDocs: number;
  apiKey: string;
  debugMode: boolean;
} 