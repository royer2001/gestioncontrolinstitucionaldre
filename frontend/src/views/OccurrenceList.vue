<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div>
                    <h1
                        class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                        Libro de Ocurrencias
                    </h1>
                    <p class="mt-2 text-slate-600">Registro histórico de incidentes y novedades</p>
                </div>
                <div v-if="activeTab === 'list'" class="flex gap-3">
                    <!-- Botón Personal Ausente -->
                    <button @click="showAbsentModal = true"
                        class="inline-flex items-center px-5 py-3 border-2 border-purple-500 text-sm font-bold rounded-xl text-purple-600 bg-white hover:bg-purple-50 focus:outline-none focus:ring-4 focus:ring-purple-200 transition-all duration-300 ease-in-out">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                        Personal Ausente
                        <span v-if="activeLicenses.length > 0"
                            class="ml-2 bg-purple-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
                            {{ activeLicenses.length }}
                        </span>
                    </button>
                    <!-- Botón Nueva Ocurrencia -->
                    <button @click="showRegisterModal = true"
                        class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-bold rounded-xl shadow-lg text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                        Nueva Ocurrencia
                    </button>
                </div>
            </div>

            <!-- Tabs Navigation -->
            <div class="border-b border-gray-200 mb-6">
                <nav class="-mb-px flex space-x-8">
                    <button @click="activeTab = 'list'"
                        :class="[activeTab === 'list'
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                        Listado
                    </button>
                    <button @click="activeTab = 'reports'"
                        :class="[activeTab === 'reports'
                            ? 'border-indigo-500 text-indigo-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors']">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Reportes Semanales
                    </button>
                </nav>
            </div>

            <!-- List Tab Content -->
            <div v-if="activeTab === 'list'">

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
                                <input type="text" v-model="filters.search"
                                    placeholder="Buscar por descripción o responsable..."
                                    class="w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 text-sm" />
                            </div>
                        </div>

                        <!-- Type Filter -->
                        <div>
                            <label
                                class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Tipo</label>
                            <select v-model="filters.tipo"
                                class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 text-sm bg-white">
                                <option value="">Todos</option>
                                <option value="Incidente">Incidente</option>
                                <option value="Emergencia">Emergencia</option>
                                <option value="Rutina">Rutina</option>
                                <option value="Aviso">Aviso</option>
                                <option value="Otros">Otros</option>
                            </select>
                        </div>

                        <!-- Date From -->
                        <div>
                            <label
                                class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Desde</label>
                            <input type="date" v-model="filters.fechaDesde"
                                class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 text-sm" />
                        </div>

                        <!-- Date To -->
                        <div>
                            <label
                                class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Hasta</label>
                            <input type="date" v-model="filters.fechaHasta"
                                class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 text-sm" />
                        </div>
                    </div>

                    <!-- Filter Actions -->
                    <div class="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
                        <p class="text-sm text-slate-500">
                            <span class="font-semibold text-slate-700">{{ filteredOccurrences.length }}</span>
                            resultados
                            encontrados
                        </p>
                        <button @click="clearFilters"
                            class="text-sm font-semibold text-slate-500 hover:text-blue-600 transition-colors duration-200 flex items-center gap-1">
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
                                        Tipo</th>
                                    <th scope="col"
                                        class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                        Descripción</th>
                                    <th scope="col"
                                        class="px-6 py-4 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                                        Responsable</th>
                                    <th scope="col"
                                        class="px-6 py-4 text-center text-xs font-bold text-slate-600 uppercase tracking-wider">
                                        Estado</th>
                                    <th scope="col" class="relative px-6 py-4"><span class="sr-only">Acciones</span>
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-slate-100">
                                <tr v-if="isLoading">
                                    <td colspan="6" class="px-6 py-12 text-center">
                                        <div class="flex flex-col items-center justify-center">
                                            <svg class="animate-spin h-10 w-10 text-blue-600 mb-4"
                                                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                    stroke-width="4"></circle>
                                                <path class="opacity-75" fill="currentColor"
                                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                                </path>
                                            </svg>
                                            <p class="text-sm font-semibold text-slate-500">Cargando ocurrencias...</p>
                                        </div>
                                    </td>
                                </tr>
                                <tr v-else v-for="occurrence in paginatedOccurrences" :key="occurrence.id"
                                    class="hover:bg-blue-50 transition-colors duration-200 ease-in-out">
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm font-semibold text-slate-900">{{ occurrence.fecha }}</div>
                                        <div class="text-xs text-slate-500 font-medium">{{ occurrence.hora }}</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="px-3 py-1.5 inline-flex text-xs leading-5 font-bold rounded-lg shadow-sm"
                                            :class="{
                                                'bg-gradient-to-r from-red-500 to-red-600 text-white': occurrence.tipo === 'Emergencia' || occurrence.tipo === 'Robo',
                                                'bg-gradient-to-r from-yellow-500 to-yellow-600 text-white': occurrence.tipo === 'Incidente',
                                                'bg-gradient-to-r from-green-500 to-green-600 text-white': occurrence.tipo === 'Rutina',
                                                'bg-gradient-to-r from-blue-500 to-blue-600 text-white': occurrence.tipo === 'Aviso',
                                                'bg-gradient-to-r from-gray-500 to-gray-600 text-white': occurrence.tipo === 'Otros'
                                            }">
                                            {{ occurrence.tipo }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4">
                                        <div class="text-sm text-slate-700 line-clamp-2 max-w-xs"
                                            :title="occurrence.descripcion">{{ occurrence.descripcion }}</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div
                                                class="h-8 w-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-xs font-bold text-white shadow-md mr-3">
                                                {{ String(occurrence.vigilante || '?').charAt(0) }}
                                            </div>
                                            <div class="text-sm font-semibold text-slate-900">{{ occurrence.vigilante }}
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-center">
                                        <span
                                            class="px-3 py-1.5 inline-flex text-xs leading-5 font-bold rounded-lg bg-gradient-to-r from-green-500 to-green-600 text-white shadow-sm">
                                            {{ occurrence.estado }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button @click="openDetailModal(occurrence)"
                                            class="text-slate-400 hover:text-blue-600 transition-colors duration-200 ease-in-out p-2 hover:bg-blue-50 rounded-lg"
                                            title="Ver detalle">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                            </svg>
                                        </button>
                                    </td>
                                </tr>
                                <tr v-if="!isLoading && paginatedOccurrences.length === 0">
                                    <td colspan="6" class="px-6 py-16 text-center">
                                        <div class="flex flex-col items-center">
                                            <div class="bg-slate-100 rounded-full p-4 mb-4">
                                                <svg class="h-12 w-12 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                    stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                                                </svg>
                                            </div>
                                            <h3 class="text-lg font-bold text-slate-900 mb-1">No hay ocurrencias</h3>
                                            <p v-if="hasActiveFilters" class="text-sm text-slate-500">No se encontraron
                                                resultados con los filtros aplicados.</p>
                                            <p v-else class="text-sm text-slate-500">Registra una nueva ocurrencia para
                                                comenzar.</p>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Pagination -->
                    <div v-if="totalPages > 1" class="bg-slate-50 px-6 py-4 border-t border-slate-200">
                        <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
                            <div class="flex items-center gap-2 text-sm text-slate-600">
                                <span>Mostrar</span>
                                <select v-model="perPage" @change="currentPage = 1"
                                    class="border border-slate-200 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white">
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
                                            ? 'bg-blue-600 text-white'
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

                <!-- Modals -->
                <OccurrenceModal v-if="showRegisterModal" @close="showRegisterModal = false"
                    @saved="fetchOccurrences" />
                <OccurrenceDetailModal :show="showDetailModal" :occurrence="selectedOccurrence"
                    @close="showDetailModal = false" />

                <!-- Modal Personal Ausente -->
                <div v-if="showAbsentModal" class="fixed inset-0 z-50 overflow-y-auto">
                    <div class="flex items-center justify-center min-h-screen px-4">
                        <div class="fixed inset-0 bg-black/50 transition-opacity" @click="showAbsentModal = false">
                        </div>

                        <div class="relative bg-white rounded-2xl shadow-2xl max-w-2xl w-full z-10 overflow-hidden">
                            <!-- Header -->
                            <div
                                class="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4 flex justify-between items-center">
                                <div>
                                    <h3 class="text-xl font-bold text-white flex items-center gap-2">
                                        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                                        </svg>
                                        Personal Ausente Hoy
                                    </h3>
                                    <p class="text-purple-100 text-sm mt-1">Empleados con licencia, vacaciones u otra
                                        ausencia</p>
                                </div>
                                <button @click="showAbsentModal = false"
                                    class="text-purple-100 hover:text-white transition-colors p-1">
                                    <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>

                            <!-- Content -->
                            <div class="p-6 max-h-[60vh] overflow-y-auto">
                                <!-- Loading -->
                                <div v-if="isLoadingLicenses" class="text-center py-8">
                                    <svg class="animate-spin h-10 w-10 text-purple-600 mx-auto mb-4" fill="none"
                                        viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4">
                                        </circle>
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z">
                                        </path>
                                    </svg>
                                    <p class="text-slate-500">Cargando personal ausente...</p>
                                </div>

                                <!-- Lista de ausentes -->
                                <div v-else-if="activeLicenses.length > 0" class="space-y-3">
                                    <div v-for="person in activeLicenses" :key="person.dni"
                                        class="bg-slate-50 border border-slate-200 rounded-xl p-4 hover:bg-purple-50 transition-colors">
                                        <div class="flex items-start justify-between">
                                            <div class="flex items-center gap-3">
                                                <div
                                                    class="h-12 w-12 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm">
                                                    {{ (person.nombres || '?').charAt(0) }}{{ (person.apellidos ||
                                                        '?').charAt(0) }}
                                                </div>
                                                <div>
                                                    <p class="font-bold text-slate-900">{{ person.nombres }} {{
                                                        person.apellidos }}</p>
                                                    <p class="text-sm text-slate-500">DNI: {{ person.dni }}</p>
                                                    <p v-if="person.cargo || person.area"
                                                        class="text-sm text-slate-600">
                                                        {{ person.cargo }} {{ person.area ? '- ' + person.area : '' }}
                                                    </p>
                                                </div>
                                            </div>
                                            <div class="text-right">
                                                <span class="px-3 py-1 text-xs font-bold rounded-lg" :class="{
                                                    'bg-red-100 text-red-700': person.tipo_licencia === 'Enfermedad',
                                                    'bg-blue-100 text-blue-700': person.tipo_licencia === 'Vacaciones' || person.tipo_licencia === 'Personal',
                                                    'bg-pink-100 text-pink-700': person.tipo_licencia === 'Maternidad' || person.tipo_licencia === 'Paternidad',
                                                    'bg-gray-100 text-gray-700': !['Enfermedad', 'Vacaciones', 'Personal', 'Maternidad', 'Paternidad'].includes(person.tipo_licencia)
                                                }">
                                                    {{ person.tipo_licencia }}
                                                </span>
                                                <p class="text-xs text-slate-500 mt-2">Regresa en {{
                                                    person.dias_restantes }} día(s)</p>
                                                <p class="text-xs text-slate-400">{{ person.fecha_fin }}</p>
                                            </div>
                                        </div>
                                        <p v-if="person.motivo"
                                            class="text-sm text-slate-600 mt-2 pt-2 border-t border-slate-200">
                                            <span class="font-medium">Motivo:</span> {{ person.motivo }}
                                        </p>
                                    </div>
                                </div>

                                <!-- Sin ausentes -->
                                <div v-else class="text-center py-12">
                                    <div
                                        class="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                                        <svg class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24"
                                            stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7" />
                                        </svg>
                                    </div>
                                    <h3 class="text-lg font-bold text-slate-900 mb-1">Todo el personal presente</h3>
                                    <p class="text-sm text-slate-500">No hay empleados con licencia activa el día de
                                        hoy.</p>
                                </div>
                            </div>

                            <!-- Footer -->
                            <div
                                class="bg-slate-50 px-6 py-4 border-t border-slate-200 flex justify-between items-center">
                                <p class="text-sm text-slate-500">
                                    <span class="font-bold text-slate-700">{{ activeLicenses.length }}</span> persona(s)
                                    ausente(s)
                                </p>
                                <button @click="showAbsentModal = false"
                                    class="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-xl hover:from-purple-700 hover:to-indigo-700 transition-all">
                                    Cerrar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Reports Tab Content -->
            <div v-if="activeTab === 'reports'">
                <div class="bg-white shadow-xl rounded-2xl border border-slate-200 overflow-hidden">
                    <!-- Reports Header -->
                    <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
                        <h2 class="text-xl font-bold text-white">Reportes Semanales de Ocurrencias</h2>
                        <p class="text-indigo-100 text-sm mt-1">Generación de reportes cada viernes (Sábado a Viernes)
                        </p>
                    </div>

                    <div class="p-6">
                        <!-- Week Selector -->
                        <div class="mb-6">
                            <label class="block text-sm font-bold text-slate-700 mb-2">Seleccionar Semana</label>
                            <div class="flex gap-4 items-end">
                                <div class="flex-1">
                                    <select v-model="selectedWeek"
                                        class="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200">
                                        <option v-for="week in availableWeeks" :key="week.value" :value="week.value">
                                            {{ week.label }}
                                        </option>
                                    </select>
                                </div>
                                <button @click="generateWeeklyReport" :disabled="isGeneratingReport"
                                    class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed">
                                    <svg v-if="isGeneratingReport" class="animate-spin w-5 h-5 mr-2" fill="none"
                                        viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4">
                                        </circle>
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                                    </svg>
                                    <svg v-else class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    {{ isGeneratingReport ? 'Generando...' : 'Generar Reporte PDF' }}
                                </button>
                            </div>
                        </div>

                        <!-- Week Summary -->
                        <div v-if="weeklyReportData" class="space-y-6">
                            <!-- Stats Cards -->
                            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                                <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 text-white">
                                    <p class="text-blue-100 text-sm font-medium">Total Ocurrencias</p>
                                    <p class="text-3xl font-bold">{{ weeklyReportData.total }}</p>
                                </div>
                                <div class="bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-4 text-white">
                                    <p class="text-red-100 text-sm font-medium">Emergencias</p>
                                    <p class="text-3xl font-bold">{{ weeklyReportData.emergencias }}</p>
                                </div>
                                <div class="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl p-4 text-white">
                                    <p class="text-yellow-100 text-sm font-medium">Incidentes</p>
                                    <p class="text-3xl font-bold">{{ weeklyReportData.incidentes }}</p>
                                </div>
                                <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-4 text-white">
                                    <p class="text-green-100 text-sm font-medium">Rutina</p>
                                    <p class="text-3xl font-bold">{{ weeklyReportData.rutina }}</p>
                                </div>
                            </div>

                            <!-- Occurrences Table for Selected Week -->
                            <div class="border border-slate-200 rounded-xl overflow-hidden">
                                <div class="bg-slate-50 px-4 py-3 border-b border-slate-200">
                                    <h3 class="font-bold text-slate-700">Ocurrencias de la Semana</h3>
                                </div>
                                <div class="overflow-x-auto">
                                    <table class="min-w-full divide-y divide-slate-200">
                                        <thead class="bg-slate-50">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-bold text-slate-600 uppercase">
                                                    Fecha
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-bold text-slate-600 uppercase">
                                                    Tipo</th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-bold text-slate-600 uppercase">
                                                    Descripción</th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-bold text-slate-600 uppercase">
                                                    Responsable</th>
                                            </tr>
                                        </thead>
                                        <tbody class="divide-y divide-slate-100">
                                            <tr v-for="occ in weeklyReportData.occurrences" :key="occ.id"
                                                class="hover:bg-slate-50">
                                                <td class="px-4 py-3 text-sm text-slate-900">{{ occ.fecha }} {{ occ.hora
                                                    }}</td>
                                                <td class="px-4 py-3">
                                                    <span class="px-2 py-1 text-xs font-bold rounded-lg" :class="{
                                                        'bg-red-100 text-red-700': occ.tipo === 'Emergencia',
                                                        'bg-yellow-100 text-yellow-700': occ.tipo === 'Incidente',
                                                        'bg-green-100 text-green-700': occ.tipo === 'Rutina',
                                                        'bg-blue-100 text-blue-700': occ.tipo === 'Aviso',
                                                        'bg-gray-100 text-gray-700': occ.tipo === 'Otros'
                                                    }">{{ occ.tipo }}</span>
                                                </td>
                                                <td class="px-4 py-3 text-sm text-slate-700 max-w-xs truncate">{{
                                                    occ.descripcion }}
                                                </td>
                                                <td class="px-4 py-3 text-sm text-slate-900">{{ occ.vigilante }}</td>
                                            </tr>
                                            <tr v-if="weeklyReportData.occurrences.length === 0">
                                                <td colspan="4" class="px-4 py-8 text-center text-slate-500">
                                                    No hay ocurrencias registradas en esta semana.
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>

                        <!-- Empty state when no week selected -->
                        <div v-else class="text-center py-12">
                            <svg class="mx-auto h-12 w-12 text-slate-400" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <h3 class="mt-2 text-sm font-medium text-slate-900">Seleccione una semana</h3>
                            <p class="mt-1 text-sm text-slate-500">Elija una semana para ver el resumen y generar el
                                reporte.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '../api';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import OccurrenceModal from '../components/OccurrenceModal.vue';
