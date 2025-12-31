<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-emerald-50 to-teal-50 py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div>
                    <h1
                        class="text-3xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                        Recursos Humanos
                    </h1>
                    <p class="mt-2 text-slate-600">Gestión integral del personal DRE Huánuco</p>
                </div>
                <div class="flex gap-2">
                    <button @click="showEmployeeModal = true"
                        class="inline-flex items-center px-5 py-2.5 text-sm font-bold rounded-xl shadow-lg text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 transition-all">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                        </svg>
                        Nuevo Empleado
                    </button>
                </div>
            </div>

            <!-- Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Total Personal</p>
                            <p class="text-3xl font-bold text-slate-900">{{ summary.total_empleados || 0 }}</p>
                        </div>
                        <div class="bg-emerald-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Activos</p>
                            <p class="text-3xl font-bold text-green-600">{{ summary.empleados_activos || 0 }}</p>
                        </div>
                        <div class="bg-green-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">En Vacaciones</p>
                            <p class="text-3xl font-bold text-orange-600">{{ summary.en_vacaciones || 0 }}</p>
                        </div>
                        <div class="bg-orange-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Actividades del Mes</p>
                            <p class="text-3xl font-bold text-blue-600">{{ summary.actividades_mes || 0 }}</p>
                        </div>
                        <div class="bg-blue-100 p-3 rounded-xl">
                            <svg class="w-8 h-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabs -->
            <div class="border-b border-gray-200 mb-6">
                <nav class="-mb-px flex space-x-8">
                    <button @click="activeTab = 'personal'"
                        :class="[activeTab === 'personal' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        Directorio de Personal
                    </button>
                    <button @click="activeTab = 'vacaciones'"
                        :class="[activeTab === 'vacaciones' ? 'border-orange-500 text-orange-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Vacaciones
                    </button>
                    <button @click="activeTab = 'actividades'"
                        :class="[activeTab === 'actividades' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                        </svg>
                        Gestiones / Actividades
                    </button>
                </nav>
            </div>

            <!-- Personal Tab -->
            <div v-if="activeTab === 'personal'"
                class="bg-white shadow-xl rounded-2xl border border-slate-200 overflow-hidden">
                <!-- Search -->
                <div class="p-4 border-b border-slate-200 bg-slate-50">
                    <input v-model="searchQuery" type="text" placeholder="Buscar por nombre, DNI o área..."
                        class="w-full md:w-96 px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-200">
                        <thead class="bg-slate-50">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Empleado</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">DNI</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Cargo</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Área</th>
                                <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Contrato</th>
                                <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Estado</th>
                                <th class="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-if="isLoading">
                                <td colspan="7" class="px-6 py-24 text-center">
                                    <div class="flex flex-col items-center justify-center">
                                        <svg class="animate-spin h-12 w-12 text-emerald-600 mb-4" fill="none"
                                            viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor"
                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                            </path>
                                        </svg>
                                        <p class="text-lg font-medium text-slate-600">Cargando personal...</p>
                                    </div>
                                </td>
                            </tr>
                            <tr v-else v-for="emp in filteredEmployees" :key="emp.id"
                                class="hover:bg-emerald-50 transition-colors">
                                <td class="px-6 py-4">
                                    <div class="flex items-center">
                                        <div
                                            class="h-10 w-10 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white font-bold text-sm mr-3">
                                            {{ getInitials(emp.nombres + ' ' + emp.apellidos) }}
                                        </div>
                                        <div>
                                            <p class="font-semibold text-slate-900">{{ emp.nombres }} {{ emp.apellidos
                                            }}</p>
                                            <p class="text-xs text-slate-500">{{ emp.correo || '-' }}</p>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4 font-mono text-slate-700">{{ emp.dni }}</td>
                                <td class="px-6 py-4 text-sm text-slate-700">{{ emp.cargo || '-' }}</td>
                                <td class="px-6 py-4 text-sm text-slate-700">{{ emp.area || '-' }}</td>
                                <td class="px-6 py-4">
                                    <span class="px-2 py-1 text-xs font-bold rounded-lg" :class="{
                                        'bg-blue-100 text-blue-700': emp.tipo_contrato === 'Nombrado',
                                        'bg-yellow-100 text-yellow-700': emp.tipo_contrato === 'CAS',
                                        'bg-gray-100 text-gray-700': !emp.tipo_contrato
                                    }">{{ emp.tipo_contrato || '-' }}</span>
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <span class="px-3 py-1 text-xs font-bold rounded-lg" :class="{
                                        'bg-green-100 text-green-700': emp.estado === 'ACTIVO',
                                        'bg-red-100 text-red-700': emp.estado !== 'ACTIVO'
                                    }">{{ emp.estado }}</span>
                                </td>
                                <td class="px-6 py-4 text-right">
                                    <button @click="viewEmployee(emp)" title="Ver detalle del empleado"
                                        class="text-emerald-600 hover:text-emerald-800 p-2 rounded-lg hover:bg-emerald-50 transition-colors"
                                        aria-label="Ver detalle">
                                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="!isLoading && filteredEmployees.length === 0">
                                <td colspan="7" class="px-6 py-12 text-center text-slate-500">No hay empleados
                                    registrados.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Vacaciones Tab -->
            <div v-if="activeTab === 'vacaciones'" class="space-y-6">
                <div class="flex justify-end">
                    <button @click="showVacationModal = true"
                        class="inline-flex items-center px-4 py-2 bg-orange-600 text-white font-bold rounded-xl hover:bg-orange-700 transition-colors">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                        Registrar Vacaciones
                    </button>
                </div>
                <div class="bg-white shadow-xl rounded-2xl border border-slate-200 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-slate-200">
                            <thead class="bg-slate-50">
                                <tr>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Empleado
                                    </th>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Período
                                    </th>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Fecha
                                        Inicio</th>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Fecha Fin
                                    </th>
                                    <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Días
                                    </th>
                                    <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Estado
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr v-for="vac in vacations" :key="vac.id" class="hover:bg-orange-50">
                                    <td class="px-6 py-4 font-semibold text-slate-900">DNI: {{ vac.dni }}</td>
                                    <td class="px-6 py-4 text-slate-700">{{ vac.periodo }}</td>
                                    <td class="px-6 py-4 text-slate-700">{{ vac.fecha_inicio }}</td>
                                    <td class="px-6 py-4 text-slate-700">{{ vac.fecha_fin }}</td>
                                    <td class="px-6 py-4 text-center font-bold text-orange-600">{{ vac.dias_tomados }}
                                    </td>
                                    <td class="px-6 py-4 text-center">
                                        <span class="px-3 py-1 text-xs font-bold rounded-lg" :class="{
                                            'bg-yellow-100 text-yellow-700': vac.estado === 'PROGRAMADO',
                                            'bg-green-100 text-green-700': vac.estado === 'COMPLETADO',
                                            'bg-blue-100 text-blue-700': vac.estado === 'EN CURSO'
                                        }">{{ vac.estado }}</span>
                                    </td>
                                </tr>
                                <tr v-if="vacations.length === 0">
                                    <td colspan="6" class="px-6 py-12 text-center text-slate-500">No hay vacaciones
                                        registradas.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Actividades Tab -->
            <div v-if="activeTab === 'actividades'" class="space-y-6">
                <div class="flex justify-end">
                    <button @click="showActivityModal = true"
                        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                        Nueva Actividad
                    </button>
                </div>
                <div class="bg-white shadow-xl rounded-2xl border border-slate-200 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-slate-200">
                            <thead class="bg-slate-50">
                                <tr>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Fecha
                                    </th>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Empleado
                                    </th>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">Tipo</th>
                                    <th class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase">
                                        Descripción</th>
                                    <th class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase">Estado
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr v-for="act in activities" :key="act.id" class="hover:bg-blue-50">
                                    <td class="px-6 py-4 text-slate-700">{{ act.fecha }}</td>
                                    <td class="px-6 py-4 font-semibold text-slate-900">DNI: {{ act.dni }}</td>
                                    <td class="px-6 py-4">
                                        <span
                                            class="px-2 py-1 text-xs font-bold rounded-lg bg-blue-100 text-blue-700">{{
                                                act.tipo_actividad }}</span>
                                    </td>
                                    <td class="px-6 py-4 text-sm text-slate-600 max-w-xs truncate">{{ act.descripcion }}
                                    </td>
                                    <td class="px-6 py-4 text-center">
                                        <span
                                            class="px-3 py-1 text-xs font-bold rounded-lg bg-green-100 text-green-700">{{
                                                act.estado }}</span>
                                    </td>
                                </tr>
                                <tr v-if="activities.length === 0">
                                    <td colspan="5" class="px-6 py-12 text-center text-slate-500">No hay actividades
                                        registradas.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Employee Modal -->
        <div v-if="showEmployeeModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="flex items-center justify-center min-h-screen px-4">
                <div class="fixed inset-0 bg-black/50" @click="showEmployeeModal = false"></div>
                <div
                    class="relative bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-6 z-10 max-h-[90vh] overflow-y-auto">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-bold text-slate-900">Registrar Nuevo Empleado</h3>
                        <button @click="showEmployeeModal = false" class="text-slate-400 hover:text-slate-600">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <form @submit.prevent="saveEmployee" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">DNI *</label>
                                <input v-model="employeeForm.dni" type="text" maxlength="8" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Tipo Contrato</label>
                                <select v-model="employeeForm.tipo_contrato"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500">
                                    <option value="Nombrado">Nombrado</option>
                                    <option value="CAS">CAS</option>
                                    <option value="Locador">Locador</option>
                                    <option value="Practicante">Practicante</option>
                                </select>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Nombres *</label>
                                <input v-model="employeeForm.nombres" type="text" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Apellidos *</label>
                                <input v-model="employeeForm.apellidos" type="text" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Fecha Nacimiento</label>
                                <input v-model="employeeForm.fecha_nacimiento" type="date"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Género</label>
                                <select v-model="employeeForm.genero"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500">
                                    <option value="">Seleccionar...</option>
                                    <option value="Masculino">Masculino</option>
                                    <option value="Femenino">Femenino</option>
                                </select>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Cargo</label>
                                <input v-model="employeeForm.cargo" type="text"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Área</label>
                                <input v-model="employeeForm.area" type="text"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Teléfono</label>
                                <input v-model="employeeForm.telefono" type="text"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Correo</label>
                                <input v-model="employeeForm.correo" type="email"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Dirección</label>
                            <input v-model="employeeForm.direccion" type="text"
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Fecha de Ingreso</label>
                            <input v-model="employeeForm.fecha_ingreso" type="date"
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500" />
                        </div>
                        <div class="flex gap-3 pt-4">
                            <button type="button" @click="showEmployeeModal = false"
                                class="flex-1 px-4 py-3 border border-slate-200 text-slate-700 font-bold rounded-xl hover:bg-slate-50">Cancelar</button>
                            <button type="submit" :disabled="isSubmitting"
                                class="flex-1 px-4 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50">
                                {{ isSubmitting ? 'Guardando...' : 'Guardar Empleado' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Vacation Modal -->
        <div v-if="showVacationModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="flex items-center justify-center min-h-screen px-4">
                <div class="fixed inset-0 bg-black/50" @click="showVacationModal = false"></div>
                <div class="relative bg-white rounded-2xl shadow-2xl max-w-lg w-full p-6 z-10">
                    <h3 class="text-xl font-bold text-slate-900 mb-6">Registrar Vacaciones</h3>
                    <form @submit.prevent="saveVacation" class="space-y-4">
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Empleado (DNI) *</label>
                            <select v-model="vacationForm.empleado_id" required
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl">
                                <option value="">Seleccionar...</option>
                                <option v-for="emp in employees" :key="emp.id" :value="emp.id">{{ emp.dni }} - {{
                                    emp.nombres }} {{ emp.apellidos }}</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Fecha Inicio *</label>
                                <input v-model="vacationForm.fecha_inicio" type="date" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl" />
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Fecha Fin *</label>
                                <input v-model="vacationForm.fecha_fin" type="date" required
                                    class="w-full px-4 py-2 border border-slate-200 rounded-xl" />
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Observaciones</label>
                            <textarea v-model="vacationForm.observaciones" rows="2"
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl"></textarea>
                        </div>
                        <div class="flex gap-3 pt-4">
                            <button type="button" @click="showVacationModal = false"
                                class="flex-1 px-4 py-3 border border-slate-200 text-slate-700 font-bold rounded-xl">Cancelar</button>
                            <button type="submit"
                                class="flex-1 px-4 py-3 bg-orange-600 text-white font-bold rounded-xl hover:bg-orange-700">Guardar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Activity Modal -->
        <div v-if="showActivityModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="flex items-center justify-center min-h-screen px-4">
                <div class="fixed inset-0 bg-black/50" @click="showActivityModal = false"></div>
                <div class="relative bg-white rounded-2xl shadow-2xl max-w-lg w-full p-6 z-10">
                    <h3 class="text-xl font-bold text-slate-900 mb-6">Registrar Actividad</h3>
                    <form @submit.prevent="saveActivity" class="space-y-4">
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Empleado *</label>
                            <select v-model="activityForm.empleado_id" required
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl">
                                <option value="">Seleccionar...</option>
                                <option v-for="emp in employees" :key="emp.id" :value="emp.id">{{ emp.dni }} - {{
                                    emp.nombres }} {{ emp.apellidos }}</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Tipo de Actividad *</label>
                            <select v-model="activityForm.tipo_actividad" required
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl">
                                <option value="">Seleccionar...</option>
                                <option value="Capacitación">Capacitación</option>
                                <option value="Amonestación">Amonestación</option>
                                <option value="Reconocimiento">Reconocimiento</option>
                                <option value="Cambio de Área">Cambio de Área</option>
                                <option value="Ascenso">Ascenso</option>
                                <option value="Memorándum">Memorándum</option>
                                <option value="Otros">Otros</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Descripción *</label>
                            <textarea v-model="activityForm.descripcion" rows="3" required
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl"></textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Documento de Referencia</label>
                            <input v-model="activityForm.documento_referencia" type="text"
                                class="w-full px-4 py-2 border border-slate-200 rounded-xl"
                                placeholder="Ej: MEMO-001-2024" />
                        </div>
                        <div class="flex gap-3 pt-4">
                            <button type="button" @click="showActivityModal = false"
                                class="flex-1 px-4 py-3 border border-slate-200 text-slate-700 font-bold rounded-xl">Cancelar</button>
                            <button type="submit"
                                class="flex-1 px-4 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700">Guardar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- View Employee Modal -->
        <div v-if="showViewEmployeeModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="flex items-center justify-center min-h-screen px-4">
                <div class="fixed inset-0 bg-black/50 transition-opacity" @click="closeViewEmployeeModal"></div>
                <div class="relative bg-white rounded-2xl shadow-2xl max-w-lg w-full p-6 z-10">
                    <!-- Header with Avatar -->
                    <div class="flex items-center justify-between mb-6">
                        <div class="flex items-center gap-4">
                            <div
                                class="h-14 w-14 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                                {{ selectedEmployee ? getInitials(selectedEmployee.nombres + ' ' +
                                selectedEmployee.apellidos) : '?' }}
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-slate-900">
                                    {{ selectedEmployee?.nombres }} {{ selectedEmployee?.apellidos }}
                                </h3>
                                <p class="text-sm text-slate-500">{{ selectedEmployee?.cargo || 'Sin cargo asignado' }}
                                </p>
                            </div>
                        </div>
                        <button @click="closeViewEmployeeModal"
                            class="text-slate-400 hover:text-slate-600 transition-colors">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Employee Details -->
                    <div v-if="selectedEmployee" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-slate-50 rounded-xl p-4">
                                <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">DNI</p>
                                <p class="text-lg font-semibold text-slate-900 font-mono">{{ selectedEmployee.dni }}</p>
                            </div>
                            <div class="bg-slate-50 rounded-xl p-4">
                                <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Estado</p>
                                <span class="px-3 py-1 text-sm font-bold rounded-lg" :class="{
                                    'bg-green-100 text-green-700': selectedEmployee.estado === 'ACTIVO',
                                    'bg-red-100 text-red-700': selectedEmployee.estado !== 'ACTIVO'
                                }">{{ selectedEmployee.estado }}</span>
                            </div>
                        </div>

                        <div class="bg-slate-50 rounded-xl p-4">
                            <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Área</p>
                            <p class="text-base font-medium text-slate-900">{{ selectedEmployee.area || '-' }}</p>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-slate-50 rounded-xl p-4">
                                <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Tipo de
                                    Contrato</p>
                                <span class="px-2 py-1 text-xs font-bold rounded-lg" :class="{
                                    'bg-blue-100 text-blue-700': selectedEmployee.tipo_contrato === 'Nombrado',
                                    'bg-yellow-100 text-yellow-700': selectedEmployee.tipo_contrato === 'CAS',
                                    'bg-gray-100 text-gray-700': !selectedEmployee.tipo_contrato
                                }">{{ selectedEmployee.tipo_contrato || '-' }}</span>
                            </div>
                            <div class="bg-slate-50 rounded-xl p-4">
                                <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Fecha Ingreso
                                </p>
                                <p class="text-base font-medium text-slate-900">{{ selectedEmployee.fecha_ingreso || '-'
                                    }}</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-slate-50 rounded-xl p-4">
                                <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Teléfono</p>
                                <p class="text-base font-medium text-slate-900">{{ selectedEmployee.telefono || '-' }}
                                </p>
                            </div>
                            <div class="bg-slate-50 rounded-xl p-4">
                                <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Correo</p>
                                <p class="text-sm font-medium text-slate-900 break-all">{{ selectedEmployee.correo ||
                                    '-' }}</p>
                            </div>
                        </div>

                        <div v-if="selectedEmployee.direccion" class="bg-slate-50 rounded-xl p-4">
                            <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Dirección</p>
                            <p class="text-base font-medium text-slate-900">{{ selectedEmployee.direccion }}</p>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="mt-6 pt-4 border-t border-slate-200">
                        <button @click="closeViewEmployeeModal"
                            class="w-full px-4 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all">
                            Cerrar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api';
