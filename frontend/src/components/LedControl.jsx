import React from 'react';
import { Lightbulb, Zap, Radio, RefreshCw } from 'lucide-react';

export default function LedControl({ ledState, toggleLed, isPending, deviceOnline }) {
  return (
    <div className="glass-panel led-card">
      <div className="card-header-row">
        <div className="card-title">
          <Zap size={18} />
          <span>ESP32 Actuator Control</span>
        </div>
        <div className="status-badge" style={{ padding: '3px 10px', fontSize: '0.72rem' }}>
          <Radio size={12} style={{ color: ledState ? '#00f2fe' : '#94a3b8' }} />
          <span>GPIO 4 (LED)</span>
        </div>
      </div>

      <div className="led-interactive-body">
        {/* Glowing Diode / Lamp with Radial Light Flare */}
        <div className="diode-container">
          <div className={`diode-bulb ${ledState ? 'lit' : ''}`}>
            <Lightbulb size={28} />
          </div>
          <div className="diode-aura" />
        </div>

        {/* Master Interactive Toggle Button */}
        <button
          className={`led-toggle-btn ${ledState ? 'active' : ''}`}
          onClick={() => toggleLed(!ledState)}
          disabled={isPending}
          title={`Click to turn LED ${ledState ? 'OFF' : 'ON'}`}
        >
          <span className="toggle-label">
            {isPending ? 'Syncing...' : ledState ? 'LED Active (ON)' : 'LED Standby (OFF)'}
          </span>
          <div className={`toggle-switch-pill ${ledState ? 'active' : ''}`}>
            <div className="toggle-switch-thumb" />
          </div>
        </button>
      </div>

      <div className="led-footer-status">
        <span>
          MQTT Command Topic: <strong style={{ color: '#e2e8f0' }}>aerosense_iot/actuators/led/set</strong>
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {isPending ? (
            <>
              <RefreshCw size={12} className="spin-icon" style={{ color: '#00f2fe' }} />
              <span style={{ color: '#00f2fe' }}>Transmitting...</span>
            </>
          ) : (
            <span style={{ color: ledState ? '#34d399' : '#94a3b8' }}>
              ● {ledState ? 'HIGH' : 'LOW'}
            </span>
          )}
        </span>
      </div>
    </div>
  );
}
