import { useState, useEffect } from 'react';
import { Upload, FileText, Trash2, FileSearch, Loader2 } from 'lucide-react';
import { documentService } from '../services/api';

export default function DocumentManager() {
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [summary, setSummary] = useState(null);
  const [isSummarizing, setIsSummarizing] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const docs = await documentService.getDocuments();
      setDocuments(docs);
    } catch (e) {
      console.error(e);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setIsUploading(true);
    try {
      await documentService.uploadDocument(file);
      await fetchDocuments();
    } catch (e) {
      alert('Failed to upload document');
    } finally {
      setIsUploading(false);
      e.target.value = null; // reset
    }
  };

  const handleDelete = async (id) => {
    try {
      await documentService.deleteDocument(id);
      await fetchDocuments();
    } catch (e) {
      console.error(e);
    }
  };

  const handleSummarize = async (id) => {
    setIsSummarizing(true);
    setSummary(null);
    try {
      const res = await documentService.summarizeDocument(id);
      setSummary({ id, text: res.summary });
    } catch (e) {
      alert('Failed to summarize');
    } finally {
      setIsSummarizing(false);
    }
  };

  return (
    <div className="flex-1 p-8 bg-surface-50 overflow-y-auto">
      <div className="max-w-5xl mx-auto space-y-8">
        
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-surface-900">Document Knowledge Base</h2>
            <p className="text-surface-500 mt-1">Upload PDFs to enable RAG capabilities</p>
          </div>
          
          <div>
            <input
              type="file"
              id="upload-doc"
              accept=".pdf"
              className="hidden"
              onChange={handleUpload}
              disabled={isUploading}
            />
            <label 
              htmlFor="upload-doc"
              className="cursor-pointer bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-soft"
            >
              {isUploading ? <Loader2 className="animate-spin" size={20} /> : <Upload size={20} />}
              {isUploading ? 'Indexing...' : 'Upload PDF'}
            </label>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {documents.map(doc => (
            <div key={doc.id} className="bg-white rounded-2xl p-6 shadow-soft border border-surface-100 flex flex-col group hover:border-brand-200 transition-colors">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-brand-50 rounded-xl text-brand-600">
                  <FileText size={24} />
                </div>
                <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button 
                    onClick={() => handleSummarize(doc.id)}
                    className="p-2 text-surface-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="Generate Summary"
                  >
                    <FileSearch size={18} />
                  </button>
                  <button 
                    onClick={() => handleDelete(doc.id)}
                    className="p-2 text-surface-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Delete Document"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
              
              <h3 className="font-semibold text-surface-800 truncate mb-1" title={doc.filename}>{doc.filename}</h3>
              <div className="flex items-center gap-2 text-xs text-surface-500">
                <span className="w-2 h-2 rounded-full bg-green-500"></span>
                {doc.status}
              </div>
            </div>
          ))}
          {documents.length === 0 && !isUploading && (
            <div className="col-span-full py-12 text-center bg-white rounded-2xl border border-dashed border-surface-300">
              <p className="text-surface-500">No documents uploaded yet.</p>
            </div>
          )}
        </div>

        {/* Summary Modal / Section */}
        {(summary || isSummarizing) && (
          <div className="mt-12 bg-white rounded-2xl p-8 shadow-soft border border-brand-100 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-1 h-full bg-brand-500"></div>
            <h3 className="text-xl font-bold text-surface-900 mb-4 flex items-center gap-2">
              <FileSearch className="text-brand-500" />
              Document Summary
            </h3>
            {isSummarizing ? (
              <div className="flex items-center gap-3 text-surface-500">
                <Loader2 className="animate-spin text-brand-500" />
                Generating concise summary...
              </div>
            ) : (
              <div className="prose max-w-none text-surface-700">
                <pre className="whitespace-pre-wrap font-sans bg-surface-50 p-6 rounded-xl border border-surface-100">
                  {summary.text}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
