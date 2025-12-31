<template>
  <div class="waiting-screen">
    <!-- Header con logo y fecha/hora -->
    <header class="screen-header">
      <div class="header-left">
        <div class="dre-logo">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 14l9-5-9-5-9 5 9 5z" />
            <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
            <path d="M12 14l9-5-9-5-9 5 9 5z" />
            <path d="M12 14v7" />
          </svg>
          <div class="logo-text">
            <span class="logo-title">DRE HUÁNUCO</span>
            <span class="logo-subtitle">Sistema de Turnos</span>
          </div>
        </div>
      </div>
      <div class="header-right">
        <div class="datetime-display">
          <span class="time">{{ currentTime }}</span>
          <span class="date">{{ currentDate }}</span>
        </div>
      </div>
    </header>

    <!-- Área principal de turnos actuales siendo llamados -->
    <main class="main-content">
      <!-- Turnos actuales llamando -->
      <section class="current-turns-section">
        <h2 class="section-title">
          <span class="pulse-dot"></span>
          ATENCIÓN ACTUAL
        </h2>
        
        <div class="current-turns-grid" v-if="currentTurns.length > 0">
          <div 
            v-for="turn in currentTurns" 
            :key="turn.id" 
            class="current-turn-card"
            :class="{ 'new-turn': isNewTurn(turn.id) }"
          >
            <div class="turn-number">{{ turn.numero_turno }}</div>
            <div class="turn-info">
              <span class="turn-area">{{ getAreaShortName(turn.codigo_area) }}</span>
              <span class="turn-window">Ventanilla {{ turn.ventanilla || '1' }}</span>
            </div>
            <div class="turn-arrow">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </div>
          </div>
        </div>
        
        <div v-else class="no-current-turns">
          <svg class="waiting-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12,6 12,12 16,14" />
          </svg>
          <p>Esperando siguiente turno...</p>
        </div>
      </section>

      <!-- Panel lateral con turnos en espera por área -->
      <aside class="waiting-panel">
        <h2 class="section-title">EN ESPERA</h2>
        
        <div class="areas-waiting-list">
          <div 
            v-for="(area, codigo) in waitingByArea" 
            :key="codigo" 
            class="area-waiting-card"
            :class="{ 'has-waiting': area.count > 0 }"
          >
            <div class="area-header">
              <span class="area-prefix">{{ area.prefijo }}</span>
              <span class="area-name">{{ getAreaShortName(codigo) }}</span>
            </div>
            <div class="area-count">
              {{ area.count }}
              <span class="count-label">{{ area.count === 1 ? 'turno' : 'turnos' }}</span>
            </div>
            <div class="area-next" v-if="area.turns && area.turns.length > 0">
              Próximo: <strong>{{ area.turns[0].numero_turno }}</strong>
            </div>
          </div>
        </div>
      </aside>
    </main>

    <!-- Footer con información adicional -->
    <footer class="screen-footer">
      <div class="footer-left">
        <span class="total-waiting">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          {{ totalWaiting }} personas en espera
        </span>
      </div>
      <div class="footer-center">
        <marquee behavior="scroll" direction="left" scrollamount="3">
          🎉 Bienvenidos a la Dirección Regional de Educación Huánuco • Por favor, espere su turno y mantenga el orden • Gracias por su visita 🎉
        </marquee>
      </div>
      <div class="footer-right">
        <span class="last-update">Actualizado: {{ lastUpdate }}</span>
      </div>
    </footer>

    <!-- Audio para notificación (oculto) -->
    <audio ref="notificationSound" preload="auto">
      <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2teleP+CXYCD/7+d/06b/wAA" type="audio/wav">
    </audio>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'WaitingScreen',
  data() {
    return {
      currentTurns: [],
      waitingByArea: {},
      totalWaiting: 0,
      currentTime: '',
      currentDate: '',
      lastUpdate: '',
      previousTurnIds: new Set(),
      newTurnIds: new Set(),
      refreshInterval: null,
      clockInterval: null
    };
  },
  mounted() {
    this.updateClock();
    this.fetchDisplayData();
    
    // Actualizar cada 5 segundos
    this.refreshInterval = setInterval(() => {
      this.fetchDisplayData();
    }, 5000);
    
    // Actualizar reloj cada segundo
    this.clockInterval = setInterval(() => {
      this.updateClock();
    }, 1000);
  },
  beforeUnmount() {
    if (this.refreshInterval) clearInterval(this.refreshInterval);
    if (this.clockInterval) clearInterval(this.clockInterval);
  },
  methods: {
    async fetchDisplayData() {
      try {
        const response = await api.get('/turn/display');
        if (response.data.success) {
          // Detectar nuevos turnos para animación y sonido
          const newCurrentTurns = response.data.current || [];
          const newIds = new Set(newCurrentTurns.map(t => t.id));
          
          // Verificar si hay un nuevo turno llamando
          for (const turn of newCurrentTurns) {
            if (!this.previousTurnIds.has(turn.id)) {
              this.newTurnIds.add(turn.id);
              this.playNotificationSound();
              
              // Remover la clase de animación después de 3 segundos
              setTimeout(() => {
                this.newTurnIds.delete(turn.id);
              }, 3000);
            }
          }
          
          this.previousTurnIds = newIds;
          this.currentTurns = newCurrentTurns;
          this.waitingByArea = response.data.waiting_by_area || {};
          this.totalWaiting = response.data.total_waiting || 0;
          this.lastUpdate = new Date().toLocaleTimeString('es-PE');
        }
      } catch (error) {
        console.error('Error fetching display data:', error);
      }
    },
    
    updateClock() {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString('es-PE', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
      this.currentDate = now.toLocaleDateString('es-PE', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    
    getAreaShortName(codigo) {
      const shortNames = {
        'DGI': 'Gestión Institucional',
        'DGP': 'Gestión Pedagógica',
        'TRAMITE': 'Trámite Documentario',
        'ACTAS': 'Actas y Certificados',
        'TESORERIA': 'Tesorería',
        'ESCALAFON': 'Escalafón',
        'RRHH': 'Recursos Humanos',
        'OCI': 'Control Institucional',
        'DIRECCION': 'Dirección Regional',
        'LEGAL': 'Asesoría Legal'
      };
      return shortNames[codigo] || codigo;
    },
    
    isNewTurn(turnId) {
      return this.newTurnIds.has(turnId);
    },
    
    playNotificationSound() {
      try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Función para crear una nota de campana con armónicos
        const playBellNote = (frequency, startTime, duration, volume = 0.4) => {
          // Oscilador principal
          const osc1 = audioContext.createOscillator();
          const gain1 = audioContext.createGain();
          
          // Armónico 2 (doble de frecuencia, más suave)
          const osc2 = audioContext.createOscillator();
          const gain2 = audioContext.createGain();
          
          // Armónico 3 (triple, muy suave para brillo)
          const osc3 = audioContext.createOscillator();
          const gain3 = audioContext.createGain();
          
          // Conectar osciladores a sus ganancias
          osc1.connect(gain1);
          osc2.connect(gain2);
          osc3.connect(gain3);
          
          // Conectar al destino
          gain1.connect(audioContext.destination);
          gain2.connect(audioContext.destination);
          gain3.connect(audioContext.destination);
          
          // Configurar frecuencias
          osc1.frequency.value = frequency;
          osc2.frequency.value = frequency * 2;
          osc3.frequency.value = frequency * 3;
          
          // Tipo de onda sinusoidal para sonido limpio
          osc1.type = 'sine';
          osc2.type = 'sine';
          osc3.type = 'sine';
          
          // Envolvente de campana: ataque rápido, decaimiento largo
          gain1.gain.setValueAtTime(0, startTime);
          gain1.gain.linearRampToValueAtTime(volume, startTime + 0.01);
          gain1.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
          
          gain2.gain.setValueAtTime(0, startTime);
          gain2.gain.linearRampToValueAtTime(volume * 0.5, startTime + 0.01);
          gain2.gain.exponentialRampToValueAtTime(0.001, startTime + duration * 0.7);
          
          gain3.gain.setValueAtTime(0, startTime);
          gain3.gain.linearRampToValueAtTime(volume * 0.25, startTime + 0.01);
          gain3.gain.exponentialRampToValueAtTime(0.001, startTime + duration * 0.5);
          
          // Iniciar y detener
          osc1.start(startTime);
          osc2.start(startTime);
          osc3.start(startTime);
          
          osc1.stop(startTime + duration);
          osc2.stop(startTime + duration);
          osc3.stop(startTime + duration);
        };
        
        const now = audioContext.currentTime;
        
        // ✨ DING-DONG clásico de servicio
        // Primera nota: DING (nota alta G5 = 784 Hz)
        playBellNote(784, now, 0.8, 0.5);
        
        // Segunda nota: DONG (nota baja E5 = 659 Hz) - después de 0.3s
        playBellNote(659, now + 0.35, 1.0, 0.5);
        
        // Tercera nota opcional: toque final suave (C5 = 523 Hz)
        playBellNote(523, now + 0.75, 0.6, 0.25);
        
      } catch (e) {
        console.log('No se pudo reproducir el sonido:', e);
      }
    }
  }
};
</script>

<style scoped>
.waiting-screen {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  display: flex;
  flex-direction: column;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  color: #ffffff;
  overflow: hidden;
}

/* Header */
.screen-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 3rem;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.8) 100%);
  border-bottom: 2px solid rgba(59, 130, 246, 0.3);
}

