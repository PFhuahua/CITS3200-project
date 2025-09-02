import React from 'react';

export const WorldMapBackground = () => {
  return (
    <div className="absolute inset-0 world-map-bg overflow-hidden">
      <svg
        className="absolute inset-0 w-full h-full opacity-20"
        viewBox="0 0 1200 600"
        preserveAspectRatio="xMidYMid slice"
      >
        {/* Simplified world map paths */}
        <g fill="currentColor" className="text-white/30">
          {/* North America */}
          <path d="M120 120 L280 100 L320 180 L280 250 L200 280 L150 240 L120 180 Z" />
          {/* South America */}
          <path d="M220 300 L280 320 L300 420 L260 480 L220 460 L200 380 Z" />
          {/* Europe */}
          <path d="M480 100 L540 90 L580 120 L560 160 L500 170 L460 140 Z" />
          {/* Africa */}
          <path d="M480 180 L560 170 L580 280 L540 380 L480 360 L460 260 Z" />
          {/* Asia */}
          <path d="M580 80 L780 60 L850 140 L800 200 L720 180 L600 160 Z" />
          {/* Australia */}
          <path d="M720 320 L800 310 L820 350 L780 380 L720 370 Z" />
        </g>
        
        {/* Glowing dots for major cities/data points */}
        <g className="text-white/50">
          <circle cx="200" cy="150" r="3" fill="currentColor" className="animate-pulse" />
          <circle cx="500" cy="120" r="3" fill="currentColor" className="animate-pulse" />
          <circle cx="680" cy="140" r="3" fill="currentColor" className="animate-pulse" />
          <circle cx="750" cy="340" r="3" fill="currentColor" className="animate-pulse" />
          <circle cx="250" cy="350" r="3" fill="currentColor" className="animate-pulse" />
          <circle cx="520" cy="220" r="3" fill="currentColor" className="animate-pulse" />
        </g>
      </svg>
    </div>
  );
};