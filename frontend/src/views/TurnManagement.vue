<template>
  <div class="turn-management">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-title">
          <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
            <path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>
          </svg>
          <div>
            <h1>Gestión de Turnos</h1>
            <p>Control y atención de turnos por áreas</p>
          </div>
        </div>
        <div class="header-actions">
          <a href="/externo/turnos" target="_blank" class="action-btn secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
              <polyline points="15 3 21 3 21 9"/>
              <line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
            Abrir Tótem
          </a>
          <a href="/pantalla-turnos" target="_blank" class="action-btn primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
            Ver Pantalla TV
          </a>
        </div>
      </div>
    </header>

    <!-- Stats -->
    <section class="stats-section">
      <div class="stat-card">
        <div class="stat-icon total">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.total || 0 }}</span>
          <span class="stat-label">Total Turnos Hoy</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon waiting">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12,6 12,12 16,14"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.en_espera || 0 }}</span>
          <span class="stat-label">En Espera</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon calling">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.llamando || 0 }}</span>
          <span class="stat-label">Llamando</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon completed">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 11 12 14 22 4"/>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.atendidos || 0 }}</span>
          <span class="stat-label">Atendidos</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon time">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12,6 12,12 8,14"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.tiempo_promedio_espera || 0 }} min</span>
          <span class="stat-label">Tiempo Promedio</span>
        </div>
      </div>
    </section>

    <!-- Main content -->
    <div class="main-content">
      <!-- Panel de control por área -->
      <section class="control-panel">
        <h2 class="section-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z"/>
            <path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/>
          </svg>
          Control por Área
        </h2>
        
        <div class="areas-control-grid">
          <div 
            v-for="area in areas" 
            :key="area.codigo"
            class="area-control-card"
            :class="{ active: selectedArea === area.codigo }"
            @click="selectArea(area.codigo)"
          >
            <div class="area-card-header">
              <span class="area-prefix">{{ area.prefijo }}</span>
              <div class="area-info">
                <span class="area-name">{{ area.nombre }}</span>
                <span class="area-waiting">
                  {{ getWaitingCount(area.codigo) }} en espera
                </span>
              </div>
            </div>
            
            <div class="area-card-actions">
              <button 
                class="call-next-btn"
                :disabled="getWaitingCount(area.codigo) === 0"
                @click.stop="callNextTurn(area.codigo)"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                  <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
                </svg>
                Llamar Siguiente
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Turno actual llamando -->
      <section v-if="currentlyCallingTurn" class="current-turn-section">
        <h2 class="section-title calling">
          <span class="pulse-dot"></span>
          Turno en Atención
        </h2>
        
        <div class="current-turn-display">
          <div class="turn-number-large">{{ currentlyCallingTurn.numero_turno }}</div>
          <div class="turn-details">
            <span class="turn-area">{{ currentlyCallingTurn.nombre_area }}</span>
            <span class="turn-user" v-if="currentlyCallingTurn.nombre_usuario">
              {{ currentlyCallingTurn.nombre_usuario }}
            </span>
            <span class="turn-time">
              Tiempo espera: {{ currentlyCallingTurn.tiempo_espera_minutos || 0 }} min
            </span>
          </div>
          
          <div class="current-turn-actions">
            <button class="complete-btn" @click="completeTurn(currentlyCallingTurn.id)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 11 12 14 22 4"/>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
              </svg>
              Completar Atención
            </button>
            <button class="noshow-btn" @click="cancelTurn(currentlyCallingTurn.id)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
              No se Presentó
            </button>
          </div>
        </div>
      </section>

      <!-- Crear turno manual -->
      <section class="create-turn-section">
        <h2 class="section-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          Generar Turno Manual
        </h2>
        
        <form @submit.prevent="createManualTurn" class="create-turn-form">
          <div class="form-row">
            <div class="form-group">
              <label>Área *</label>
              <select v-model="newTurn.codigo_area" required>
                <option value="">Seleccione área</option>
                <option v-for="area in areas" :key="area.codigo" :value="area.codigo">
                  {{ area.prefijo }} - {{ area.nombre }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label>DNI</label>
              <input v-model="newTurn.dni_usuario" type="text" maxlength="8" placeholder="DNI (opcional)">
            </div>
            
            <div class="form-group">
              <label>Nombre</label>
              <input v-model="newTurn.nombre_usuario" type="text" placeholder="Nombre (opcional)">
            </div>
            
            <button type="submit" class="generate-btn" :disabled="creatingTurn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 11 12 14 22 4"/>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
              </svg>
              Generar
            </button>
          </div>
        </form>
      </section>

      <!-- Lista de turnos del día -->
      <section class="turns-list-section">
        <div class="section-header">
          <h2 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6"/>
              <line x1="8" y1="12" x2="21" y2="12"/>
              <line x1="8" y1="18" x2="21" y2="18"/>
              <line x1="3" y1="6" x2="3.01" y2="6"/>
              <line x1="3" y1="12" x2="3.01" y2="12"/>
              <line x1="3" y1="18" x2="3.01" y2="18"/>
            </svg>
            Turnos del Día
          </h2>
          
          <div class="filter-controls">
            <select v-model="filterArea" class="filter-select">
              <option value="">Todas las áreas</option>
              <option v-for="area in areas" :key="area.codigo" :value="area.codigo">
                {{ area.prefijo }} - {{ area.nombre }}
              </option>
            </select>
            
            <select v-model="filterStatus" class="filter-select">
              <option value="">Todos los estados</option>
              <option value="EN_ESPERA">En Espera</option>
              <option value="LLAMANDO">Llamando</option>
              <option value="ATENDIDO">Atendido</option>
              <option value="CANCELADO">Cancelado</option>
            </select>
          </div>
        </div>
        
        <div class="turns-table-container">
          <table class="turns-table">
            <thead>
              <tr>
                <th>Turno</th>
                <th>Área</th>
                <th>Usuario</th>
                <th>Hora</th>
                <th>Estado</th>
                <th>Llamados</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="turn in filteredTurns" :key="turn.id" :class="'status-' + turn.estado?.toLowerCase()">
                <td class="turn-number-cell">{{ turn.numero_turno }}</td>
                <td>{{ turn.codigo_area }}</td>
                <td>{{ turn.nombre_usuario || 'Sin nombre' }}</td>
                <td>{{ turn.hora_creacion?.substring(0, 5) }}</td>
                <td>
                  <span class="status-badge" :class="'status-' + turn.estado?.toLowerCase()">
                    {{ formatStatus(turn.estado) }}
                  </span>
                </td>
                <td>
                  <!-- Indicador de llamados -->
                  <div class="call-count-indicator" v-if="turn.estado === 'LLAMANDO' || getCallCount(turn.id) > 0">
                    <span 
                      class="call-dot" 
                      :class="{ active: getCallCount(turn.id) >= 1 }"
                      title="1er llamado"
                    >1</span>
                    <span 
                      class="call-dot" 
                      :class="{ active: getCallCount(turn.id) >= 2 }"
                      title="2do llamado"
                    >2</span>
                  </div>
                  <span v-else class="no-calls">-</span>
                </td>
                <td class="actions-cell">
                  <!-- Turno EN ESPERA: Botón de primer llamado -->
                  <button 
                    v-if="turn.estado === 'EN_ESPERA'"
                    class="action-icon-btn call"
                    @click="firstCall(turn)"
                    title="1er Llamado"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                      <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
                    </svg>
                  </button>
                  
                  <!-- Turno LLAMANDO con 1 llamado: Botón de segundo llamado (RE-LLAMAR) -->
                  <button 
                    v-if="turn.estado === 'LLAMANDO' && getCallCount(turn.id) === 1"
                    class="action-btn-mini recall"
                    @click="secondCall(turn)"
                    title="2do Llamado - RE-LLAMAR"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                      <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
                      <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
                    </svg>
                    Re-llamar
                  </button>
                  
                  <!-- Turno LLAMANDO con 2 llamados: Botones de confirmación -->
                  <div v-if="turn.estado === 'LLAMANDO' && getCallCount(turn.id) >= 2" class="confirm-actions">
                    <button 
                      class="action-btn-mini complete"
                      @click="completeTurn(turn.id)"
                      title="Atendido"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="9 11 12 14 22 4"/>
                      </svg>
                      Atendido
                    </button>
                    <button 
                      class="action-btn-mini absent"
                      @click="markAbsent(turn.id)"
                      title="Ausente"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                      </svg>
                      Ausente
                    </button>
                  </div>
                  
                  <!-- Para turnos completados/cancelados no hay acciones -->
                </td>
              </tr>
              <tr v-if="filteredTurns.length === 0">
                <td colspan="7" class="empty-row">No hay turnos para mostrar</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'TurnManagement',
  data() {
    return {
      areas: [],
      turns: [],
      stats: {},
      selectedArea: null,
      currentlyCallingTurn: null,
      filterArea: '',
      filterStatus: '',
      newTurn: {
        codigo_area: '',
        dni_usuario: '',
        nombre_usuario: '',
        created_by: 'VIGILANTE'
      },
      creatingTurn: false,
      refreshInterval: null,
      // Registro de llamados por turno (turnId -> número de llamados)
      callCounts: {}
    };
  },
  computed: {
    filteredTurns() {
      let result = [...this.turns];
      
      if (this.filterArea) {
        result = result.filter(t => t.codigo_area === this.filterArea);
      }
      
      if (this.filterStatus) {
        result = result.filter(t => t.estado === this.filterStatus);
      }
      
      return result;
    }
  },
  mounted() {
    this.fetchAreas();
    this.fetchData();
    
    // Auto-refresh cada 10 segundos
    this.refreshInterval = setInterval(() => {
      this.fetchData();
    }, 10000);
  },
  beforeUnmount() {
    if (this.refreshInterval) clearInterval(this.refreshInterval);
  },
  methods: {
    async fetchAreas() {
      try {
        const response = await api.get('/turn/areas');
        if (response.data.success) {
          this.areas = response.data.areas;
        }
      } catch (error) {
        console.error('Error fetching areas:', error);
      }
    },
    
    async fetchData() {
      try {
        // Fetch turns
        const turnsResponse = await api.get('/turn/by-date');
        if (turnsResponse.data.success) {
          this.turns = turnsResponse.data.turnos || [];
        }
        
        // Fetch current calling turns
        const currentResponse = await api.get('/turn/current');
        if (currentResponse.data.success) {
          const currentTurns = currentResponse.data.turnos || [];
          this.currentlyCallingTurn = currentTurns.length > 0 ? currentTurns[0] : null;
        }
        
        // Fetch stats
        const statsResponse = await api.get('/turn/statistics');
        if (statsResponse.data.success) {
          this.stats = statsResponse.data.estadisticas || {};
        }
      } catch (error) {
        console.error('Error fetching turns data:', error);
      }
    },
    
    getWaitingCount(codigoArea) {
      return this.turns.filter(
        t => t.codigo_area === codigoArea && t.estado === 'EN_ESPERA'
      ).length;
    },
    
    selectArea(codigo) {
      this.selectedArea = this.selectedArea === codigo ? null : codigo;
    },
    
    async callNextTurn(codigoArea) {
      try {
        const response = await api.post('/turn/call-next', {
          codigo_area: codigoArea,
          ventanilla: '1',
          user: 'Vigilante'
        });
        
        if (response.data.success) {
          this.currentlyCallingTurn = response.data.turno;
          this.fetchData();
          
          // Reproducir sonido
          this.playNotification();
        } else {
          alert(response.data.error || 'Error al llamar turno');
        }
      } catch (error) {
        console.error('Error calling next turn:', error);
        alert('Error al conectar con el servidor');
      }
    },
    
    async callSpecificTurn(turn) {
      try {
        // Primero marcamos el turno específico como llamando
        const response = await api.post('/turn/call-next', {
          codigo_area: turn.codigo_area,
          ventanilla: '1',
          user: 'Vigilante'
        });
        
        if (response.data.success) {
          this.fetchData();
          this.playNotification();
        }
      } catch (error) {
        console.error('Error calling turn:', error);
      }
    },
    
    // Obtener número de llamados para un turno
    getCallCount(turnId) {
      return this.callCounts[turnId] || 0;
    },
    
    // Primer llamado (desde EN_ESPERA a LLAMANDO)
    async firstCall(turn) {
      try {
        const response = await api.post('/turn/call-next', {
          codigo_area: turn.codigo_area,
          ventanilla: '1',
          user: 'Vigilante'
        });
        
        if (response.data.success) {
          // Registrar primer llamado
          this.callCounts[response.data.turno.id] = 1;
          this.currentlyCallingTurn = response.data.turno;
          this.fetchData();
          this.playNotification();
        } else {
          alert(response.data.error || 'Error al llamar turno');
        }
      } catch (error) {
        console.error('Error en primer llamado:', error);
        alert('Error al conectar con el servidor');
      }
    },
    
    // Segundo llamado (RE-LLAMAR)
    secondCall(turn) {
      // Incrementar contador de llamados
      this.callCounts[turn.id] = 2;
      
      // Reproducir sonido de llamado
      this.playNotification();
      
      // Opcional: Forzar actualización de la vista
      this.$forceUpdate();
    },
    
    // Marcar como ausente
    async markAbsent(turnId) {
      try {
        const response = await api.post(`/turn/cancel/${turnId}`, {
          user: 'Vigilante'
        });
        
        if (response.data.success) {
          // Limpiar contador de llamados
          delete this.callCounts[turnId];
          
          if (this.currentlyCallingTurn?.id === turnId) {
            this.currentlyCallingTurn = null;
          }
          this.fetchData();
        }
      } catch (error) {
        console.error('Error al marcar ausente:', error);
      }
    },
    
    async completeTurn(turnId) {
      try {
        const response = await api.post(`/turn/complete/${turnId}`, {
          user: 'Vigilante'
        });
        
        if (response.data.success) {
          // Limpiar contador de llamados
          delete this.callCounts[turnId];
          
          if (this.currentlyCallingTurn?.id === turnId) {
            this.currentlyCallingTurn = null;
          }
          this.fetchData();
        }
      } catch (error) {
        console.error('Error completing turn:', error);
      }
    },
    
    async cancelTurn(turnId) {
      if (!confirm('¿Está seguro de cancelar este turno?')) return;
      
      try {
        const response = await api.post(`/turn/cancel/${turnId}`, {
          user: 'Vigilante'
        });
        
        if (response.data.success) {
          if (this.currentlyCallingTurn?.id === turnId) {
            this.currentlyCallingTurn = null;
          }
          this.fetchData();
        }
      } catch (error) {
        console.error('Error canceling turn:', error);
      }
    },
    
    async createManualTurn() {
      if (!this.newTurn.codigo_area) {
        alert('Debe seleccionar un área');
        return;
      }
      
      this.creatingTurn = true;
      
      try {
        const response = await api.post('/turn/create', this.newTurn);
        
        if (response.data.success) {
          alert(`Turno ${response.data.turno.numero_turno} generado exitosamente`);
          this.newTurn = {
            codigo_area: '',
            dni_usuario: '',
            nombre_usuario: '',
            created_by: 'VIGILANTE'
          };
          this.fetchData();
        } else {
          alert(response.data.error || 'Error al generar turno');
        }
      } catch (error) {
        console.error('Error creating turn:', error);
        alert('Error al conectar con el servidor');
      } finally {
        this.creatingTurn = false;
      }
    },
    
    formatStatus(status) {
      const statuses = {
        'EN_ESPERA': 'En Espera',
        'LLAMANDO': 'Llamando',
        'ATENDIDO': 'Atendido',
        'CANCELADO': 'Cancelado'
      };
      return statuses[status] || status;
    },
    
    playNotification() {
      try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Función para crear una nota de campana con armónicos
        const playBellNote = (frequency, startTime, duration, volume = 0.4) => {
          const osc1 = audioContext.createOscillator();
          const gain1 = audioContext.createGain();
          const osc2 = audioContext.createOscillator();
          const gain2 = audioContext.createGain();
          
          osc1.connect(gain1);
          osc2.connect(gain2);
          gain1.connect(audioContext.destination);
          gain2.connect(audioContext.destination);
          
          osc1.frequency.value = frequency;
          osc2.frequency.value = frequency * 2;
          osc1.type = 'sine';
          osc2.type = 'sine';
          
          gain1.gain.setValueAtTime(0, startTime);
          gain1.gain.linearRampToValueAtTime(volume, startTime + 0.01);
          gain1.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
          
          gain2.gain.setValueAtTime(0, startTime);
          gain2.gain.linearRampToValueAtTime(volume * 0.4, startTime + 0.01);
          gain2.gain.exponentialRampToValueAtTime(0.001, startTime + duration * 0.7);
          
          osc1.start(startTime);
          osc2.start(startTime);
          osc1.stop(startTime + duration);
          osc2.stop(startTime + duration);
        };
        
        const now = audioContext.currentTime;
        
        // DING-DONG
        playBellNote(784, now, 0.8, 0.5);
        playBellNote(659, now + 0.35, 1.0, 0.5);
        playBellNote(523, now + 0.75, 0.6, 0.25);
        
      } catch (e) {
        console.log('No audio support:', e);
      }
    }
  }
};
</script>