.dre-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  width: 60px;
  height: 60px;
  color: #3b82f6;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-subtitle {
  font-size: 1rem;
  color: #94a3b8;
  letter-spacing: 4px;
  text-transform: uppercase;
}

.datetime-display {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.time {
  font-size: 3rem;
  font-weight: 700;
  color: #60a5fa;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.date {
  font-size: 1rem;
  color: #94a3b8;
  text-transform: capitalize;
}

/* Main content */
.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  padding: 2rem 3rem;
  overflow: hidden;
}

/* Current turns section */
.current-turns-section {
  display: flex;
  flex-direction: column;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 1.5rem;
  letter-spacing: 2px;
}

.pulse-dot {
  width: 12px;
  height: 12px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.7; }
}

.current-turns-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
}

.current-turn-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 3rem;
  background: linear-gradient(135deg, 
    rgba(16, 185, 129, 0.2) 0%, 
    rgba(59, 130, 246, 0.2) 100%);
  border: 2px solid rgba(16, 185, 129, 0.5);
  border-radius: 1.5rem;
  animation: slideIn 0.5s ease-out;
}

.current-turn-card.new-turn {
  animation: newTurnPulse 0.5s ease-out, glowPulse 2s infinite;
  border-color: #fbbf24;
  background: linear-gradient(135deg, 
    rgba(251, 191, 36, 0.3) 0%, 
    rgba(16, 185, 129, 0.2) 100%);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes newTurnPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.02); }
  100% { transform: scale(1); }
}

