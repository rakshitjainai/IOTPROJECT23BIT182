import { useState, useEffect, useRef, useCallback } from 'react';

const API_BASE_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws/telemetry';

export function useTelemetry() {
  const [telemetry, setTelemetry] = useState({
    temperature: 25.0,
    humidity: 50.0,
    tvoc: 55,
    eco2: 420,
    aqi: 1,
    aqi_status: 'Excellent',
    sensor_mode: 'simulated_fallback',
    is_simulated: true,
    device_id: 'esp32_station_01',
    wifi_rssi: -58,
    uptime_sec: 0,
    ip: '192.168.43.100'
  });

  const [history, setHistory] = useState([]);
  const [ledState, setLedState] = useState(false);
  const [isPendingLed, setIsPendingLed] = useState(false);
  const [deviceOnline, setDeviceOnline] = useState(false);
  const [brokerConnected, setBrokerConnected] = useState(false);
  const [brokerHost, setBrokerHost] = useState('broker.emqx.io');
  const [simulationRunning, setSimulationRunning] = useState(false);
  const [wsStatus, setWsStatus] = useState('connecting'); // 'connected' | 'connecting' | 'disconnected'
  const [lastPacketTime, setLastPacketTime] = useState(null);

  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connectWebSocket = useCallback(() => {
    try {
      setWsStatus('connecting');
      const ws = new WebSocket(WS_URL);
      socketRef.current = ws;

      ws.onopen = () => {
        setWsStatus('connected');
        console.log('[WebSocket] Connected to FastAPI backend');
      };

      ws.onmessage = (event) => {
        try {
          const packet = JSON.parse(event.data);
          const { type, data } = packet;
          setLastPacketTime(new Date());

          if (type === 'init') {
            if (data.latest) setTelemetry(data.latest);
            if (Array.isArray(data.history)) setHistory(data.history);
            if (data.led_state !== undefined) setLedState(data.led_state);
            if (data.device_online !== undefined) setDeviceOnline(data.device_online);
            if (data.broker_connected !== undefined) setBrokerConnected(data.broker_connected);
            if (data.broker) setBrokerHost(data.broker);
            if (data.simulation_running !== undefined) setSimulationRunning(data.simulation_running);
          } else if (type === 'telemetry') {
            setTelemetry(data);
            setDeviceOnline(true);
            if (data.led_state !== undefined) setLedState(data.led_state);
            setHistory((prev) => {
              const updated = [...prev, data];
              return updated.slice(-40); // Keep last 40 for clean chart view
            });
          } else if (type === 'led_status') {
            if (data.led_state !== undefined) {
              setLedState(data.led_state);
              setIsPendingLed(false);
            }
          } else if (type === 'device_status') {
            setDeviceOnline(data.device_online);
          } else if (type === 'broker_status') {
            setBrokerConnected(data.status === 'connected');
            if (data.broker) setBrokerHost(data.broker);
          } else if (type === 'simulation_status') {
            setSimulationRunning(data.simulation_running);
          }
        } catch (err) {
          console.error('[WebSocket] Failed to parse message:', err);
        }
      };

      ws.onclose = () => {
        setWsStatus('disconnected');
        console.warn('[WebSocket] Closed, retrying in 3s...');
        reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (err) => {
        console.error('[WebSocket] Error:', err);
        ws.close();
      };
    } catch (err) {
      console.error('[WebSocket] Connection attempt failed:', err);
      reconnectTimeoutRef.current = setTimeout(connectWebSocket, 4000);
    }
  }, []);

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (socketRef.current) socketRef.current.close();
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
    };
  }, [connectWebSocket]);

  // Toggle LED command with immediate optimistic UI & REST fallback
  const toggleLed = async (desiredState) => {
    const nextState = desiredState !== undefined ? desiredState : !ledState;
    setIsPendingLed(true);
    setLedState(nextState); // Optimistic UI update

    // Send via WebSocket if open
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({
        action: 'toggle_led',
        state: nextState
      }));
    } else {
      // Fallback to REST API
      try {
        await fetch(`${API_BASE_URL}/api/led`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ state: nextState })
        });
      } catch (err) {
        console.error('Failed to trigger LED via REST:', err);
      }
    }

    setTimeout(() => setIsPendingLed(false), 800);
  };

  // Toggle backend mock generator
  const toggleSimulation = async () => {
    const nextSim = !simulationRunning;
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ action: 'toggle_sim' }));
    } else {
      try {
        await fetch(`${API_BASE_URL}/api/simulation/toggle`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ enable: nextSim })
        });
        setSimulationRunning(nextSim);
      } catch (err) {
        console.error('Failed to toggle simulation:', err);
      }
    }
  };

  return {
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
  };
}
