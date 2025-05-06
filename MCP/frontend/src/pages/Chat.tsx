import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Paper,
  Divider,
} from '@mui/material';
import { useQuery } from 'react-query';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface QueryResponse {
  answer: string;
  sections: string[];
  documents_used: number;
  processing_time: number;
  timestamp: string;
}

const Chat: React.FC = () => {
  const [query, setQuery] = useState('');
  const [submittedQuery, setSubmittedQuery] = useState('');

  const { data, isLoading, error } = useQuery<QueryResponse>(
    ['query', submittedQuery],
    async () => {
      if (!submittedQuery) return null;
      const response = await axios.post('http://localhost:8000/api/v1/rag/query', {
        query: submittedQuery,
      });
      return response.data;
    },
    {
      enabled: !!submittedQuery,
    }
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setSubmittedQuery(query);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      <Paper
        component="form"
        onSubmit={handleSubmit}
        sx={{
          p: 2,
          mb: 3,
          display: 'flex',
          gap: 2,
        }}
      >
        <TextField
          fullWidth
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question..."
          variant="outlined"
          size="small"
        />
        <Button
          type="submit"
          variant="contained"
          disabled={!query.trim() || isLoading}
        >
          {isLoading ? <CircularProgress size={24} /> : 'Ask'}
        </Button>
      </Paper>

      {error && (
        <Card sx={{ mb: 3, bgcolor: 'error.light' }}>
          <CardContent>
            <Typography color="error">
              Error: {error instanceof Error ? error.message : 'An error occurred'}
            </Typography>
          </CardContent>
        </Card>
      )}

      {data && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Response
            </Typography>
            <Box sx={{ mb: 2 }}>
              <ReactMarkdown
                components={{
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '');
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        {...props}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                }}
              >
                {data.answer}
              </ReactMarkdown>
            </Box>
            <Divider sx={{ my: 2 }} />
            <Box sx={{ display: 'flex', justifyContent: 'space-between', color: 'text.secondary' }}>
              <Typography variant="body2">
                Documents used: {data.documents_used}
              </Typography>
              <Typography variant="body2">
                Processing time: {data.processing_time.toFixed(2)}s
              </Typography>
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default Chat; 