import Swal from 'sweetalert2';

const activeTab = ref('personal');
const isLoading = ref(false);
const isSubmitting = ref(false);
const searchQuery = ref('');

const employees = ref([]);
const vacations = ref([]);
const activities = ref([]);
const summary = ref({});

const showEmployeeModal = ref(false);
const showVacationModal = ref(false);
const showActivityModal = ref(false);
const showViewEmployeeModal = ref(false);
const selectedEmployee = ref(null);

const employeeForm = ref({
    dni: '', nombres: '', apellidos: '', fecha_nacimiento: '', genero: '',
    direccion: '', telefono: '', correo: '', cargo: '', area: '',
    fecha_ingreso: '', tipo_contrato: 'Nombrado'
});

const vacationForm = ref({ empleado_id: '', fecha_inicio: '', fecha_fin: '', observaciones: '' });
const activityForm = ref({ empleado_id: '', tipo_actividad: '', descripcion: '', documento_referencia: '' });

const filteredEmployees = computed(() => {
    if (!searchQuery.value) return employees.value;
    const q = searchQuery.value.toLowerCase();
    return employees.value.filter(e =>
        (e.nombres + ' ' + e.apellidos).toLowerCase().includes(q) ||
        String(e.dni).includes(q) ||
        (e.area || '').toLowerCase().includes(q)
    );
});

