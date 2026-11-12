import React from 'react';
import { Cpu, Wifi, WifiOff, Radio, Play, Pause, Activity } from 'lucide-react';

export default function Header({
  deviceOnline,
  brokerConnected,
  brokerHost,
  wsStatus,
  simulationRunning,
  toggleSimulation,
  telemetry
}) {
  return (
    <header className="glass-panel header-bar">
      <div className="brand-section">
        <div className="brand-icon-wrapper">
          <Activity size={24} />
        </div>
        <div className="brand-title-group">
          <h1>
            AeroSense IoT
            <span style={{ fontSize: '0.65rem', padding: '2px 8px', borderRadius: '4px', background: 'rgba(0, 242, 254, 0.15)', color: '#00f2fe', border: '1px solid rgba(0, 242, 254, 0.3)', verticalAlign: 'middle', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              HD Station
            </span>
          </h1>
          <p>ESP32 • AHT21 Climate & ENS160 Air Quality Telemetry</p>
        </div>
      </div>

      <div className="header-badges">
        {/* WebSocket Backend Link */}
        <div className={`status-badge ${wsStatus === 'connected' ? 'online' : 'offline'}`} title="Dashboard to FastAPI WebSocket Link">
          <span className="pulse-dot" />
          <span>WS: {wsStatus === 'connected' ? 'Connected' : 'Reconnecting...'}</span>
        </div>

        {/* ESP32 Hardware Status */}
        <div className={`status-badge ${deviceOnline ? 'online' : 'offline'}`} title="ESP32 Node Status (LWT)">
          {deviceOnline ? <Wifi size={14} /> : <WifiOff size={14} />}
          <span>ESP32: {deviceOnline ? 'Online' : 'Standby / Offline'}</span>
        </div>

        {/* MQTT Broker Status */}
        <div className="status-badge" style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }} title="Configured MQTT Broker">
          <Radio size={13} style={{ color: brokerConnected ? '#00f2fe' : '#94a3b8' }} />
          <span>{brokerHost}</span>
        </div>

        {/* Simulation Mode Toggle Button */}
        <button
          className={`btn-secondary ${simulationRunning ? 'active' : ''}`}
          onClick={toggleSimulation}
          title="Toggle live telemetry simulation loop"
        >
          {simulationRunning ? <Pause size={14} /> : <Play size={14} />}
          <span>{simulationRunning ? 'Sim Active' : 'Test Sim'}</span>
        </button>
      </div>
    </header>
  );
}