import OccurrenceDetailModal from '../components/OccurrenceDetailModal.vue';

const occurrences = ref([]);
const showRegisterModal = ref(false);
const showDetailModal = ref(false);
const selectedOccurrence = ref(null);
const isLoading = ref(false);

// Personal Ausente
const showAbsentModal = ref(false);
const activeLicenses = ref([]);
const isLoadingLicenses = ref(false);

// Tabs
const activeTab = ref('list');

// Reports
const selectedWeek = ref('');
const isGeneratingReport = ref(false);
const weeklyReportData = ref(null);

// Función para cargar licencias activas
const fetchActiveLicenses = async () => {
    isLoadingLicenses.value = true;
    try {
        const response = await api.get('/license/active');
        activeLicenses.value = response.data || [];
    } catch (error) {
        console.error('Error fetching active licenses:', error);
        activeLicenses.value = [];
    } finally {
        isLoadingLicenses.value = false;
    }
};

// Generate list of available weeks (last 12 weeks ending on Friday)
const availableWeeks = computed(() => {
    const weeks = [];
    const today = new Date();

    // Find the most recent Friday
    let friday = new Date(today);
    friday.setDate(friday.getDate() - (friday.getDay() + 2) % 7);

    for (let i = 0; i < 12; i++) {
        const endDate = new Date(friday);
        endDate.setDate(endDate.getDate() - (i * 7));

        const startDate = new Date(endDate);
        startDate.setDate(startDate.getDate() - 6);

        const formatDate = (d) => d.toISOString().split('T')[0];
        const formatDisplay = (d) => d.toLocaleDateString('es-PE', { day: '2-digit', month: 'short' });

        weeks.push({
            value: `${formatDate(startDate)}_${formatDate(endDate)}`,
            label: `${formatDisplay(startDate)} - ${formatDisplay(endDate)} ${i === 0 ? '(Esta semana)' : ''}`
        });
    }
    return weeks;
});

