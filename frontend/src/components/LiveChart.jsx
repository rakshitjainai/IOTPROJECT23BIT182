import React, { useState } from 'react';
import { LineChart, Layers, Eye } from 'lucide-react';

export default function LiveChart({ history = [] }) {
  const [activeTab, setActiveTab] = useState('all'); // 'all' | 'climate' | 'air'
  const [hoveredIndex, setHoveredIndex] = useState(null);

  // If history is small, create a smooth visual demonstration baseline
  const data = history.length > 2 ? history : [
    { temperature: 24.5, humidity: 52.0, eco2: 420, tvoc: 45 },
    { temperature: 24.8, humidity: 52.5, eco2: 430, tvoc: 50 },
    { temperature: 25.1, humidity: 53.0, eco2: 440, tvoc: 55 }
  ];

  const width = 800;
  const height = 240;
  const padding = { top: 20, right: 30, bottom: 30, left: 45 };

  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  // Compute Scales
  const getPoints = (key, minVal, maxVal) => {
    return data.map((d, index) => {
      const val = Number(d[key]) || minVal;
      const x = padding.left + (index / Math.max(1, data.length - 1)) * plotWidth;
      const normalized = (val - minVal) / Math.max(0.1, maxVal - minVal);
      const y = padding.top + plotHeight - normalized * plotHeight;
      return { x, y, val };
    });
  };

  // Temperature (20 - 35 C)
  const tempPoints = getPoints('temperature', 15, 40);
  // Humidity (30 - 90 %)
  const humPoints = getPoints('humidity', 20, 90);
  // eCO2 (400 - 1600 ppm)
  const eco2Points = getPoints('eco2', 350, 1600);
  // TVOC (0 - 500 ppb)
  const tvocPoints = getPoints('tvoc', 0, 500);

  const makePath = (points) => {
    if (!points.length) return '';
    return points.reduce((acc, pt, i) => (i === 0 ? `M ${pt.x} ${pt.y}` : `${acc} L ${pt.x} ${pt.y}`), '');
  };

  const makeAreaPath = (points) => {
    if (!points.length) return '';
    const line = makePath(points);
    const lastX = points[points.length - 1].x;
    const firstX = points[0].x;
    const bottomY = padding.top + plotHeight;
    return `${line} L ${lastX} ${bottomY} L ${firstX} ${bottomY} Z`;
  };

  const hoveredPoint = hoveredIndex !== null && data[hoveredIndex] ? data[hoveredIndex] : null;

  return (
    <div className="glass-panel chart-panel">
      <div className="card-header-row" style={{ marginBottom: 0 }}>
        <div className="card-title">
          <LineChart size={18} />
          <span>Real-Time Environmental Trend History</span>
        </div>

        <div className="chart-tabs">
          <button
            className={`chart-tab-btn ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            All Channels
          </button>
          <button
            className={`chart-tab-btn ${activeTab === 'climate' ? 'active' : ''}`}
            onClick={() => setActiveTab('climate')}
          >
            Climate (Temp & Hum)
          </button>
          <button
            className={`chart-tab-btn ${activeTab === 'air' ? 'active' : ''}`}
            onClick={() => setActiveTab('air')}
          >
            Air Quality (eCO2 & TVOC)
          </button>
        </div>
      </div>

      {/* SVG Chart Viewport */}
      <div className="chart-viewport">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="svg-chart-container"
          onMouseLeave={() => setHoveredIndex(null)}
        >
          <defs>
            {/* Gradients */}
            <linearGradient id="gradTemp" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.0" />
            </linearGradient>
            <linearGradient id="gradHum" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#00f2fe" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#00f2fe" stopOpacity="0.0" />
            </linearGradient>
            <linearGradient id="gradEco2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#10b981" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#10b981" stopOpacity="0.0" />
            </linearGradient>
            <linearGradient id="gradTvoc" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#a855f7" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#a855f7" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => {
            const y = padding.top + pct * plotHeight;
            return (
              <line
                key={i}
                x1={padding.left}
                y1={y}
                x2={width - padding.right}
                y2={y}
                className="chart-grid-line"
              />
            );
          })}

          {/* Lines and Areas */}
          {(activeTab === 'all' || activeTab === 'climate') && (
            <>
              {/* Humidity Area & Line */}
              <path d={makeAreaPath(humPoints)} fill="url(#gradHum)" />
              <path d={makePath(humPoints)} fill="none" stroke="#00f2fe" strokeWidth="2.2" />
              {humPoints.length > 0 && (
                <circle
                  cx={humPoints[humPoints.length - 1].x}
                  cy={humPoints[humPoints.length - 1].y}
                  r="4"
                  fill="#00f2fe"
                  style={{ filter: 'drop-shadow(0 0 6px #00f2fe)' }}
                />
              )}

              {/* Temperature Area & Line */}
              <path d={makeAreaPath(tempPoints)} fill="url(#gradTemp)" />
              <path d={makePath(tempPoints)} fill="none" stroke="#f59e0b" strokeWidth="2.2" />
              {tempPoints.length > 0 && (
                <circle
                  cx={tempPoints[tempPoints.length - 1].x}
                  cy={tempPoints[tempPoints.length - 1].y}
                  r="4"
                  fill="#f59e0b"
                  style={{ filter: 'drop-shadow(0 0 6px #f59e0b)' }}
                />
              )}
            </>
          )}

          {(activeTab === 'all' || activeTab === 'air') && (
            <>
              {/* eCO2 Area & Line */}
              <path d={makeAreaPath(eco2Points)} fill="url(#gradEco2)" />
              <path d={makePath(eco2Points)} fill="none" stroke="#10b981" strokeWidth="2" strokeDasharray={activeTab === 'all' ? '5 3' : 'none'} />

              {/* TVOC Area & Line */}
              <path d={makeAreaPath(tvocPoints)} fill="url(#gradTvoc)" />
              <path d={makePath(tvocPoints)} fill="none" stroke="#a855f7" strokeWidth="2" />
              {tvocPoints.length > 0 && (
                <circle
                  cx={tvocPoints[tvocPoints.length - 1].x}
                  cy={tvocPoints[tvocPoints.length - 1].y}
                  r="4"
                  fill="#a855f7"
                  style={{ filter: 'drop-shadow(0 0 6px #a855f7)' }}
                />
              )}
            </>
          )}

          {/* Interactive Mouse Hover Overlay Columns */}
          {data.map((_, index) => {
            const x = padding.left + (index / Math.max(1, data.length - 1)) * plotWidth;
            const colWidth = plotWidth / Math.max(1, data.length);
            return (
              <rect
                key={index}
                x={x - colWidth / 2}
                y={padding.top}
                width={colWidth}
                height={plotHeight}
                fill="transparent"
                style={{ cursor: 'crosshair' }}
                onMouseEnter={() => setHoveredIndex(index)}
              />
            );
          })}

          {/* Hover indicator vertical bar */}
          {hoveredIndex !== null && (
            <line
              x1={padding.left + (hoveredIndex / Math.max(1, data.length - 1)) * plotWidth}
              y1={padding.top}
              x2={padding.left + (hoveredIndex / Math.max(1, data.length - 1)) * plotWidth}
              y2={padding.top + plotHeight}
              stroke="rgba(255, 255, 255, 0.4)"
              strokeDasharray="3 3"
            />
          )}
        </svg>

        {/* Live Hover Legend Tooltip */}
        {hoveredPoint && (
          <div
            style={{
              position: 'absolute',
              top: '12px',
              right: '20px',
              background: 'rgba(10, 15, 26, 0.9)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              borderRadius: '8px',
              padding: '6px 14px',
              fontSize: '0.75rem',
              fontFamily: 'var(--font-mono)',
              display: 'flex',
              gap: '12px',
              boxShadow: '0 8px 20px rgba(0,0,0,0.5)',
              pointerEvents: 'none'
            }}
          >
            <span style={{ color: '#f59e0b' }}>Temp: {hoveredPoint.temperature}°C</span>
            <span style={{ color: '#00f2fe' }}>Hum: {hoveredPoint.humidity}%</span>
            <span style={{ color: '#10b981' }}>eCO2: {hoveredPoint.eco2}ppm</span>
            <span style={{ color: '#a855f7' }}>TVOC: {hoveredPoint.tvoc}ppb</span>
          </div>
        )}
      </div>

      {/* Chart Legend Footer */}
      <div
        style={{
          display: 'flex',
          gap: '20px',
          fontSize: '0.76rem',
          color: 'var(--text-secondary)',
          borderTop: '1px solid var(--border-subtle)',
          paddingTop: '12px',
          flexWrap: 'wrap'
        }}
      >
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#f59e0b', boxShadow: '0 0 6px #f59e0b' }} />
          Temperature (°C)
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#00f2fe', boxShadow: '0 0 6px #00f2fe' }} />
          Humidity (% RH)
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 6px #10b981' }} />
          eCO2 (ppm)
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#a855f7', boxShadow: '0 0 6px #a855f7' }} />
          TVOC (ppb)
        </span>
      </div>
    </div>
  );
}
