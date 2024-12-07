import React, { useState } from 'react';
import axios from 'axios';

const ChatGPT = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState('');

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {

      const response = await axios.post('http://127.0.0.1:5000/chat', {
        question: question,
      });
      setAnswer(response.data.answer);
      setError('');
    } catch (error) {
      setError('Failed to get an answer.');
    }
  };

  return (
    <div className="chat-container">
      <h2>Chat with AI Assistant</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={handleQuestionChange}
          placeholder="Ask your question here..."
          rows="4"
        />
        <button type="submit">Submit</button>
      </form>
      {answer && <div className="answer">{answer}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default ChatGPT;