@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(251, 191, 36, 0.3); }
  50% { box-shadow: 0 0 40px rgba(251, 191, 36, 0.6); }
}

.turn-number {
  font-size: 5rem;
  font-weight: 900;
  color: #10b981;
  letter-spacing: 4px;
  text-shadow: 0 0 30px rgba(16, 185, 129, 0.5);
}

.new-turn .turn-number {
  color: #fbbf24;
  text-shadow: 0 0 30px rgba(251, 191, 36, 0.5);
}

.turn-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.turn-area {
  font-size: 1.25rem;
  color: #e2e8f0;
  font-weight: 600;
}

.turn-window {
  font-size: 2rem;
  font-weight: 700;
  color: #60a5fa;
  padding: 0.5rem 1.5rem;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 0.75rem;
  border: 1px solid rgba(59, 130, 246, 0.4);
}

.turn-arrow {
  display: flex;
  align-items: center;
  animation: arrowBounce 1s infinite;
}

.turn-arrow svg {
  width: 60px;
  height: 60px;
  color: #10b981;
}

@keyframes arrowBounce {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(10px); }
}

.no-current-turns {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  color: #64748b;
}

.waiting-icon {
  width: 120px;
  height: 120px;
  opacity: 0.5;
  animation: waitingPulse 2s infinite;
}

@keyframes waitingPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

.no-current-turns p {
  font-size: 1.5rem;
  font-weight: 500;
}

/* Waiting panel */
.waiting-panel {
  background: rgba(30, 41, 59, 0.7);
  border-radius: 1.5rem;
  padding: 1.5rem;
  border: 1px solid rgba(71, 85, 105, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.waiting-panel .section-title {
  text-align: center;
  margin-bottom: 1rem;
}

.areas-waiting-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
  flex: 1;
}

.area-waiting-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 1rem;
  border: 1px solid rgba(100, 116, 139, 0.3);
  transition: all 0.3s ease;
}

.area-waiting-card.has-waiting {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.4);
}

.area-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.area-prefix {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border-radius: 0.5rem;
  font-weight: 800;
  font-size: 1.25rem;
}

.area-name {
  font-size: 0.9rem;
  color: #cbd5e1;
  font-weight: 500;
}

.area-count {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 1rem;
  min-width: 60px;
}

.area-count {
  font-size: 1.75rem;
  font-weight: 700;
  color: #60a5fa;
}

.count-label {
  font-size: 0.7rem;
  color: #94a3b8;
  font-weight: 400;
}

.area-next {
  font-size: 0.85rem;
  color: #94a3b8;
  padding: 0.5rem 0.75rem;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 0.5rem;
  white-space: nowrap;
}

.area-next strong {
  color: #10b981;
}

/* Footer */
.screen-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 3rem;
  background: linear-gradient(0deg, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.8) 100%);
  border-top: 2px solid rgba(59, 130, 246, 0.3);
}

.footer-left, .footer-right {
  flex: 0 0 auto;
}

.footer-center {
  flex: 1;
  margin: 0 2rem;
  overflow: hidden;
}

.total-waiting {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: #94a3b8;
}

.total-waiting svg {
  width: 24px;
  height: 24px;
  color: #60a5fa;
}

.last-update {
  font-size: 0.9rem;
  color: #64748b;
}

/* Responsive */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .waiting-panel {
    max-height: 200px;
  }
  
  .turn-number {
    font-size: 3.5rem;
  }
}
</style>
