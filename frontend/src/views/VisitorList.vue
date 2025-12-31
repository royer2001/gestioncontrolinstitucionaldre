<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div>
                    <h1
                        class="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                        Registro de Visitas
                    </h1>
                    <p class="mt-2 text-slate-600">Control de ingreso de personas externas</p>
                </div>
                <div>
                    <button @click="showModal = true"
                        class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-bold rounded-xl shadow-lg text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-purple-300 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                        Nueva Visita
                    </button>
                </div>
            </div>

            <!-- Filters Section -->
            <div class="bg-white shadow-lg rounded-2xl border border-slate-200 p-4 mb-6">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                    <!-- Search -->
                    <div class="lg:col-span-2">
                        <label
                            class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Buscar</label>
                        <div class="relative">
                            <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <input type="text" v-model="filters.search" placeholder="Buscar por nombre o DNI..."
                                class="w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200 text-sm" />
                        </div>
                    </div>

                    <!-- Area Filter -->
                    <div>
                        <label
                            class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Área</label>
                        <select v-model="filters.area"
                            class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200 text-sm bg-white">
                            <option value="">Todas</option>
                            <option v-for="area in areas" :key="area" :value="area">{{ area }}</option>
                        </select>
                    </div>

                    <!-- Status Filter -->
                    <div>
                        <label
                            class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Estado</label>
                        <select v-model="filters.estado"
                            class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200 text-sm bg-white">
                            <option value="">Todos</option>
                            <option value="En curso">En curso</option>
                            <option value="Finalizado">Finalizado</option>
                        </select>
                    </div>

                    <!-- Date Filter -->
                    <div>
                        <label
                            class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Fecha</label>
                        <input type="date" v-model="filters.fecha"
                            class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200 text-sm" />
                    </div>
                </div>

                <!-- Filter Actions -->
                <div class="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
                    <p class="text-sm text-slate-500">
                        <span class="font-semibold text-slate-700">{{ filteredVisitors.length }}</span> resultados
                        encontrados
                    </p>
                    <button @click="clearFilters"
                        class="text-sm font-semibold text-slate-500 hover:text-purple-600 transition-colors duration-200 flex items-center gap-1">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Limpiar filtros
                    </button>
                </div>
            </div>

            <!-- Table Card -->
            <div class="bg-white shadow-xl rounded-2xl border border-slate-200 overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-200">
                        <thead class="bg-slate-50">
                            <tr>
                                <th scope="col"
                                    class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                    Fecha</th>
                                <th scope="col"
                                    class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                    Visitante</th>
                                <th scope="col"
                                    class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                    Área</th>
                                <th scope="col"
                                    class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                    Hora Ingreso</th>
                                <th scope="col"
                                    class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                    Hora Salida</th>
                                <th scope="col"
                                    class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                    Estado</th>
                                <th scope="col"
                                    class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                    Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-slate-100">
                            <tr v-if="loading">
                                <td colspan="7" class="px-6 py-24 text-center">
                                    <div class="flex flex-col items-center justify-center">
                                        <svg class="animate-spin h-12 w-12 text-purple-600 mb-4"
                                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor"
                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                            </path>
                                        </svg>
                                        <p class="text-lg font-medium text-slate-600">Cargando visitas...</p>
                                    </div>
                                </td>
                            </tr>
                            <template v-else>
                                <tr v-for="visitor in paginatedVisitors" :key="visitor.entry_id"
                                    class="hover:bg-purple-50 transition-colors duration-200 ease-in-out">
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm font-semibold text-slate-900">{{ visitor.fecha }}</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div
                                                class="h-10 w-10 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-sm font-bold text-white shadow-md mr-3">
                                                {{ visitor.visitor_name?.charAt(0) || '?' }}
                                            </div>
                                            <div>
                                                <div class="text-sm font-bold text-slate-900">{{ visitor.visitor_name }}
                                                </div>
                                                <div class="text-xs text-slate-500 font-medium">DNI: {{ visitor.dni }}
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="px-3 py-1.5 inline-flex text-xs leading-5 font-bold rounded-lg bg-blue-50 text-blue-700 border border-blue-200">
                                            {{ visitor.area }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                                        {{ visitor.hora_entrada }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                                        {{ visitor.hora_salida || '--:--' }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="px-3 py-1.5 inline-flex text-xs leading-5 font-bold rounded-lg"
                                            :class="visitor.estado === 'Finalizado' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'">
                                            {{ visitor.estado || 'En curso' }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <div class="flex items-center justify-end gap-2">
                                            <button @click="printTicket(visitor)"
                                                class="text-slate-500 hover:text-purple-600 p-2 rounded-lg hover:bg-purple-50 transition-colors duration-200"
                                                title="Imprimir Ticket">
                                                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24"
                                                    stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2-4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                                                </svg>
                                            </button>
                                            <button v-if="visitor.estado !== 'Finalizado'"
                                                @click="checkoutVisitor(visitor)" :disabled="isProcessing"
                                                class="inline-flex items-center text-indigo-600 hover:text-indigo-900 bg-indigo-50 hover:bg-indigo-100 px-3 py-1 rounded-lg transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed">
                                                <svg v-if="isProcessing && currentProcessingId === visitor.entry_id"
                                                    class="animate-spin -ml-1 mr-2 h-4 w-4 text-indigo-600"
                                                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                    <circle class="opacity-25" cx="12" cy="12" r="10"
                                                        stroke="currentColor" stroke-width="4"></circle>
                                                    <path class="opacity-75" fill="currentColor"
                                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                                    </path>
                                                </svg>
                                                {{ isProcessing && currentProcessingId === visitor.entry_id ?
                                                    'Procesando...' : 'Marcar Salida' }}
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                                <tr v-if="paginatedVisitors.length === 0">
                                    <td colspan="7" class="px-6 py-16 text-center">
                                        <div class="flex flex-col items-center">
                                            <div class="bg-slate-100 rounded-full p-4 mb-4">
                                                <svg class="h-12 w-12 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                    stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                                                </svg>
                                            </div>
                                            <h3 class="text-lg font-bold text-slate-900 mb-1">No hay visitas registradas
                                            </h3>
                                            <p v-if="hasActiveFilters" class="text-sm text-slate-500">No se encontraron
                                                resultados con los filtros aplicados.</p>
                                            <p v-else class="text-sm text-slate-500">Registra una nueva visita para
                                                comenzar.</p>
                                        </div>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div v-if="totalPages > 1" class="bg-slate-50 px-6 py-4 border-t border-slate-200">
                    <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
                        <div class="flex items-center gap-2 text-sm text-slate-600">
                            <span>Mostrar</span>
                            <select v-model="perPage" @change="currentPage = 1"
                                class="border border-slate-200 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white">
                                <option :value="10">10</option>
                                <option :value="25">25</option>
                                <option :value="50">50</option>
                                <option :value="100">100</option>
                            </select>
                            <span>por página</span>
                        </div>

                        <div class="flex items-center gap-2">
                            <span class="text-sm text-slate-600">
                                Página {{ currentPage }} de {{ totalPages }}
                            </span>
                        </div>

                        <div class="flex items-center gap-1">
                            <button @click="currentPage = 1" :disabled="currentPage === 1"
                                class="p-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
                                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
                                </svg>
                            </button>
                            <button @click="currentPage--" :disabled="currentPage === 1"
                                class="p-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
                                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 19l-7-7 7-7" />
                                </svg>
                            </button>

                            <!-- Page Numbers -->
                            <template v-for="page in visiblePages" :key="page">
                                <button v-if="page !== '...'" @click="currentPage = page" :class="[
                                    'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors duration-200',
                                    currentPage === page
                                        ? 'bg-purple-600 text-white'
                                        : 'border border-slate-200 text-slate-600 hover:bg-slate-100'
                                ]">
                                    {{ page }}
                                </button>
                                <span v-else class="px-2 text-slate-400">...</span>
                            </template>

                            <button @click="currentPage++" :disabled="currentPage === totalPages"
                                class="p-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
                                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 5l7 7-7 7" />
                                </svg>
                            </button>
                            <button @click="currentPage = totalPages" :disabled="currentPage === totalPages"
                                class="p-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
                                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal de Registro -->
        <VisitorRegistrationModal v-if="showModal" @close="showModal = false" @saved="fetchVisitors" />
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '../api';
import VisitorRegistrationModal from '../components/VisitorRegistrationModal.vue';
import Swal from 'sweetalert2';

const visitors = ref([]);
const areas = ref([]);
const showModal = ref(false);
const loading = ref(false);
const isProcessing = ref(false);
const currentProcessingId = ref(null);

// Pagination
const currentPage = ref(1);
const perPage = ref(10);

// Filters
const filters = ref({
    search: '',
    area: '',
    estado: '',
    fecha: ''
});

// Computed: Filtered visitors
const filteredVisitors = computed(() => {
    let result = [...visitors.value];

    // Filter by search term
    if (filters.value.search) {
        const searchLower = filters.value.search.toLowerCase();
        result = result.filter(visitor =>
            (visitor.visitor_name && visitor.visitor_name.toLowerCase().includes(searchLower)) ||
            (visitor.dni && visitor.dni.toLowerCase().includes(searchLower))
        );
    }

    // Filter by area
    if (filters.value.area) {
        result = result.filter(visitor => visitor.area === filters.value.area);
    }

    // Filter by status
    if (filters.value.estado) {
        result = result.filter(visitor => (visitor.estado || 'En curso') === filters.value.estado);
    }

    // Filter by date
    if (filters.value.fecha) {
        result = result.filter(visitor => visitor.fecha === filters.value.fecha);
    }

    return result;
});

// Computed: Paginated visitors
const paginatedVisitors = computed(() => {
    const itemsPerPage = Number(perPage.value);
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredVisitors.value.slice(start, end);
});

// Computed: Total pages
const totalPages = computed(() => {
    return Math.ceil(filteredVisitors.value.length / Number(perPage.value)) || 1;
});

// Computed: Visible page numbers
const visiblePages = computed(() => {
    const pages = [];
    const total = totalPages.value;
    const current = currentPage.value;

    if (total <= 7) {
        for (let i = 1; i <= total; i++) pages.push(i);
    } else {
        if (current <= 3) {
            pages.push(1, 2, 3, 4, '...', total);
        } else if (current >= total - 2) {
            pages.push(1, '...', total - 3, total - 2, total - 1, total);
        } else {
            pages.push(1, '...', current - 1, current, current + 1, '...', total);
        }
    }
    return pages;
});

// Computed: Check if filters are active
const hasActiveFilters = computed(() => {
    return filters.value.search || filters.value.area || filters.value.estado || filters.value.fecha;
});

// Reset page when filters change
watch(filters, () => {
    currentPage.value = 1;
}, { deep: true });

// Clear all filters
const clearFilters = () => {
    filters.value = {
        search: '',
        area: '',
        estado: '',
        fecha: ''
    };
};

const fetchAreas = async () => {
    try {
        const response = await api.get('/visitor/areas');
        areas.value = response.data;
    } catch (error) {
        console.error('Error fetching areas:', error);
    }
};

const fetchVisitors = async () => {
    loading.value = true;
    try {
        const response = await api.get('/visitor/list');
        visitors.value = response.data;
    } catch (error) {
        console.error('Error fetching visitors:', error);
    } finally {
        loading.value = false;
    }
};

const printTicket = (visitor) => {
    window.open(`${api.defaults.baseURL}/visitor/ticket/${visitor.entry_id}`, '_blank');
};

const checkoutVisitor = async (visitor) => {
    try {
        const result = await Swal.fire({
            title: '¿Confirmar Salida?',
            text: `¿Desea registrar la salida de ${visitor.visitor_name}?`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#7C3AED',
            cancelButtonColor: '#6B7280',
            confirmButtonText: 'Sí, registrar salida'
        });

        if (result.isConfirmed) {
            isProcessing.value = true;
            currentProcessingId.value = visitor.entry_id;

            const user = JSON.parse(localStorage.getItem('user'));
            await api.post('/visitor/checkout', {
                entry_id: visitor.entry_id,
                username: user ? user.usuario : 'unknown'
            });
            await Swal.fire('Salida Registrada', '', 'success');
            fetchVisitors();
        }
    } catch (error) {
        console.error('Error checking out:', error);
        Swal.fire('Error', 'No se pudo registrar la salida', 'error');
    } finally {
        isProcessing.value = false;
        currentProcessingId.value = null;
    }
};

onMounted(() => {
    fetchAreas();
    fetchVisitors();
});
</script>
