import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import UploadPage from './pages/UploadPage';
import './App.css';

const App = () => {
  return (
    <Router>
      <div className="app">
        <nav>
          <ul>
            <li>
              <a href="/">Chat</a>
            </li>
            <li>
              <a href="/upload">Upload</a>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
