import React, { useEffect } from 'react';

interface ModalProps {
  title: string;
  children: React.ReactNode;
  onClose: () => void;
}

export const Modal: React.FC<ModalProps> = ({ title, children, onClose }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  return (
    <div
      style={styles.overlay}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose(); // Click outside modal
      }}
    >
      <div style={styles.modal}>
        <div style={styles.header}>
          <h3>{title}</h3>
          <button style={styles.closeButton} onClick={onClose}>×</button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  overlay: {
    position: 'fixed',
    top: 0, left: 0, right: 0, bottom: 0,
    background: 'rgba(0,0,0,0.5)',
    display: 'flex', justifyContent: 'center', alignItems: 'center',
    zIndex: 1000
  },
  modal: {
    background: '#fff',
    padding: '20px',
    borderRadius: '12px',
    width: '400px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px'
  },
  closeButton: {
    fontSize: '20px',
    background: 'none',
    border: 'none',
    cursor: 'pointer'
  }
};