<style scoped>
.turn-management {
  padding: 1.5rem;
  background: #0f172a;
  min-height: 100vh;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* Header */
.page-header {
  margin-bottom: 1.5rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 48px;
  height: 48px;
  color: #f97316;
  background: rgba(249, 115, 22, 0.1);
  padding: 10px;
  border-radius: 12px;
}

.header-title h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
}

.header-title p {
  color: #94a3b8;
  font-size: 0.95rem;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(249, 115, 22, 0.3);
}

.action-btn.secondary {
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.3);
  color: #fb923c;
}

.action-btn.secondary:hover {
  background: rgba(249, 115, 22, 0.2);
}

/* Stats */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 1rem;
  border: 1px solid rgba(71, 85, 105, 0.3);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.75rem;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-icon.total {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}

.stat-icon.waiting {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.stat-icon.calling {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.stat-icon.completed {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.stat-icon.time {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
}

.stat-label {
  font-size: 0.8rem;
  color: #94a3b8;
}

/* Section titles */
.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 1rem;
}

.section-title svg {
  width: 22px;
  height: 22px;
  color: #f97316;
}

.section-title.calling {
  color: #10b981;
}

.pulse-dot {
  width: 10px;
  height: 10px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.7; }
}

/* Control panel */
.control-panel {
  background: rgba(30, 41, 59, 0.5);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(71, 85, 105, 0.3);
  margin-bottom: 1.5rem;
}

.areas-control-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.area-control-card {
  padding: 1rem;
  background: rgba(51, 65, 85, 0.5);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.area-control-card:hover {
  border-color: rgba(249, 115, 22, 0.5);
  background: rgba(249, 115, 22, 0.05);
}

.area-control-card.active {
  border-color: #f97316;
  background: rgba(249, 115, 22, 0.1);
}

.area-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.area-prefix {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 0.5rem;
  font-weight: 800;
  font-size: 1.1rem;
  color: white;
}

.area-info {
  display: flex;
  flex-direction: column;
}

.area-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #e2e8f0;
}

.area-waiting {
  font-size: 0.8rem;
  color: #fbbf24;
}

.call-next-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 0.75rem;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.call-next-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.call-next-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.call-next-btn svg {
  width: 18px;
  height: 18px;
}

/* Current turn section */
.current-turn-section {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 2px solid rgba(16, 185, 129, 0.3);
  margin-bottom: 1.5rem;
}

.current-turn-display {
  text-align: center;
}

.turn-number-large {
  font-size: 4rem;
  font-weight: 900;
  color: #10b981;
  letter-spacing: 4px;
  text-shadow: 0 0 30px rgba(16, 185, 129, 0.5);
  animation: glowPulse 2s infinite;
}

@keyframes glowPulse {
  0%, 100% { text-shadow: 0 0 20px rgba(16, 185, 129, 0.3); }
  50% { text-shadow: 0 0 40px rgba(16, 185, 129, 0.6); }
}

.turn-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1rem 0;
}

