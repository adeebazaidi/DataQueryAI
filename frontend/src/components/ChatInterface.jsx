import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Database, FileText } from 'lucide-react';
import { chatService } from '../services/api';

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(userMsg.content);
      const aiMsg = {
        role: 'ai',
        content: response.answer,
        queryType: response.query_type,
        sources: response.sources,
        sqlQuery: response.sql_query
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', content: 'Sorry, there was an error processing your request.', isError: true }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-surface-50">
      <header className="bg-white border-b border-surface-200 px-6 py-4 flex items-center justify-between">
        <h2 className="text-xl font-bold text-surface-800">Chat Session</h2>
        <div className="flex items-center gap-2 text-sm text-surface-500">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500"></span> System Online</span>
        </div>
      </header>
      
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-surface-400">
            <MessageSquarePlus size={48} className="mb-4 opacity-50" />
            <p>Ask a question about your documents or database...</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl rounded-2xl px-6 py-4 shadow-soft ${msg.role === 'user' ? 'bg-brand-600 text-white' : 'bg-white text-surface-800 border border-surface-200'}`}>
              
              {msg.role === 'ai' && (
                <div className="flex items-center gap-2 mb-3 text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 inline-flex px-3 py-1 rounded-full">
                  {msg.queryType === 'Database' ? <Database size={14}/> : <FileText size={14}/>}
                  {msg.queryType}
                </div>
              )}
              
              <div className="prose prose-sm max-w-none">
                {msg.content}
              </div>
              
              {msg.sqlQuery && (
                <div className="mt-4 bg-surface-800 text-surface-100 p-4 rounded-xl overflow-x-auto text-sm font-mono">
                  <div className="text-surface-400 text-xs mb-2 uppercase tracking-wide">Executed SQL</div>
                  {msg.sqlQuery}
                </div>
              )}
              
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-4 pt-4 border-t border-surface-100">
                  <div className="text-surface-500 text-xs font-semibold uppercase mb-2">Sources</div>
                  <ul className="space-y-1">
                    {msg.sources.map((src, i) => (
                      <li key={i} className="text-sm text-surface-600 flex items-center gap-2">
                        <FileText size={14} className="text-brand-500" />
                        <span>{src.filename} — Page {src.page}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white text-surface-800 border border-surface-200 rounded-2xl px-6 py-4 shadow-soft flex items-center gap-3">
              <Loader2 size={20} className="animate-spin text-brand-500" />
              <span className="text-surface-500 animate-pulse">Analyzing query...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-6 bg-white border-t border-surface-200">
        <form onSubmit={handleSend} className="relative max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask about leave policies, employee counts, etc..."
            className="w-full pl-6 pr-14 py-4 bg-surface-50 border border-surface-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all shadow-inner"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-brand-600 text-white rounded-xl hover:bg-brand-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}

// Need to import MessageSquarePlus for the empty state
import { MessageSquarePlus } from 'lucide-react';
