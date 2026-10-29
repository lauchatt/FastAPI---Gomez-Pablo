import React, { useState, useEffect } from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const ErrorBanner: React.FC = () => {
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);
  const [checking, setChecking] = useState<boolean>(false);

  const checkApi = async () => {
    setChecking(true);
    const baseUrl = import.meta.env.VITE_API_BASE_URL || '';
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 2000);
      let res = await fetch(`${baseUrl}/questions`, { signal: controller.signal }).catch(() => null);
      if (!res || !res.ok) {
        res = await fetch(`${baseUrl}/questions/category/geografia`, { signal: controller.signal }).catch(() => null);
      }
      clearTimeout(timeoutId);
      setApiOnline(res ? true : false);
    } catch {
      setApiOnline(false);
    } finally {
      setChecking(false);
    }
  };

  useEffect(() => {
    checkApi();
  }, []);

  if (apiOnline === true) return null; // Hide if connected

  return (
    <div className="bg-amber-500/90 text-amber-950 px-4 py-2 text-sm font-semibold flex items-center justify-between shadow-md">
      <div className="flex items-center gap-2">
        <AlertCircle className="w-5 h-5 flex-shrink-0 animate-pulse" />
        <span>
          Backend FastAPI no detectado en <code>http://localhost:8000</code>. Usando modo de desarrollo local (UI interactiva).
        </span>
      </div>
      <button 
        onClick={checkApi} 
        disabled={checking}
        className="flex items-center gap-1 bg-amber-950 text-amber-100 px-3 py-1 rounded hover:bg-amber-900 transition-colors text-xs"
      >
        <RefreshCw className={`w-3.5 h-3.5 ${checking ? 'animate-spin' : ''}`} />
        Verificar conexión
      </button>
    </div>
  );
};
