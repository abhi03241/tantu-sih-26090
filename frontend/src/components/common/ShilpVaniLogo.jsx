import React from 'react';

export default function ShilpVaniLogo({ size = 24, className = '', style = {} }) {
  const dimension = typeof size === 'number' ? `${size}px` : size;
  return (
    <img
      src="/shilpvani_logo.jpg"
      alt="ShilpVani Logo"
      style={{
        width: dimension,
        height: dimension,
        objectFit: 'contain',
        borderRadius: '8px',
        display: 'inline-block',
        verticalAlign: 'middle',
        ...style
      }}
      className={`shilpvani-official-logo ${className}`}
    />
  );
}
