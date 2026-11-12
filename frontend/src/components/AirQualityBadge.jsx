import React from 'react';
import { Wind, ShieldCheck, AlertTriangle, AlertOctagon } from 'lucide-react';

const AQI_CONFIG = {
  1: {
    label: 'Excellent',
    color: '#10b981',
    glow: 'rgba(16, 185, 129, 0.4)',
    desc: 'Air quality is considered ideal, with minimal or zero chemical pollutants. Safe for all sensitive groups.',
    icon: ShieldCheck
  },
  2: {
    label: 'Good',
    color: '#00f2fe',
    glow: 'rgba(0, 242, 254, 0.4)',
    desc: 'Air quality is acceptable. Very low presence of VOCs and CO2 is well within normal indoor levels.',
    icon: ShieldCheck
  },
  3: {
    label: 'Moderate',
    color: '#f59e0b',
    glow: 'rgba(245, 158, 11, 0.4)',
    desc: 'Mild accumulation of organic compounds or elevated CO2. Consider opening a window for fresh airflow.',
    icon: AlertTriangle
  },
  4: {
    label: 'Poor',
    color: '#f97316',
    glow: 'rgba(249, 115, 22, 0.4)',
    desc: 'Noticeable VOC concentrations or elevated CO2. Increased ventilation recommended to maintain focus.',
    icon: AlertTriangle
  },
  5: {
    label: 'Hazardous',
    color: '#f43f5e',
    glow: 'rgba(244, 63, 94, 0.4)',
    desc: 'High concentration of volatile organic contaminants or severe stuffiness. Ventilate space immediately.',
    icon: AlertOctagon
  }
};

export default function AirQualityBadge({ aqi = 1, aqiStatus = 'Excellent', isSimulated = false, sensorMode = 'simulated_fallback' }) {
  const safeAqi = Math.max(1, Math.min(5, Math.round(aqi) || 1));
  const currentConfig = AQI_CONFIG[safeAqi] || AQI_CONFIG[1];
  const IconComponent = currentConfig.icon;

  // Circular gauge math (radius = 56, circumference = 2 * PI * 56 ≈ 351.86)
  const radius = 56;
  const circumference = 2 * Math.PI * radius;
  // Map AQI (1 to 5) to fraction of circumference (0.2 to 1.0)
  const progress = (safeAqi / 5) * circumference;
  const dashoffset = circumference - progress;

  const isPhysical = sensorMode === 'physical_i2c' && !isSimulated;

  return (
    <div className="glass-panel aqi-card">
      <div className="card-header-row">
        <div className="card-title">
          <Wind size={18} />
          <span>ENS160 Air Quality Index</span>
        </div>
        <div className={`mode-tag ${isPhysical ? 'physical' : 'simulated'}`}>
          {isPhysical ? 'Physical I2C Node' : 'Simulated Sensor Fallback'}
        </div>
      </div>

      <div className="aqi-content-layout">
        {/* Radial SVG Gauge */}
        <div className="aqi-gauge-visual">
          <svg className="aqi-gauge-svg" viewBox="0 0 140 140">
            <circle
              className="aqi-gauge-bg"
              cx="70"
              cy="70"
              r={radius}
            />
            <circle
              className="aqi-gauge-meter"
              cx="70"
              cy="70"
              r={radius}
              stroke={currentConfig.color}
              strokeDasharray={circumference}
              strokeDashoffset={dashoffset}
              style={{ filter: `drop-shadow(0 0 8px ${currentConfig.glow})` }}
            />
          </svg>
          <div className="aqi-center-text">
            <span className="aqi-number" style={{ color: currentConfig.color }}>
              {safeAqi}
            </span>
            <span className="aqi-max-label">AQI / 5</span>
          </div>
        </div>

        {/* Text Metadata */}
        <div className="aqi-meta">
          <div className="aqi-status-text" style={{ color: currentConfig.color }}>
            <IconComponent size={26} />
            <span>{aqiStatus || currentConfig.label}</span>
          </div>
          <p className="aqi-description">{currentConfig.desc}</p>

          {/* 5-Step Bar Meter */}
          <div className="aqi-scale-meter">
            {[1, 2, 3, 4, 5].map((step) => {
              const active = step <= safeAqi;
              const stepColor = AQI_CONFIG[step].color;
              return (
                <div
                  key={step}
                  className={`aqi-scale-step ${active ? 'active' : ''}`}
                  style={{
                    backgroundColor: active ? stepColor : 'rgba(255, 255, 255, 0.08)',
                    color: stepColor
                  }}
                  title={`Level ${step}: ${AQI_CONFIG[step].label}`}
                />
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
