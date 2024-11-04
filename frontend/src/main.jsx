import React from 'react'
import ReactDOM from 'react-dom/client'
import { CartProvider } from 'react-use-cart';
import App from './App.jsx'
import './index.css'


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    
    <CartProvider>
      <App />
    </CartProvider>
  
  </React.StrictMode>,
)
