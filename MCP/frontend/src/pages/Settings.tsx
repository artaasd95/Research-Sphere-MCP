import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  Slider,
  TextField,
  Button,
  Divider,
  Alert,
  Snackbar,
} from '@mui/material';

interface Settings {
  maxSections: number;
  maxDocs: number;
  apiKey: string;
  debugMode: boolean;
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<Settings>({
    maxSections: 5,
    maxDocs: 8,
    apiKey: localStorage.getItem('apiKey') || '',
    debugMode: false,
  });

  const [showSuccess, setShowSuccess] = useState(false);

  const handleChange = (field: keyof Settings) => (
    event: React.ChangeEvent<HTMLInputElement> | Event,
    value?: number | boolean
  ) => {
    if (field === 'apiKey') {
      const inputEvent = event as React.ChangeEvent<HTMLInputElement>;
      setSettings((prev) => ({ ...prev, [field]: inputEvent.target.value }));
    } else {
      setSettings((prev) => ({ ...prev, [field]: value }));
    }
  };

  const handleSave = () => {
    // Save settings to localStorage
    localStorage.setItem('apiKey', settings.apiKey);
    localStorage.setItem('settings', JSON.stringify(settings));
    setShowSuccess(true);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            RAG Pipeline Configuration
          </Typography>
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>Maximum Sections</Typography>
            <Slider
              value={settings.maxSections}
              onChange={handleChange('maxSections')}
              min={1}
              max={10}
              marks
              valueLabelDisplay="auto"
            />
          </Box>
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>Maximum Documents</Typography>
            <Slider
              value={settings.maxDocs}
              onChange={handleChange('maxDocs')}
              min={1}
              max={20}
              marks
              valueLabelDisplay="auto"
            />
          </Box>
        </CardContent>
      </Card>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            API Configuration
          </Typography>
          <Box sx={{ mb: 3 }}>
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={settings.apiKey}
              onChange={handleChange('apiKey') as any}
              helperText="Your OpenAI API key for the RAG system"
            />
          </Box>
          <FormControlLabel
            control={
              <Switch
                checked={settings.debugMode}
                onChange={handleChange('debugMode')}
              />
            }
            label="Debug Mode"
          />
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button variant="contained" onClick={handleSave}>
          Save Settings
        </Button>
      </Box>

      <Snackbar
        open={showSuccess}
        autoHideDuration={3000}
        onClose={() => setShowSuccess(false)}
      >
        <Alert severity="success" sx={{ width: '100%' }}>
          Settings saved successfully!
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Settings; 