const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
};

const fetchData = async () => {
    isLoading.value = true;
    try {
        const [empRes, vacRes, actRes, sumRes] = await Promise.all([
            api.get('/hr/employees'),
            api.get('/hr/vacations'),
            api.get('/hr/activities'),
            api.get('/hr/summary')
        ]);
        employees.value = empRes.data;
        vacations.value = vacRes.data;
        activities.value = actRes.data;
        summary.value = sumRes.data;
    } catch (error) {
        console.error('Error fetching HR data:', error);
    } finally {
        isLoading.value = false;
    }
};

const saveEmployee = async () => {
    isSubmitting.value = true;
    try {
        await api.post('/hr/employee', employeeForm.value);
        Swal.fire({ icon: 'success', title: 'Empleado Registrado', toast: true, position: 'top-end', showConfirmButton: false, timer: 3000 });
        showEmployeeModal.value = false;
        employeeForm.value = { dni: '', nombres: '', apellidos: '', fecha_nacimiento: '', genero: '', direccion: '', telefono: '', correo: '', cargo: '', area: '', fecha_ingreso: '', tipo_contrato: 'Nombrado' };
        fetchData();
    } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error', text: error.response?.data?.message || 'No se pudo registrar' });
    } finally {
        isSubmitting.value = false;
    }
};

