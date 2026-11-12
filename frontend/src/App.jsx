import React from 'react';
import { useTelemetry } from './hooks/useTelemetry';
import Header from './components/Header';
import AirQualityBadge from './components/AirQualityBadge';
import LedControl from './components/LedControl';
import SensorCards from './components/SensorCard';
import LiveChart from './components/LiveChart';
import DeviceStatus from './components/DeviceStatus';
import { Cpu } from 'lucide-react';

export default function App() {
  const {
    telemetry,
    history,
    ledState,
    isPendingLed,
    deviceOnline,
    brokerConnected,
    brokerHost,
    simulationRunning,
    wsStatus,
    lastPacketTime,
    toggleLed,
    toggleSimulation
  } = useTelemetry();

  return (
    <div className="app-container">
      {/* 1. Header Bar */}
      <Header
        deviceOnline={deviceOnline}
        brokerConnected={brokerConnected}
        brokerHost={brokerHost}
        wsStatus={wsStatus}
        simulationRunning={simulationRunning}
        toggleSimulation={toggleSimulation}
        telemetry={telemetry}
      />

      {/* 2. Hero Section: Air Quality Index Showcase & LED Actuator */}
      <section className="hero-grid">
        <AirQualityBadge
          aqi={telemetry.aqi}
          aqiStatus={telemetry.aqi_status}
          isSimulated={telemetry.is_simulated}
          sensorMode={telemetry.sensor_mode}
        />
        <LedControl
          ledState={ledState}
          toggleLed={toggleLed}
          isPending={isPendingLed}
          deviceOnline={deviceOnline}
        />
      </section>

      {/* 3. Primary Sensor Metric Cards (AHT21 & ENS160) */}
      <section>
        <SensorCards telemetry={telemetry} />
      </section>

      {/* 4. Live Charts & Diagnostics Section */}
      <section className="charts-grid">
        <LiveChart history={history} />
        <DeviceStatus
          telemetry={telemetry}
          brokerHost={brokerHost}
          brokerConnected={brokerConnected}
          lastPacketTime={lastPacketTime}
        />
      </section>

      {/* 5. Minimalist Tech Footer & Pinout Reference */}
      <footer
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '16px 20px',
          borderTop: '1px solid var(--border-subtle)',
          fontSize: '0.78rem',
          color: 'var(--text-muted)',
          flexWrap: 'wrap',
          gap: '12px'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Cpu size={14} style={{ color: '#00f2fe' }} />
          <span>ESP32 Hardware Pinout: SDA=GPIO21 • SCL=GPIO22 • LED=GPIO4</span>
        </div>
        <div>
          <span>MQTT Sub: <code style={{ color: '#94a3b8' }}>aerosense_iot/sensors/data</code> • Mode: Hotspot LAN</span>
        </div>
      </footer>
    </div>
  );
}
