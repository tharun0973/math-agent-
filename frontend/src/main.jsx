import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import 'katex/dist/katex.min.css'; // ✅ Enables math rendering

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