const saveVacation = async () => {
    try {
        const emp = employees.value.find(e => e.id === vacationForm.value.empleado_id);
        await api.post('/hr/vacation', { ...vacationForm.value, dni: emp?.dni });
        Swal.fire({ icon: 'success', title: 'Vacaciones Registradas', toast: true, position: 'top-end', showConfirmButton: false, timer: 3000 });
        showVacationModal.value = false;
        vacationForm.value = { empleado_id: '', fecha_inicio: '', fecha_fin: '', observaciones: '' };
        fetchData();
    } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error', text: error.response?.data?.message || 'No se pudo registrar' });
    }
};

const saveActivity = async () => {
    try {
        const emp = employees.value.find(e => e.id === activityForm.value.empleado_id);
        await api.post('/hr/activity', { ...activityForm.value, dni: emp?.dni });
        Swal.fire({ icon: 'success', title: 'Actividad Registrada', toast: true, position: 'top-end', showConfirmButton: false, timer: 3000 });
        showActivityModal.value = false;
        activityForm.value = { empleado_id: '', tipo_actividad: '', descripcion: '', documento_referencia: '' };
        fetchData();
    } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error', text: error.response?.data?.message || 'No se pudo registrar' });
    }
};

const viewEmployee = (emp) => {
    selectedEmployee.value = emp;
    showViewEmployeeModal.value = true;
};

const closeViewEmployeeModal = () => {
    showViewEmployeeModal.value = false;
    selectedEmployee.value = null;
};

onMounted(() => {
    fetchData();
});
</script>