// Watch for week selection changes
watch(selectedWeek, (newVal) => {
    if (newVal) {
        calculateWeeklyData(newVal);
    } else {
        weeklyReportData.value = null;
    }
});

// Calculate weekly report data
const calculateWeeklyData = (weekValue) => {
    const [startDate, endDate] = weekValue.split('_');

    const weekOccurrences = occurrences.value.filter(occ => {
        return occ.fecha >= startDate && occ.fecha <= endDate;
    });

    weeklyReportData.value = {
        startDate,
        endDate,
        total: weekOccurrences.length,
        emergencias: weekOccurrences.filter(o => o.tipo === 'Emergencia' || o.tipo === 'Robo').length,
        incidentes: weekOccurrences.filter(o => o.tipo === 'Incidente').length,
        rutina: weekOccurrences.filter(o => o.tipo === 'Rutina').length,
        avisos: weekOccurrences.filter(o => o.tipo === 'Aviso').length,
        otros: weekOccurrences.filter(o => o.tipo === 'Otros').length,
        occurrences: weekOccurrences.sort((a, b) => new Date(a.fecha + ' ' + a.hora) - new Date(b.fecha + ' ' + b.hora))
    };
};

// Generate PDF Report
const generateWeeklyReport = async () => {
    if (!weeklyReportData.value) return;

    isGeneratingReport.value = true;

    try {
        const doc = new jsPDF();
        const data = weeklyReportData.value;

        // Header
        doc.setFontSize(18);
        doc.setTextColor(40, 50, 100);
        doc.text('DRE Huánuco', 105, 20, { align: 'center' });

        doc.setFontSize(14);
        doc.text('Reporte Semanal de Ocurrencias', 105, 30, { align: 'center' });

        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text(`Período: ${data.startDate} al ${data.endDate}`, 105, 38, { align: 'center' });

        // Summary stats
        doc.setFontSize(11);
        doc.setTextColor(0);
        doc.text(`Total de Ocurrencias: ${data.total}`, 20, 55);
        doc.text(`Emergencias: ${data.emergencias}`, 20, 62);
        doc.text(`Incidentes: ${data.incidentes}`, 80, 62);
        doc.text(`Rutina: ${data.rutina}`, 140, 62);

        // Table
        if (data.occurrences.length > 0) {
            doc.autoTable({
                startY: 75,
                head: [['Fecha', 'Hora', 'Tipo', 'Descripción', 'Responsable']],
                body: data.occurrences.map(occ => [
                    occ.fecha,
                    occ.hora,
                    occ.tipo,
                    (occ.descripcion || '').substring(0, 50) + ((occ.descripcion || '').length > 50 ? '...' : ''),
                    occ.vigilante
                ]),
                styles: { fontSize: 8 },
                headStyles: { fillColor: [79, 70, 229] },
                alternateRowStyles: { fillColor: [245, 247, 250] }
            });
        } else {
            doc.text('No se registraron ocurrencias en este período.', 20, 80);
        }

        // Footer
        const pageCount = doc.internal.getNumberOfPages();
        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.setTextColor(150);
            doc.text(`Generado el ${new Date().toLocaleString('es-PE')} - Página ${i} de ${pageCount}`, 105, 290, { align: 'center' });
        }

        doc.save(`Reporte_Semanal_${data.startDate}_${data.endDate}.pdf`);
    } catch (error) {
        console.error('Error generating report:', error);
    } finally {
        isGeneratingReport.value = false;
    }
};

