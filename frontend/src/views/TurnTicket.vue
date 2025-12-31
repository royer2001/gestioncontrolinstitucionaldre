<template>
  <div class="turn-ticket-page">
    <div class="ticket-container">
      <!-- Header -->
      <header class="ticket-header">
        <div class="dre-logo">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 14l9-5-9-5-9 5 9 5z" />
              <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
              <path d="M12 14v7" />
            </svg>
          </div>
          <div class="logo-text">
            <h1>DRE HUÁNUCO</h1>
            <p>Sistema de Turnos</p>
          </div>
        </div>
      </header>

      <!-- Contenido principal -->
      <main class="ticket-main">
        <!-- Vista de formulario para sacar turno -->
        <div v-if="!generatedTurn" class="form-section">
          <h2 class="form-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            Obtener Turno de Atención
          </h2>
          
          <p class="form-description">
            Seleccione el área donde desea ser atendido y complete sus datos para generar su turno.
          </p>

          <form @submit.prevent="generateTurn" class="turn-form">
            <!-- Selección de área -->
            <div class="form-group area-selection">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                  <polyline points="9,22 9,12 15,12 15,22"/>
                </svg>
                Seleccione el Área *
              </label>
              <div class="areas-grid">
                <button
                  v-for="area in areas"
                  :key="area.codigo"
                  type="button"
                  class="area-card"
                  :class="{ selected: form.codigo_area === area.codigo }"
                  @click="selectArea(area)"
                >
                  <span class="area-prefix">{{ area.prefijo }}</span>
                  <span class="area-name">{{ area.nombre }}</span>
                </button>
              </div>
              <span v-if="errors.codigo_area" class="error-message">{{ errors.codigo_area }}</span>
            </div>

            <!-- Datos opcionales -->
            <div class="optional-data">
              <h3 class="optional-title">Datos Opcionales</h3>
              
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="4" width="18" height="16" rx="2"/>
                      <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    DNI
                  </label>
                  <input
                    v-model="form.dni_usuario"
                    type="text"
                    class="form-input"
                    placeholder="Ingrese su DNI"
                    maxlength="8"
                  />
                </div>
                
                <div class="form-group">
                  <label class="form-label">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                    Nombre
                  </label>
                  <input
                    v-model="form.nombre_usuario"
                    type="text"
                    class="form-input"
                    placeholder="Ingrese su nombre"
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="21" y1="10" x2="3" y2="10"/>
                    <line x1="21" y1="6" x2="3" y2="6"/>
                    <line x1="21" y1="14" x2="3" y2="14"/>
                    <line x1="21" y1="18" x2="3" y2="18"/>
                  </svg>
                  Motivo de la visita
                </label>
                <textarea
                  v-model="form.motivo"
                  class="form-textarea"
                  rows="2"
                  placeholder="Describa brevemente el motivo de su visita"
                ></textarea>
              </div>
            </div>

            <!-- Botón de envío -->
            <button type="submit" class="submit-btn" :disabled="loading">
              <svg v-if="loading" class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="8" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9,11 12,14 22,4"/>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
              </svg>
              {{ loading ? 'Generando...' : 'Generar Mi Turno' }}
            </button>
          </form>
        </div>

        <!-- Vista de turno generado -->
        <div v-else class="ticket-section">
          <div class="ticket-success">
            <div class="success-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M9 12l2 2 4-4"/>
              </svg>
            </div>
            <h2>¡Turno Generado Exitosamente!</h2>
          </div>

          <div class="ticket-display">
            <div class="ticket-number">{{ generatedTurn.numero_turno }}</div>
            <div class="ticket-area">{{ generatedTurn.nombre_area }}</div>
            <div class="ticket-datetime">
              <span class="ticket-date">{{ formatDate(generatedTurn.fecha) }}</span>
              <span class="ticket-time">{{ generatedTurn.hora }}</span>
            </div>
            <div class="queue-position">
              <span class="position-label">Su posición en la cola:</span>
              <span class="position-number">{{ generatedTurn.posicion_cola }}</span>
            </div>
          </div>

          <div class="ticket-instructions">
            <h3>Instrucciones:</h3>
            <ol>
              <li>Espere en la sala de espera hasta que su turno sea llamado.</li>
              <li>Esté atento a la pantalla donde se mostrará su número.</li>
              <li>Cuando vea su número, diríjase a la ventanilla indicada.</li>
              <li>Tenga sus documentos listos para ser atendido.</li>
            </ol>
          </div>

          <div class="ticket-actions">
            <button class="print-btn" @click="printTicket">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6,9 6,2 18,2 18,9"/>
                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                <rect x="6" y="14" width="12" height="8"/>
              </svg>
              Imprimir Ticket
            </button>
            <button class="new-btn" @click="resetForm">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M5 12h14"/>
              </svg>
              Nuevo Turno
            </button>
          </div>
        </div>
      </main>

      <!-- Footer -->
      <footer class="ticket-footer">
        <p>© {{ new Date().getFullYear() }} Dirección Regional de Educación Huánuco</p>
        <p class="footer-time">{{ currentTime }}</p>
      </footer>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'TurnTicket',
  data() {
    return {
      areas: [],
      form: {
        codigo_area: '',
        dni_usuario: '',
        nombre_usuario: '',
        motivo: '',
        created_by: 'TOTEM'
      },
      errors: {},
      loading: false,
      generatedTurn: null,
      currentTime: ''
    };
  },
  mounted() {
    this.fetchAreas();
    this.updateTime();
    setInterval(this.updateTime, 1000);
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
    
    selectArea(area) {
      this.form.codigo_area = area.codigo;
      this.errors.codigo_area = '';
    },
    
    validateForm() {
      this.errors = {};
      
      if (!this.form.codigo_area) {
        this.errors.codigo_area = 'Debe seleccionar un área';
        return false;
      }
      
      return true;
    },
    
    async generateTurn() {
      if (!this.validateForm()) return;
      
      this.loading = true;
      
      try {
        const response = await api.post('/turn/create', this.form);
        
        if (response.data.success) {
          this.generatedTurn = response.data.turno;
        } else {
          alert(response.data.error || 'Error al generar el turno');
        }
      } catch (error) {
        console.error('Error generating turn:', error);
        alert('Error al conectar con el servidor');
      } finally {
        this.loading = false;
      }
    },
    
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr + 'T00:00:00');
      return date.toLocaleDateString('es-PE', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    
    printTicket() {
      window.print();
    },
    
    resetForm() {
      this.form = {
        codigo_area: '',
        dni_usuario: '',
        nombre_usuario: '',
        motivo: '',
        created_by: 'TOTEM'
      };
      this.generatedTurn = null;
      this.errors = {};
    },
    
    updateTime() {
      this.currentTime = new Date().toLocaleTimeString('es-PE');
    }
  }
};
</script>