.turn-area {
  font-size: 1.25rem;
  color: #60a5fa;
  font-weight: 600;
}

.turn-user {
  color: #e2e8f0;
}

.turn-time {
  color: #94a3b8;
  font-size: 0.9rem;
}

.current-turn-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.complete-btn, .noshow-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.complete-btn svg, .noshow-btn svg {
  width: 20px;
  height: 20px;
}

.complete-btn {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
}

.complete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(34, 197, 94, 0.3);
}

.noshow-btn {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.noshow-btn:hover {
  background: rgba(239, 68, 68, 0.25);
}

/* Create turn section */
.create-turn-section {
  background: rgba(30, 41, 59, 0.5);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(71, 85, 105, 0.3);
  margin-bottom: 1.5rem;
}

.create-turn-form .form-row {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  flex-wrap: wrap;
}

.create-turn-form .form-group {
  flex: 1;
  min-width: 150px;
}

.create-turn-form label {
  display: block;
  font-size: 0.85rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.create-turn-form input,
.create-turn-form select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  font-size: 0.95rem;
}

.create-turn-form input:focus,
.create-turn-form select:focus {
  outline: none;
  border-color: #f97316;
}

.generate-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 0.5rem;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.3);
}

.generate-btn svg {
  width: 18px;
  height: 18px;
}

