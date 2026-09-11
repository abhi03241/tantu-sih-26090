import React from 'react';

export default function ShilpVaniLogo({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-label="ShilpVani Logo"
    >
      <defs>
        <linearGradient id="shilpVaniEmblemGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#FFFFFF" />
          <stop offset="100%" stopColor="#FED7AA" />
        </linearGradient>
      </defs>
      {/* Traditional Indian Loom Shuttle & Acoustic Voice Resonance Curve */}
      <path
        d="M 18 50 C 18 34, 38 26, 50 26 C 62 26, 82 34, 82 50 C 82 66, 62 74, 50 74 C 38 74, 18 66, 18 50 Z"
        stroke="url(#shilpVaniEmblemGrad)"
        strokeWidth="6"
        strokeLinecap="round"
        fill="none"
      />
      {/* Central Artisan Golden Core */}
      <circle cx="50" cy="50" r="10" fill="#FFD166" />
      {/* Resonance / Thread Wave */}
      <path
        d="M 28 50 Q 50 18 72 50 Q 50 82 28 50"
        stroke="#FFFFFF"
        strokeWidth="3.5"
        strokeDasharray="4,4"
        strokeLinecap="round"
        fill="none"
      />
      {/* Sound / Radiance Spark Accent */}
      <circle cx="50" cy="30" r="3.5" fill="#FFFFFF" />
      <circle cx="50" cy="70" r="3.5" fill="#FFFFFF" />
    </svg>
  );
}