<style scoped>
.turn-ticket-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

.ticket-container {
  width: 100%;
  max-width: 800px;
  background: linear-gradient(180deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
  border-radius: 2rem;
  border: 1px solid rgba(59, 130, 246, 0.3);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 100px rgba(59, 130, 246, 0.1);
  overflow: hidden;
}

/* Header */
.ticket-header {
  padding: 2rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
  display: flex;
  justify-content: center;
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

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text h1 {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.logo-text p {
  font-size: 1rem;
  color: #94a3b8;
  margin: 0;
  letter-spacing: 3px;
  text-transform: uppercase;
}

/* Main */
.ticket-main {
  padding: 2rem;
}

/* Form section */
.form-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 0.75rem;
}

.form-title svg {
  width: 28px;
  height: 28px;
  color: #3b82f6;
}

.form-description {
  text-align: center;
  color: #94a3b8;
  margin-bottom: 2rem;
}

/* Form */
.turn-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #cbd5e1;
}

.form-label svg {
  width: 18px;
  height: 18px;
  color: #64748b;
}

/* Areas grid */
.areas-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.area-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(51, 65, 85, 0.5);
  border: 2px solid rgba(100, 116, 139, 0.3);
  border-radius: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #e2e8f0;
  text-align: left;
}

.area-card:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.5);
  transform: translateY(-2px);
}

