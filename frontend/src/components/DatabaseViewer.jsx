import { useState, useEffect } from 'react';
import { Database, Table as TableIcon, LayoutList } from 'lucide-react';
import { databaseService } from '../services/api';

export default function DatabaseViewer() {
  const [schema, setSchema] = useState({});

  useEffect(() => {
    fetchSchema();
  }, []);

  const fetchSchema = async () => {
    try {
      const data = await databaseService.getSchema();
      setSchema(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 p-8 bg-surface-50 overflow-y-auto">
      <div className="max-w-5xl mx-auto space-y-8">
        
        <div>
          <h2 className="text-2xl font-bold text-surface-900">Database Schema Explorer</h2>
          <p className="text-surface-500 mt-1">Overview of the enterprise SQL tables available for querying</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(schema).map(([tableName, columns]) => (
            <div key={tableName} className="bg-white rounded-2xl shadow-soft border border-surface-200 overflow-hidden">
              <div className="bg-surface-50 px-6 py-4 border-b border-surface-200 flex items-center gap-3">
                <TableIcon className="text-brand-600" size={20} />
                <h3 className="font-bold text-surface-800 text-lg">{tableName}</h3>
              </div>
              <div className="p-6">
                <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-surface-400 mb-3">
                  <LayoutList size={14} />
                  Columns ({columns.length})
                </div>
                <div className="flex flex-wrap gap-2">
                  {columns.map(col => (
                    <span 
                      key={col} 
                      className="px-3 py-1.5 bg-brand-50 text-brand-700 rounded-lg text-sm font-medium border border-brand-100"
                    >
                      {col}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
          {Object.keys(schema).length === 0 && (
            <div className="col-span-full py-12 text-center bg-white rounded-2xl border border-dashed border-surface-300">
              <p className="text-surface-500">No database tables found or connection failed.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
