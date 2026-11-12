import React, { useState } from 'react';
import { Thermometer, Droplets, CloudFog, Gauge } from 'lucide-react';

export default function SensorCards({ telemetry }) {
  const [useFahrenheit, setUseFahrenheit] = useState(false);

  const rawTempC = Number(telemetry.temperature) || 0;
  const tempDisplay = useFahrenheit
    ? ((rawTempC * 9) / 5 + 32).toFixed(1)
    : rawTempC.toFixed(1);
  const tempUnit = useFahrenheit ? '°F' : '°C';

  const humidity = Number(telemetry.humidity) || 0;
  const tvoc = Number(telemetry.tvoc) || 0;
  const eco2 = Number(telemetry.eco2) || 400;

  // Temperature status
  const tempStatus =
    rawTempC < 18
      ? { label: 'Cool', color: '#38bdf8', bg: 'rgba(56, 189, 248, 0.15)' }
      : rawTempC <= 27
      ? { label: 'Comfortable', color: '#34d399', bg: 'rgba(52, 211, 153, 0.15)' }
      : { label: 'Warm', color: '#fb923c', bg: 'rgba(251, 146, 60, 0.15)' };

  // Humidity status
  const humStatus =
    humidity < 35
      ? { label: 'Dry', color: '#fbbf24', bg: 'rgba(251, 191, 36, 0.15)' }
      : humidity <= 65
      ? { label: 'Optimal', color: '#34d399', bg: 'rgba(52, 211, 153, 0.15)' }
      : { label: 'Humid', color: '#38bdf8', bg: 'rgba(56, 189, 248, 0.15)' };

  // eCO2 status
  const eco2Status =
    eco2 < 800
      ? { label: 'Normal Indoor', color: '#34d399', bg: 'rgba(52, 211, 153, 0.15)' }
      : eco2 < 1200
      ? { label: 'Acceptable', color: '#fbbf24', bg: 'rgba(251, 191, 36, 0.15)' }
      : { label: 'High / Stuffy', color: '#f87171', bg: 'rgba(248, 113, 113, 0.15)' };

  // TVOC status
  const tvocStatus =
    tvoc < 100
      ? { label: 'Clean Air', color: '#34d399', bg: 'rgba(52, 211, 153, 0.15)' }
      : tvoc < 300
      ? { label: 'Moderate VOC', color: '#fbbf24', bg: 'rgba(251, 191, 36, 0.15)' }
      : { label: 'Elevated VOC', color: '#f87171', bg: 'rgba(248, 113, 113, 0.15)' };

  return (
    <div className="metrics-grid">
      {/* 1. Temperature Card */}
      <div className="glass-panel metric-card">
        <div className="metric-card-top">
          <div className="metric-icon-box temp">
            <Thermometer size={22} />
          </div>
          <button
            onClick={() => setUseFahrenheit(!useFahrenheit)}
            className="metric-source-chip"
            style={{ cursor: 'pointer', border: '1px solid rgba(255,255,255,0.1)' }}
            title="Click to toggle Celsius / Fahrenheit"
          >
            {useFahrenheit ? 'Switch to °C' : 'Switch to °F'}
          </button>
        </div>

        <div>
          <div className="card-title" style={{ fontSize: '0.8rem', marginBottom: '8px' }}>
            Ambient Temperature
          </div>
          <div className="metric-value-container">
            <span className="metric-main-value" style={{ color: '#fed7aa' }}>
              {tempDisplay}
            </span>
            <span className="metric-unit">{tempUnit}</span>
          </div>
        </div>

        <div className="metric-bottom-info">
          <span>Sensor: AHT21 (I2C)</span>
          <span
            className="metric-indicator-pill"
            style={{ color: tempStatus.color, backgroundColor: tempStatus.bg }}
          >
            {tempStatus.label}
          </span>
        </div>
      </div>

      {/* 2. Humidity Card */}
      <div className="glass-panel metric-card">
        <div className="metric-card-top">
          <div className="metric-icon-box hum">
            <Droplets size={22} />
          </div>
          <span className="metric-source-chip">RH%</span>
        </div>

        <div>
          <div className="card-title" style={{ fontSize: '0.8rem', marginBottom: '8px' }}>
            Relative Humidity
          </div>
          <div className="metric-value-container">
            <span className="metric-main-value" style={{ color: '#bae6fd' }}>
              {humidity.toFixed(1)}
            </span>
            <span className="metric-unit">%</span>
          </div>
        </div>

        <div className="metric-bottom-info">
          <span>Target: 40% - 60%</span>
          <span
            className="metric-indicator-pill"
            style={{ color: humStatus.color, backgroundColor: humStatus.bg }}
          >
            {humStatus.label}
          </span>
        </div>
      </div>

      {/* 3. eCO2 Card */}
      <div className="glass-panel metric-card">
        <div className="metric-card-top">
          <div className="metric-icon-box eco2">
            <Gauge size={22} />
          </div>
          <span className="metric-source-chip">ENS160</span>
        </div>

        <div>
          <div className="card-title" style={{ fontSize: '0.8rem', marginBottom: '8px' }}>
            Equivalent CO₂ (eCO₂)
          </div>
          <div className="metric-value-container">
            <span className="metric-main-value" style={{ color: '#a7f3d0' }}>
              {eco2}
            </span>
            <span className="metric-unit">ppm</span>
          </div>
        </div>

        <div className="metric-bottom-info">
          <span>Baseline: ~400 ppm</span>
          <span
            className="metric-indicator-pill"
            style={{ color: eco2Status.color, backgroundColor: eco2Status.bg }}
          >
            {eco2Status.label}
          </span>
        </div>
      </div>

      {/* 4. TVOC Card */}
      <div className="glass-panel metric-card">
        <div className="metric-card-top">
          <div className="metric-icon-box tvoc">
            <CloudFog size={22} />
          </div>
          <span className="metric-source-chip">ENS160</span>
        </div>

        <div>
          <div className="card-title" style={{ fontSize: '0.8rem', marginBottom: '8px' }}>
            Volatile Organics (TVOC)
          </div>
          <div className="metric-value-container">
            <span className="metric-main-value" style={{ color: '#e9d5ff' }}>
              {tvoc}
            </span>
            <span className="metric-unit">ppb</span>
          </div>
        </div>

        <div className="metric-bottom-info">
          <span>Organic Gases</span>
          <span
            className="metric-indicator-pill"
            style={{ color: tvocStatus.color, backgroundColor: tvocStatus.bg }}
          >
            {tvocStatus.label}
          </span>
        </div>
      </div>
    </div>
  );
}
