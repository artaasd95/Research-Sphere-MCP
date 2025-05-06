import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
  useTheme,
} from '@mui/material';
import {
  Chat as ChatIcon,
  Settings as SettingsIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  const features = [
    {
      title: 'Advanced RAG Pipeline',
      description: 'Powerful document processing and semantic search capabilities.',
      icon: <InfoIcon fontSize="large" />,
    },
    {
      title: 'Interactive Chat',
      description: 'Ask questions and get detailed, context-aware responses.',
      icon: <ChatIcon fontSize="large" />,
      action: () => navigate('/chat'),
    },
    {
      title: 'Customizable Settings',
      description: 'Configure the system to match your needs.',
      icon: <SettingsIcon fontSize="large" />,
      action: () => navigate('/settings'),
    },
  ];

  return (
    <Box>
      <Box sx={{ mb: 6, textAlign: 'center' }}>
        <Typography variant="h3" gutterBottom>
          Welcome to MCP RAG System
        </Typography>
        <Typography variant="h6" color="text.secondary">
          A powerful Retrieval-Augmented Generation system for intelligent document processing and Q&A
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {features.map((feature) => (
          <Grid item xs={12} md={4} key={feature.title}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: feature.action ? 'translateY(-4px)' : 'none',
                  cursor: feature.action ? 'pointer' : 'default',
                },
              }}
              onClick={feature.action}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ color: 'primary.main', mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography variant="h5" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<ChatIcon />}
          onClick={() => navigate('/chat')}
        >
          Start Chatting
        </Button>
      </Box>
    </Box>
  );
};

export default Home; 