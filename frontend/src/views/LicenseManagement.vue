<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-indigo-50 py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div>
                    <h1
                        class="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                        Control de Licencias
                    </h1>
                    <p class="mt-2 text-slate-600">Gestión y seguimiento de licencias del personal</p>
                </div>
                <div>
                    <button @click="showRegisterModal = true"
                        class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-bold rounded-xl shadow-lg text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-purple-300 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                        Registrar Licencia
                    </button>
                </div>
            </div>

            <!-- Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Total Empleados</p>
                            <p class="text-3xl font-bold text-slate-900">{{ summary.total_empleados || 0 }}</p>
                        </div>
                        <div class="bg-purple-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Licencias Este Año</p>
                            <p class="text-3xl font-bold text-indigo-600">{{ summary.licencias_este_año || 0 }}</p>
                        </div>
                        <div class="bg-indigo-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Por Enfermedad</p>
                            <p class="text-3xl font-bold text-red-600">{{ summary.por_tipo?.enfermedad || 0 }}</p>
                        </div>
                        <div class="bg-red-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Sin Días Disponibles</p>
                            <p class="text-3xl font-bold text-yellow-600">{{ summary.empleados_sin_dias || 0 }}</p>
                        </div>
                        <div class="bg-yellow-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabs -->
            <div class="border-b border-gray-200 mb-6">
                <nav class="-mb-px flex space-x-8">
                    <button @click="activeTab = 'licenses'"
                        :class="[activeTab === 'licenses'
                            ? 'border-purple-500 text-purple-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Licencias Registradas
                    </button>
                    <button @click="activeTab = 'employees'"
                        :class="[activeTab === 'employees'
                            ? 'border-indigo-500 text-indigo-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        Empleados y Saldos
                    </button>
                </nav>
            </div>

            <!-- Licenses Tab -->
            <div v-if="activeTab === 'licenses'"
                class="bg-white shadow-xl rounded-2xl border border-slate-200 overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-200">
                        <thead class="bg-slate-50">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Empleado</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Tipo</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Período</th>
                                <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Días</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Motivo</th>
                                <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Estado</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-if="isLoading">
                                <td colspan="6" class="px-6 py-24 text-center">
                                    <div class="flex flex-col items-center justify-center">
                                        <svg class="animate-spin h-12 w-12 text-purple-600 mb-4" fill="none"
                                            viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor"
                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                            </path>
                                        </svg>
                                        <p class="text-lg font-medium text-slate-600">Cargando licencias...</p>
                                    </div>
                                </td>
                            </tr>
                            <tr v-else v-for="license in licenses" :key="license.id"
                                class="hover:bg-purple-50 transition-colors">
                                <td class="px-6 py-4">
                                    <div class="flex items-center">
                                        <div
                                            class="h-10 w-10 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm mr-3">
                                            {{ getInitials(license.nombres || license.dni) }}
                                        </div>
                                        <div>
                                            <p class="font-semibold text-slate-900">{{ license.nombres }} {{
                                                license.apellidos }}</p>
                                            <p class="text-sm text-slate-500 font-mono">DNI: {{ license.dni }}</p>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4">
                                    <span class="px-3 py-1 text-xs font-bold rounded-lg"
                                        :class="getLicenseTypeClass(license.tipo_licencia)">
                                        {{ license.tipo_licencia }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 text-sm text-slate-700">
                                    {{ license.fecha_inicio }} al {{ license.fecha_fin }}
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <span class="text-lg font-bold text-slate-900">{{ license.dias_solicitados }}</span>
                                </td>
                                <td class="px-6 py-4 text-sm text-slate-600 max-w-xs truncate">
                                    {{ license.motivo || '-' }}
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <span class="px-3 py-1 text-xs font-bold rounded-lg bg-green-100 text-green-700">
                                        {{ license.estado }}
                                    </span>
                                </td>
                            </tr>
                            <tr v-if="!isLoading && licenses.length === 0">
                                <td colspan="6" class="px-6 py-12 text-center text-slate-500">
                                    No hay licencias registradas.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Employees Tab -->
            <div v-if="activeTab === 'employees'"
                class="bg-white shadow-xl rounded-2xl border border-slate-200 overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-200">
                        <thead class="bg-slate-50">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Empleado</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">DNI</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Cargo / Área
                                </th>
                                <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Días
                                    Totales</th>
                                <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Días Usados
                                </th>
                                <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Días
                                    Disponibles</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-for="emp in employees" :key="emp.id" class="hover:bg-indigo-50 transition-colors">
                                <td class="px-6 py-4">
                                    <div class="flex items-center">
                                        <div
                                            class="h-10 w-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm mr-3">
                                            {{ getInitials(emp.nombres + ' ' + emp.apellidos) }}
                                        </div>
                                        <div>
                                            <p class="font-semibold text-slate-900">{{ emp.nombres }} {{ emp.apellidos
                                            }}</p>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4 font-mono text-slate-700">{{ emp.dni }}</td>
                                <td class="px-6 py-4 text-sm text-slate-600">
                                    {{ emp.cargo || '-' }} / {{ emp.area || '-' }}
                                </td>
                                <td class="px-6 py-4 text-center font-bold text-slate-700">{{ emp.dias_totales }}</td>
                                <td class="px-6 py-4 text-center font-bold text-orange-600">{{ emp.dias_usados }}</td>
                                <td class="px-6 py-4 text-center">
                                    <span class="px-3 py-1 text-sm font-bold rounded-lg" :class="{
                                        'bg-green-100 text-green-700': emp.dias_disponibles > 10,
                                        'bg-yellow-100 text-yellow-700': emp.dias_disponibles > 0 && emp.dias_disponibles <= 10,
                                        'bg-red-100 text-red-700': emp.dias_disponibles <= 0
                                    }">
                                        {{ emp.dias_disponibles }} días
                                    </span>
                                </td>
                            </tr>
                            <tr v-if="employees.length === 0">
                                <td colspan="6" class="px-6 py-12 text-center text-slate-500">
                                    No hay empleados registrados con licencias.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Register Modal -->
        <div v-if="showRegisterModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="flex items-center justify-center min-h-screen px-4">
                <div class="fixed inset-0 bg-black/50 transition-opacity" @click="showRegisterModal = false"></div>

                <div class="relative bg-white rounded-2xl shadow-2xl max-w-lg w-full p-6 z-10">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-bold text-slate-900">Registrar Nueva Licencia</h3>
                        <button @click="showRegisterModal = false" class="text-slate-400 hover:text-slate-600">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <form @submit.prevent="registerLicense" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">DNI *</label>
                                <input v-model="form.dni" type="text" maxlength="8" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                                    placeholder="12345678" @blur="searchEmployee" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Tipo de Licencia *</label>
                                <select v-model="form.tipo_licencia" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500">
                                    <option value="">Seleccionar...</option>
                                    <option value="Enfermedad">Enfermedad</option>
                                    <option value="Maternidad">Maternidad</option>
                                    <option value="Paternidad">Paternidad</option>
                                    <option value="Personal">Personal</option>
                                    <option value="Otros">Otros</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Nombres *</label>
                                <input v-model="form.nombres" type="text" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Apellidos *</label>
                                <input v-model="form.apellidos" type="text" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500" />
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Cargo</label>
                                <input v-model="form.cargo" type="text"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Área</label>
                                <input v-model="form.area" type="text"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500" />
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Fecha Inicio *</label>
                                <input v-model="form.fecha_inicio" type="date" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Fecha Fin *</label>
                                <input v-model="form.fecha_fin" type="date" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500" />
                            </div>
                        </div>

                        <!-- Days calculation -->
                        <div v-if="calculatedDays > 0" class="bg-purple-50 border border-purple-200 rounded-xl p-4">
                            <div class="flex justify-between items-center">
                                <span class="text-sm font-medium text-purple-700">Días solicitados:</span>
                                <span class="text-2xl font-bold text-purple-600">{{ calculatedDays }}</span>
                            </div>
                            <div v-if="employeeInfo" class="mt-2 pt-2 border-t border-purple-200">
                                <p class="text-sm text-purple-600">
                                    Días disponibles: <strong>{{ employeeInfo.dias_disponibles }}</strong>
                                </p>
                                <p v-if="calculatedDays > employeeInfo.dias_disponibles"
                                    class="text-sm text-red-600 font-bold mt-1">
                                    ⚠️ El empleado no tiene suficientes días disponibles
                                </p>
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Motivo / Observaciones</label>
                            <textarea v-model="form.motivo" rows="2"
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                                placeholder="Detalle del motivo de la licencia..."></textarea>
                        </div>

                        <div class="flex gap-3 pt-4">
                            <button type="button" @click="showRegisterModal = false"
                                class="flex-1 px-4 py-3 border border-slate-200 text-slate-700 font-bold rounded-xl hover:bg-slate-50 transition-colors">
                                Cancelar
                            </button>
                            <button type="submit" :disabled="isSubmitting"
                                class="flex-1 px-4 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-xl hover:from-purple-700 hover:to-indigo-700 transition-all disabled:opacity-50">
                                {{ isSubmitting ? 'Registrando...' : 'Registrar Licencia' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api';
import Swal from 'sweetalert2';

const activeTab = ref('licenses');
const isLoading = ref(false);
const showRegisterModal = ref(false);
const isSubmitting = ref(false);

const licenses = ref([]);
const employees = ref([]);
const summary = ref({});
const employeeInfo = ref(null);

const form = ref({
    dni: '',
    nombres: '',
    apellidos: '',
    cargo: '',
    area: '',
    tipo_licencia: '',
    fecha_inicio: '',
    fecha_fin: '',
    motivo: ''
});

const calculatedDays = computed(() => {
    if (form.value.fecha_inicio && form.value.fecha_fin) {
        const start = new Date(form.value.fecha_inicio);
        const end = new Date(form.value.fecha_fin);
        const diff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
        return diff > 0 ? diff : 0;
    }
    return 0;
});

const getInitials = (name) => {
    if (!name) return '?';
    const str = String(name);
    return str.split(' ').map(n => n[0] || '').join('').substring(0, 2).toUpperCase() || '?';
};

const getLicenseTypeClass = (type) => {
    const classes = {
        'Enfermedad': 'bg-red-100 text-red-700',
        'Maternidad': 'bg-pink-100 text-pink-700',
        'Paternidad': 'bg-blue-100 text-blue-700',
        'Personal': 'bg-yellow-100 text-yellow-700',
        'Otros': 'bg-gray-100 text-gray-700'
    };
    return classes[type] || 'bg-gray-100 text-gray-700';
};

const fetchData = async () => {
    isLoading.value = true;
    try {
        const [licensesRes, employeesRes, summaryRes] = await Promise.all([
            api.get('/license/list'),
            api.get('/license/employees'),
            api.get('/license/summary')
        ]);
        licenses.value = licensesRes.data;
        employees.value = employeesRes.data;
        summary.value = summaryRes.data;
    } catch (error) {
        console.error('Error fetching data:', error);
    } finally {
        isLoading.value = false;
    }
};

const searchEmployee = async () => {
    if (form.value.dni && form.value.dni.length === 8) {
        try {
            const res = await api.get(`/license/employee/${form.value.dni}`);
            if (res.data) {
                employeeInfo.value = res.data;
                form.value.nombres = res.data.nombres || form.value.nombres;
                form.value.apellidos = res.data.apellidos || form.value.apellidos;
                form.value.cargo = res.data.cargo || form.value.cargo;
                form.value.area = res.data.area || form.value.area;
            }
        } catch {
            employeeInfo.value = null;
        }
    }
};

const registerLicense = async () => {
    isSubmitting.value = true;
    try {
        await api.post('/license/register', form.value);
        Swal.fire({
            icon: 'success',
            title: 'Licencia Registrada',
            text: `Se registró la licencia por ${calculatedDays.value} días`,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        });
        showRegisterModal.value = false;
        form.value = { dni: '', nombres: '', apellidos: '', cargo: '', area: '', tipo_licencia: '', fecha_inicio: '', fecha_fin: '', motivo: '' };
        employeeInfo.value = null;
        fetchData();
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.response?.data?.message || 'No se pudo registrar la licencia'
        });
    } finally {
        isSubmitting.value = false;
    }
};

onMounted(() => {
    fetchData();
});
</script>
