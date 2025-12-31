<template>
    <div class="container mx-auto px-4 py-8">
        <div class="sm:flex sm:items-center sm:justify-between mb-8">
            <div>
                <h1 class="text-3xl font-bold text-slate-900">Gestión de Citas</h1>
                <p class="mt-2 text-sm text-slate-700">Administra las reservas de citas realizadas por usuarios
                    externos.</p>
            </div>
            <div class="mt-4 sm:mt-0">
                <button @click="fetchCitas"
                    class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Actualizar
                </button>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="bg-white rounded-xl shadow-md border border-gray-200 px-6 py-24 text-center">
            <div class="flex flex-col items-center justify-center">
                <svg class="animate-spin h-12 w-12 text-blue-600 mb-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                </svg>
                <p class="text-lg font-medium text-slate-600">Cargando citas...</p>
            </div>
        </div>

        <!-- Tabs -->
        <div v-else>
            <div class="border-b border-gray-200 mb-6">
                <nav class="-mb-px flex space-x-8">
                    <button @click="activeTab = 'pending'"
                        :class="[activeTab === 'pending'
                            ? 'border-yellow-500 text-yellow-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Pendientes
                        <span v-if="pendingCitas.length > 0"
                            class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-yellow-500 rounded-full">
                            {{ pendingCitas.length }}
                        </span>
                    </button>
                    <button @click="activeTab = 'completed'"
                        :class="[activeTab === 'completed'
                            ? 'border-green-500 text-green-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Finalizadas
                    </button>
                </nav>
            </div>

            <!-- Citas List -->
            <div class="space-y-6">
                <div v-for="cita in displayedCitas" :key="cita.id"
                    class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">

                    <!-- Header -->
                    <div class="bg-gradient-to-r from-slate-50 to-gray-100 px-6 py-4 border-b border-gray-200">
                        <div class="flex flex-wrap items-center justify-between gap-4">
                            <div class="flex items-center gap-4">
                                <div class="bg-blue-100 p-3 rounded-lg">
                                    <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div>
                                    <h3 class="text-lg font-bold text-gray-900">{{ cita.nombres }} {{ cita.apellidos }}
                                    </h3>
                                    <p class="text-sm text-gray-500">DNI: {{ cita.dni }} | {{ cita.oficina }}</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-3">
                                <span :class="{
                                    'bg-yellow-100 text-yellow-800 border-yellow-300': cita.estado === 'PENDIENTE',
                                    'bg-green-100 text-green-800 border-green-300': cita.estado === 'ATENDIDO',
                                    'bg-red-100 text-red-800 border-red-300': cita.estado === 'CANCELADO'
                                }" class="px-4 py-2 rounded-full text-sm font-bold border">
                                    {{ cita.estado }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Content -->
                    <div class="p-6">
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                            <div>
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Fecha</p>
                                <p class="font-semibold text-gray-900">{{ cita.fecha }}</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Hora</p>
                                <p class="font-semibold text-gray-900">{{ cita.hora }}</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Celular</p>
                                <p class="font-semibold text-gray-900">{{ cita.celular }}</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Correo</p>
                                <p class="font-semibold text-gray-900 text-sm truncate">{{ cita.correo }}</p>
                            </div>
                        </div>

                        <div class="mb-6">
                            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Asunto</p>
                            <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">{{ cita.asunto }}</p>
                        </div>

                        <!-- Stepper Horizontal -->
                        <div class="mb-6">
                            <p class="text-xs text-gray-500 uppercase tracking-wider mb-3">Historial de Estado</p>
                            <div class="flex items-center overflow-x-auto pb-2">
                                <template v-for="(paso, index) in (cita.historial || [])" :key="index">
                                    <!-- Step -->
                                    <div class="flex flex-col items-center min-w-[120px]">
                                        <div :class="{
                                            'bg-yellow-500': paso.estado === 'PENDIENTE',
                                            'bg-green-500': paso.estado === 'ATENDIDO',
                                            'bg-red-500': paso.estado === 'CANCELADO',
                                            'bg-blue-500': !['PENDIENTE', 'ATENDIDO', 'CANCELADO'].includes(paso.estado)
                                        }"
                                            class="w-10 h-10 rounded-full flex items-center justify-center text-white shadow-lg">
                                            <svg v-if="paso.estado === 'PENDIENTE'" class="w-5 h-5" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                            <svg v-else-if="paso.estado === 'ATENDIDO'" class="w-5 h-5" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M5 13l4 4L19 7" />
                                            </svg>
                                            <svg v-else-if="paso.estado === 'CANCELADO'" class="w-5 h-5" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M6 18L18 6M6 6l12 12" />
                                            </svg>
                                            <span v-else class="text-xs font-bold">{{ index + 1 }}</span>
                                        </div>
                                        <p class="mt-2 text-xs font-semibold text-gray-700">{{ paso.estado }}</p>
                                        <p class="text-[10px] text-gray-500">{{ formatDate(paso.fecha) }}</p>
                                    </div>
                                    <!-- Connector Line -->
                                    <div v-if="index < (cita.historial || []).length - 1"
                                        class="flex-1 h-1 bg-gray-300 mx-2 min-w-[40px] rounded"></div>
                                </template>
                                <!-- Empty state if no history -->
                                <div v-if="!cita.historial || cita.historial.length === 0"
                                    class="text-gray-400 text-sm">
                                    Sin historial de cambios
                                </div>
                            </div>
                        </div>

                        <!-- Finalization Observation (Reason) -->
                        <div v-if="cita.estado !== 'PENDIENTE' && getLatestObservation(cita)"
                            class="mb-6 p-4 bg-slate-50 rounded-xl border border-slate-200">
                            <div class="flex items-start gap-3">
                                <div :class="cita.estado === 'ATENDIDO' ? 'text-green-500' : 'text-red-500'"
                                    class="mt-0.5">
                                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                                        <span v-if="cita.estado === 'ATENDIDO'">Observación de Atención</span>
                                        <span v-else>Motivo de Cancelación</span>
                                    </p>
                                    <p class="text-sm text-slate-700 leading-relaxed font-medium">
                                        {{ getLatestObservation(cita) }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Actions -->
                        <div v-if="cita.estado === 'PENDIENTE'" class="flex gap-3 pt-4 border-t border-gray-200">
                            <button @click="updateStatus(cita.id, 'ATENDIDO')"
                                class="flex-1 inline-flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium">
                                <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M5 13l4 4L19 7" />
                                </svg>
                                Marcar como Atendido
                            </button>
                            <button @click="updateStatus(cita.id, 'CANCELADO')"
                                class="flex-1 inline-flex items-center justify-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium">
                                <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12" />
                                </svg>
                                Cancelar Cita
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Empty State for current tab -->
                <div v-if="displayedCitas.length === 0"
                    class="text-center py-12 bg-white rounded-xl shadow-sm border border-gray-200">
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <h3 class="mt-2 text-sm font-medium text-gray-900">
                        {{ activeTab === 'pending' ? 'No hay citas pendientes' : 'No hay citas finalizadas' }}
                    </h3>
                    <p class="mt-1 text-sm text-gray-500">
                        <span v-if="activeTab === 'pending'">Las citas pendientes aparecerán aquí.</span>
                        <span v-else>Las citas atendidas o canceladas aparecerán aquí.</span>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api';
import Swal from 'sweetalert2';

const citas = ref([]);
const loading = ref(false);
const activeTab = ref('pending');

// Computed properties for filtering (sorted by fecha descending - most recent first)
const pendingCitas = computed(() =>
    citas.value
        .filter(c => c.estado === 'PENDIENTE')
        .sort((a, b) => new Date(b.fecha + ' ' + b.hora) - new Date(a.fecha + ' ' + a.hora))
);

const completedCitas = computed(() =>
    citas.value
        .filter(c => c.estado !== 'PENDIENTE')
        .sort((a, b) => new Date(b.fecha + ' ' + b.hora) - new Date(a.fecha + ' ' + a.hora))
);

const displayedCitas = computed(() =>
    activeTab.value === 'pending' ? pendingCitas.value : completedCitas.value
);

const formatDate = (dateStr) => {
    if (!dateStr) return '';
    try {
        const date = new Date(dateStr);
        return date.toLocaleDateString('es-PE', {
            day: '2-digit',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch {
        return dateStr;
    }
};
const getLatestObservation = (cita) => {
    if (cita.historial && Array.isArray(cita.historial) && cita.historial.length > 0) {
        // Look for the last entry that has a relevant description
        const entriesWithDesc = [...cita.historial]
            .reverse()
            .filter(h => h.descripcion && h.descripcion.trim() !== 'Cita registrada');

        if (entriesWithDesc.length > 0) {
            return entriesWithDesc[0].descripcion;
        }
    }
    return '';
};

const fetchCitas = async () => {
    loading.value = true;
    try {
        const response = await api.get('/citas/');
        citas.value = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    } catch (error) {
        console.error("Error fetching citas", error);
        if (error.response?.status === 401) {
            Swal.fire({
                icon: 'warning',
                title: 'Sesión expirada',
                text: 'Por favor inicie sesión nuevamente'
            });
        }
    } finally {
        loading.value = false;
    }
};

const updateStatus = async (id, status) => {
    const actionText = status === 'ATENDIDO' ? 'atender' : 'cancelar';
    const confirmButtonColor = status === 'ATENDIDO' ? '#16a34a' : '#dc2626';

    const { value: observacion, isConfirmed } = await Swal.fire({
        title: `¿Confirmar ${status}?`,
        text: `Escriba una breve observación para ${actionText} esta cita:`,
        input: 'textarea',
        inputPlaceholder: 'Ingrese el motivo u observación aquí...',
        inputAttributes: {
            'aria-label': 'Ingrese su observación'
        },
        showCancelButton: true,
        confirmButtonText: 'Confirmar',
        cancelButtonText: 'Volver',
        confirmButtonColor: confirmButtonColor,
        inputValidator: (value) => {
            if (!value && status === 'CANCELADO') {
                return 'Es obligatorio indicar un motivo para la cancelación';
            }
        }
    });

    if (!isConfirmed) return;

    try {
        await api.put(`/citas/${id}/status`, {
            status,
            observacion: observacion || ''
        });
        // Refresh to get updated history
        await fetchCitas();
        Swal.fire({
            icon: 'success',
            title: 'Estado Actualizado',
            text: `La cita ha sido marcada como ${status.toLowerCase()}`,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        });
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo actualizar el estado de la cita'
        });
    }
};

onMounted(() => {
    fetchCitas();
});
</script>
