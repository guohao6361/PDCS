import { createContext, useContext, useState, useCallback } from 'react';
import './Toast.css';

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'info') => {
    const id = Date.now() + Math.random();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3000);
  }, []);

  const confirm = useCallback((message) => {
    return new Promise((resolve) => {
      const id = Date.now() + Math.random();
      setToasts(prev => [...prev, {
        id, message, type: 'confirm',
        onConfirm: () => { setToasts(prev => prev.filter(t => t.id !== id)); resolve(true); },
        onCancel: () => { setToasts(prev => prev.filter(t => t.id !== id)); resolve(false); },
      }]);
    });
  }, []);

  return (
    <ToastContext.Provider value={{ toast: addToast, confirm }}>
      {children}
      <div className="toast-container">
        {toasts.filter(t => t.type !== 'confirm').map(t => (
          <div key={t.id} className={`toast toast-${t.type}`}>
            <div className="toast-message">
              <span className="toast-icon">
                {t.type === 'success' ? '✓' : t.type === 'error' ? '✕' : 'ℹ'}
              </span>
              <span>{t.message}</span>
            </div>
          </div>
        ))}
      </div>
      {toasts.filter(t => t.type === 'confirm').map(t => (
        <div key={t.id} className="toast-confirm-overlay" onClick={t.onCancel}>
          <div className="toast-confirm" onClick={e => e.stopPropagation()}>
            <p>{t.message}</p>
            <div className="toast-confirm-actions">
              <button className="toast-btn-cancel" onClick={t.onCancel}>取消</button>
              <button className="toast-btn-ok" onClick={t.onConfirm}>确定</button>
            </div>
          </div>
        </div>
      ))}
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);
