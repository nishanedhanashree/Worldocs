/**
 * Worldocs Frontend Configuration
 * 
 * Instructions:
 * 1. Deploy your backend (app.py) to a service like Render.com.
 * 2. Copy the URL of your deployed backend (e.g., https://worldocs-backend.onrender.com).
 * 3. Replace the placeholder below with your actual backend URL.
 */

const CONFIG = {
    // 1. YOUR RENDER URL: Replace this with your actual deployed backend URL from Render
    // Example: "https://worldocs-backend.onrender.com"
    API_BASE_URL: "https://worldocs.onrender.com",

    // 2. Dynamic API URL Selection
    get API_URL() {
        const hostname = window.location.hostname;
        
        // If running locally
        if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.startsWith('192.168.')) {
            return 'http://127.0.0.1:8000';
        }
        
        // If deployed on Render (same domain as backend)
        if (hostname.endsWith('.onrender.com')) {
            return `https://${hostname}`;
        }
        
        // Default to the configured base URL (for GitHub Pages, etc.)
        return this.API_BASE_URL;
    },

    // WebSocket helper
    get WS_URL() {
        return this.API_URL.replace(/^http/, 'ws');
    }
};

window.API_CONFIG = CONFIG;