.area-card.selected {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
  border-color: #10b981;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
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
  flex-shrink: 0;
}

.area-card.selected .area-prefix {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.area-name {
  font-size: 0.85rem;
  font-weight: 500;
  line-height: 1.3;
}

/* Optional data */
.optional-data {
  background: rgba(30, 41, 59, 0.5);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(71, 85, 105, 0.3);
}

.optional-title {
  font-size: 1rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-input, .form-textarea {
  padding: 0.875rem 1rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 0.75rem;
  color: #e2e8f0;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.form-input::placeholder, .form-textarea::placeholder {
  color: #64748b;
}

.form-textarea {
  resize: none;
}

/* Submit button */
.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.25rem 2rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 1rem;
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-btn svg {
  width: 24px;
  height: 24px;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Error message */
.error-message {
  color: #f87171;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

/* Ticket section (generated) */
.ticket-success {
  text-align: center;
  margin-bottom: 2rem;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: scaleIn 0.5s ease-out;
}

@keyframes scaleIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

.success-icon svg {
  width: 48px;
  height: 48px;
  color: white;
}

.ticket-success h2 {
  font-size: 1.5rem;
  color: #10b981;
}

.ticket-display {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
  border: 2px dashed rgba(16, 185, 129, 0.5);
  border-radius: 1.5rem;
  margin-bottom: 2rem;
}

.ticket-number {
  font-size: 5rem;
  font-weight: 900;
  color: #10b981;
  letter-spacing: 4px;
  line-height: 1;
  text-shadow: 0 0 30px rgba(16, 185, 129, 0.5);
  animation: pulseNumber 2s infinite;
}

@keyframes pulseNumber {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

.ticket-area {
  font-size: 1.25rem;
  color: #60a5fa;
  font-weight: 600;
  margin: 1rem 0;
}

.ticket-datetime {
  display: flex;
  justify-content: center;
  gap: 2rem;
  color: #94a3b8;
  font-size: 0.95rem;
}

.queue-position {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(100, 116, 139, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.position-label {
  color: #94a3b8;
}

.position-number {
  font-size: 2rem;
  font-weight: 800;
  color: #fbbf24;
}

/* Instructions */
.ticket-instructions {
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  margin-bottom: 1.5rem;
}

.ticket-instructions h3 {
  color: #e2e8f0;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.ticket-instructions ol {
  color: #94a3b8;
  padding-left: 1.5rem;
  line-height: 1.8;
  font-size: 0.9rem;
}

/* Actions */
.ticket-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.print-btn, .new-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.print-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.print-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
}

.new-btn {
  background: rgba(100, 116, 139, 0.3);
  border: 1px solid rgba(100, 116, 139, 0.5);
  color: #e2e8f0;
}

.new-btn:hover {
  background: rgba(100, 116, 139, 0.5);
}

.print-btn svg, .new-btn svg {
  width: 20px;
  height: 20px;
}

/* Footer */
.ticket-footer {
  padding: 1.5rem;
  text-align: center;
  color: #64748b;
  font-size: 0.85rem;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.footer-time {
  font-variant-numeric: tabular-nums;
  margin-top: 0.25rem;
}

/* Print styles */
@media print {
  .turn-ticket-page {
    background: white;
    padding: 0;
  }
  
  .ticket-container {
    box-shadow: none;
    border: none;
    max-width: 100%;
  }
  
  .ticket-header { display: none; }
  .ticket-footer { display: none; }
  .ticket-actions { display: none; }
  .ticket-instructions { display: none; }
  
  .ticket-display {
    border: 2px solid #000;
    background: white;
  }
  
  .ticket-number {
    color: #000;
    text-shadow: none;
  }
  
  .ticket-area { color: #333; }
}

/* Responsive */
@media (max-width: 600px) {
  .areas-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .ticket-number {
    font-size: 4rem;
  }
  
  .ticket-actions {
    grid-template-columns: 1fr;
  }
}
</style>
