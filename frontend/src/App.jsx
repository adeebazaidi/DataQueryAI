import { useState } from 'react';
import { MessageSquare, FileText, Database, Clock, LayoutDashboard } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import DocumentManager from './components/DocumentManager';
import DatabaseViewer from './components/DatabaseViewer';

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <div className="flex h-screen bg-surface-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-surface-200 flex flex-col">
        <div className="p-6">
          <div className="flex items-center gap-2 text-brand-600 mb-2">
            <LayoutDashboard size={24} className="font-bold" />
            <h1 className="text-xl font-bold">DataQuery AI</h1>
          </div>
          <p className="text-xs text-surface-500 font-medium">Enterprise Assistant</p>
        </div>
        
        <nav className="flex-1 px-4 space-y-2">
          <button 
            onClick={() => setActiveTab('chat')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'chat' ? 'bg-brand-50 text-brand-700' : 'text-surface-600 hover:bg-surface-100'}`}
          >
            <MessageSquare size={20} />
            <span className="font-medium">Chat</span>
          </button>
          <button 
            onClick={() => setActiveTab('documents')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'documents' ? 'bg-brand-50 text-brand-700' : 'text-surface-600 hover:bg-surface-100'}`}
          >
            <FileText size={20} />
            <span className="font-medium">Documents</span>
          </button>
          <button 
            onClick={() => setActiveTab('database')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'database' ? 'bg-brand-50 text-brand-700' : 'text-surface-600 hover:bg-surface-100'}`}
          >
            <Database size={20} />
            <span className="font-medium">Database</span>
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {activeTab === 'chat' && <ChatInterface />}
        {activeTab === 'documents' && <DocumentManager />}
        {activeTab === 'database' && <DatabaseViewer />}
      </main>
    </div>
  );
}

export default App;
