import React from 'react';
import { useApp } from '../../context/AppContext';
import { CheckCircle, AlertCircle, Info } from 'lucide-react';

export default function Toast() {
  const { toast } = useApp();

  if (!toast) return null;

  return (
    <div className="toast-floating">
      {toast.type === 'success' && <CheckCircle size={18} color="#10B981" />}
      {toast.type === 'error' && <AlertCircle size={18} color="#EF4444" />}
      {toast.type === 'info' && <Info size={18} color="#3B82F6" />}
      <span>{toast.message}</span>
    </div>
  );
}