// Pagination
const currentPage = ref(1);
const perPage = ref(10);

// Filters
const filters = ref({
    search: '',
    tipo: '',
    fechaDesde: '',
    fechaHasta: ''
});

// Computed: Filtered occurrences
const filteredOccurrences = computed(() => {
    let result = [...occurrences.value];

    // Filter by search term
    if (filters.value.search) {
        const searchLower = filters.value.search.toLowerCase();
        result = result.filter(occ =>
            (occ.descripcion && occ.descripcion.toLowerCase().includes(searchLower)) ||
            (occ.vigilante && occ.vigilante.toLowerCase().includes(searchLower)) ||
            (occ.acciones && occ.acciones.toLowerCase().includes(searchLower))
        );
    }

    // Filter by type
    if (filters.value.tipo) {
        result = result.filter(occ => occ.tipo === filters.value.tipo);
    }

    // Filter by date range
    if (filters.value.fechaDesde) {
        result = result.filter(occ => occ.fecha >= filters.value.fechaDesde);
    }
    if (filters.value.fechaHasta) {
        result = result.filter(occ => occ.fecha <= filters.value.fechaHasta);
    }

    return result;
});

// Computed: Paginated occurrences
const paginatedOccurrences = computed(() => {
    const itemsPerPage = Number(perPage.value);
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredOccurrences.value.slice(start, end);
});

