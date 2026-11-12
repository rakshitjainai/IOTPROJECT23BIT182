import React, { useState } from 'react';
import { HardDrive, Wifi, Clock, Server, Code, ChevronDown, ChevronUp } from 'lucide-react';

export default function DeviceStatus({ telemetry, brokerHost, brokerConnected, lastPacketTime }) {
  const [showRaw, setShowRaw] = useState(false);

  // Format uptime
  const uptimeSec = telemetry.uptime_sec || 0;
  const hours = Math.floor(uptimeSec / 3600);
  const minutes = Math.floor((uptimeSec % 3600) / 60);
  const seconds = uptimeSec % 60;
  const formattedUptime = `${hours}h ${minutes}m ${seconds}s`;

  // Signal Strength
  const rssi = telemetry.wifi_rssi || -60;
  let signalQuality = 'Good';
  let signalColor = '#10b981';
  if (rssi > -50) {
    signalQuality = 'Excellent';
    signalColor = '#10b981';
  } else if (rssi > -70) {
    signalQuality = 'Good';
    signalColor = '#00f2fe';
  } else if (rssi > -85) {
    signalQuality = 'Fair';
    signalColor = '#f59e0b';
  } else {
    signalQuality = 'Weak';
    signalColor = '#f43f5e';
  }

  return (
    <div className="glass-panel diagnostics-panel">
      <div>
        <div className="card-header-row" style={{ marginBottom: '14px' }}>
          <div className="card-title">
            <HardDrive size={18} />
            <span>Node Telemetry & Network</span>
          </div>
          <span className="mode-tag" style={{ background: 'rgba(255,255,255,0.06)', color: 'var(--text-secondary)' }}>
            {telemetry.device_id || 'esp32_station'}
          </span>
        </div>

        <div>
          {/* Wi-Fi RSSI */}
          <div className="diag-item">
            <span className="diag-label">
              <Wifi size={14} style={{ color: signalColor }} />
              Hotspot Signal (RSSI)
            </span>
            <span className="diag-value" style={{ color: signalColor }}>
              {rssi} dBm ({signalQuality})
            </span>
          </div>

          {/* Node IP Address */}
          <div className="diag-item">
            <span className="diag-label">
              <Server size={14} />
              ESP32 Local LAN IP
            </span>
            <span className="diag-value">
              {telemetry.ip || '192.168.43.x'}
            </span>
          </div>

          {/* Uptime */}
          <div className="diag-item">
            <span className="diag-label">
              <Clock size={14} />
              Station Uptime
            </span>
            <span className="diag-value">
              {formattedUptime}
            </span>
          </div>

          {/* Broker Bridge */}
          <div className="diag-item">
            <span className="diag-label">
              <Server size={14} />
              Active MQTT Broker
            </span>
            <span className="diag-value" style={{ color: brokerConnected ? '#34d399' : '#f87171' }}>
              {brokerHost} ({brokerConnected ? 'Active' : 'Connecting'})
            </span>
          </div>
        </div>
      </div>

      {/* Raw JSON Inspector Drawer */}
      <div style={{ marginTop: '10px' }}>
        <button
          onClick={() => setShowRaw(!showRaw)}
          className="btn-secondary"
          style={{ width: '100%', justifyContent: 'space-between', fontSize: '0.75rem', padding: '6px 12px' }}
        >
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Code size={13} />
            <span>{showRaw ? 'Hide Raw JSON Telemetry' : 'Inspect Raw MQTT Payload'}</span>
          </span>
          {showRaw ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>

        {showRaw && (
          <pre className="raw-box" style={{ marginTop: '10px' }}>
            {JSON.stringify(telemetry, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