/* Turns list section */
.turns-list-section {
  background: rgba(30, 41, 59, 0.5);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(71, 85, 105, 0.3);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-controls {
  display: flex;
  gap: 0.75rem;
}

.filter-select {
  padding: 0.5rem 1rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  font-size: 0.9rem;
}

.turns-table-container {
  overflow-x: auto;
}

.turns-table {
  width: 100%;
  border-collapse: collapse;
}

.turns-table th {
  text-align: left;
  padding: 1rem;
  background: rgba(51, 65, 85, 0.5);
  color: #94a3b8;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.turns-table th:first-child {
  border-radius: 0.5rem 0 0 0.5rem;
}

.turns-table th:last-child {
  border-radius: 0 0.5rem 0.5rem 0;
}

.turns-table td {
  padding: 1rem;
  border-bottom: 1px solid rgba(71, 85, 105, 0.3);
  color: #e2e8f0;
}

.turns-table tr:last-child td {
  border-bottom: none;
}

.turns-table tr.status-llamando {
  background: rgba(16, 185, 129, 0.1);
}

.turn-number-cell {
  font-weight: 700;
  font-size: 1.1rem;
  color: #f97316;
}

.status-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.status-en_espera {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.status-badge.status-llamando {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  animation: pulse 1.5s infinite;
}

.status-badge.status-atendido {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.status-badge.status-cancelado {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.action-icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-icon-btn svg {
  width: 16px;
  height: 16px;
}

.action-icon-btn.call {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.action-icon-btn.call:hover {
  background: rgba(16, 185, 129, 0.3);
}

.action-icon-btn.complete {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.action-icon-btn.complete:hover {
  background: rgba(34, 197, 94, 0.3);
}

.action-icon-btn.cancel {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.action-icon-btn.cancel:hover {
  background: rgba(239, 68, 68, 0.3);
}

/* Indicador de llamados */
.call-count-indicator {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.call-dot {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(100, 116, 139, 0.3);
  color: #64748b;
  border: 2px solid rgba(100, 116, 139, 0.4);
  transition: all 0.3s ease;
}

.call-dot.active {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  border-color: #f97316;
  box-shadow: 0 0 10px rgba(249, 115, 22, 0.4);
  animation: callPulse 1s infinite;
}

@keyframes callPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.no-calls {
  color: #64748b;
}

/* Botones mini para acciones en tabla */
.action-btn-mini {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.action-btn-mini svg {
  width: 14px;
  height: 14px;
}

.action-btn-mini.recall {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  animation: recallPulse 1.5s infinite;
}

.action-btn-mini.recall:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
}

@keyframes recallPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(249, 115, 22, 0.4); }
  50% { box-shadow: 0 0 0 6px rgba(249, 115, 22, 0); }
}

.action-btn-mini.complete {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
}

.action-btn-mini.complete:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
}

.action-btn-mini.absent {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #f87171;
}

.action-btn-mini.absent:hover {
  background: rgba(239, 68, 68, 0.25);
}

/* Contenedor de acciones de confirmación */
.confirm-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.actions-cell {
  min-width: 180px;
}

.empty-row {
  text-align: center;
  color: #64748b;
  padding: 2rem !important;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .areas-control-grid {
    grid-template-columns: 1fr;
  }
  
  .create-turn-form .form-row {
    flex-direction: column;
  }
  
  .current-turn-actions {
    flex-direction: column;
  }
}
</style>