// Computed: Total pages
const totalPages = computed(() => {
    return Math.ceil(filteredOccurrences.value.length / Number(perPage.value)) || 1;
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
    return filters.value.search || filters.value.tipo || filters.value.fechaDesde || filters.value.fechaHasta;
});

// Reset page when filters change
watch(filters, () => {
    currentPage.value = 1;
}, { deep: true });

// Clear all filters
const clearFilters = () => {
    filters.value = {
        search: '',
        tipo: '',
        fechaDesde: '',
        fechaHasta: ''
    };
};

const fetchOccurrences = async () => {
    isLoading.value = true;
    try {
        const response = await api.get('/occurrence/dashboard');
        if (Array.isArray(response.data)) {
            occurrences.value = response.data.map(item => {
                const normalized = {};
                for (const key in item) {
                    normalized[key.toLowerCase()] = item[key];
                }
                return normalized;
            });
        } else {
            occurrences.value = [];
        }
    } catch (error) {
        console.error('Error fetching occurrences:', error);
        occurrences.value = [];
    } finally {
        isLoading.value = false;
    }
};

const openDetailModal = (occurrence) => {
    selectedOccurrence.value = occurrence;
    showDetailModal.value = true;
};

onMounted(() => {
    fetchOccurrences();
    fetchActiveLicenses();
});
</script>
