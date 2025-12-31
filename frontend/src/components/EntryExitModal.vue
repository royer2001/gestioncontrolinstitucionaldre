<template>
    <transition name="modal">
        <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <!-- Overlay -->
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-slate-900 bg-opacity-75 transition-opacity" aria-hidden="true"
                    @click="$emit('close')"></div>

                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

                <!-- Modal Panel -->
                <div
                    class="inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">

                    <!-- Header -->
                    <div
                        class="bg-gradient-to-r from-green-600 to-emerald-600 px-6 py-4 flex justify-between items-center">
                        <h3 class="text-xl font-bold text-white flex items-center gap-2">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                            </svg>
                            {{ mode === 'salida' ? 'Registrar Salida de Personal' : 'Registrar Retorno de Personal' }}
                        </h3>
                        <button @click="$emit('close')" class="text-green-100 hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Form Content -->
                    <div class="max-h-[80vh] overflow-y-auto bg-slate-50">
                        <form @submit.prevent="submitForm" class="divide-y divide-slate-100">

                            <!-- Sección 1: Búsqueda por DNI -->
                            <div class="p-6 sm:p-8 bg-white">
                                <div class="flex items-center gap-3 mb-6">
                                    <div class="bg-green-100 rounded-lg p-2">
                                        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                        </svg>
                                    </div>
                                    <h2 class="text-lg font-bold text-slate-800">Búsqueda de Personal</h2>
                                </div>

                                <div class="group">
                                    <label for="dni_search" class="block text-sm font-semibold text-slate-700 mb-2">
                                        Buscar por DNI
                                    </label>
                                    <div class="flex gap-2">
                                        <div class="relative flex-1">
                                            <div
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                    stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                                                </svg>
                                            </div>
                                            <input v-model="dni" @keyup.enter="searchPersonal" type="text"
                                                id="dni_search" autofocus maxlength="8" :disabled="!!initialEntry"
                                                :class="[
                                                    'block w-full pl-10 pr-4 py-3 border-2 border-slate-200 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                                                    initialEntry
                                                        ? 'bg-slate-100 text-slate-500 cursor-not-allowed'
                                                        : 'bg-white hover:border-green-300 focus:border-green-500 focus:ring-green-100'
                                                ]" placeholder="Ingrese DNI o escanee código">
                                        </div>
                                        <button type="button" @click="searchPersonal" :disabled="!!initialEntry" :class="[
                                            'inline-flex items-center gap-2 px-6 py-3 border-2 rounded-xl text-sm font-semibold transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                                            initialEntry
                                                ? 'border-slate-200 text-slate-400 bg-slate-100 cursor-not-allowed'
                                                : 'border-green-600 text-green-700 bg-green-50 hover:bg-green-100 focus:ring-green-200'
                                        ]">
                                            <svg v-if="!searching" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                                stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                            </svg>
                                            <svg v-else class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                    stroke-width="4"></circle>
                                                <path class="opacity-75" fill="currentColor"
                                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                                </path>
                                            </svg>
                                            <span>Buscar</span>
                                        </button>
                                    </div>

                                    <!-- Search Message -->
                                    <div v-if="searchMessage"
                                        class="mt-4 rounded-xl p-4 border-2 transition-all duration-300 ease-in-out"
                                        :class="{
                                            'bg-green-50 border-green-200': searchMessageType === 'success',
                                            'bg-yellow-50 border-yellow-200': searchMessageType === 'warning',
                                            'bg-blue-50 border-blue-200': searchMessageType === 'info'
                                        }">
                                        <div class="flex items-start gap-3">
                                            <svg v-if="searchMessageType === 'success'"
                                                class="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" fill="currentColor"
                                                viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <svg v-else-if="searchMessageType === 'info'"
                                                class="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" fill="currentColor"
                                                viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <svg v-else class="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0"
                                                fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <p class="text-sm font-medium" :class="{
                                                'text-green-800': searchMessageType === 'success',
                                                'text-yellow-800': searchMessageType === 'warning',
                                                'text-blue-800': searchMessageType === 'info'
                                            }">
                                                {{ searchMessage }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Sección 2: Datos del Personal -->
                            <div class="p-6 sm:p-8 bg-slate-50/50">
                                <div class="flex items-center gap-3 mb-6">
                                    <div class="bg-blue-100 rounded-lg p-2">
                                        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z">
                                            </path>
                                        </svg>
                                    </div>
                                    <h2 class="text-lg font-bold text-slate-800">Datos del Personal</h2>
                                </div>

                                <div class="space-y-6">
                                    <div class="group">
                                        <label for="personal" class="block text-sm font-semibold text-slate-700 mb-2">
                                            Nombre del Personal <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <div
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                <svg class="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors"
                                                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                                </svg>
                                            </div>
                                            <input v-model="personal"
                                                @input="e => personal = e.target.value.toUpperCase()"
                                                v-bind="personalProps" type="text" id="personal"
                                                :readonly="mode === 'retorno'" :class="[
                                                    'block w-full pl-10 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                                                    mode === 'retorno'
                                                        ? 'bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed'
                                                        : (errors.personal
                                                            ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100'
                                                            : 'border-slate-200 bg-white hover:border-blue-300 focus:border-blue-500 focus:ring-blue-100')
                                                ]" placeholder="Nombre completo del personal">
                                        </div>
                                        <p v-if="errors.personal"
                                            class="mt-2 text-sm text-red-600 flex items-center gap-1">
                                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            {{ errors.personal }}
                                        </p>
                                    </div>

                                    <div class="group">
                                        <label for="tipo_regimen"
                                            class="block text-sm font-semibold text-slate-700 mb-2">
                                            Tipo de Régimen <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <div
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                    stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                                </svg>
                                            </div>
                                            <select v-model="tipo_regimen" v-bind="tipoRegimenProps" id="tipo_regimen"
                                                :disabled="mode === 'retorno'" :class="[
                                                    'block w-full pl-10 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4 appearance-none',
                                                    mode === 'retorno'
                                                        ? 'bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed'
                                                        : (errors.tipo_regimen
                                                            ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100'
                                                            : 'border-slate-200 bg-white hover:border-blue-300 focus:border-blue-500 focus:ring-blue-100')
                                                ]">
                                                <option value="" disabled>Seleccione un régimen</option>
                                                <option value="CAS">CAS</option>
                                                <option value="Nombrado">Nombrado</option>
                                                <option value="Locación">Locación</option>
                                                <option value="Practicante">Practicante</option>
                                                <option value="Otro">Otro</option>
                                            </select>
                                            <div
                                                class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                                                <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                                </svg>
                                            </div>
                                        </div>
                                        <p v-if="errors.tipo_regimen"
                                            class="mt-2 text-sm text-red-600 flex items-center gap-1">
                                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            {{ errors.tipo_regimen }}
                                        </p>
                                    </div>

                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <!-- Hora de Salida (Solo editable en modo salida) -->
                                        <div class="group">
                                            <label for="hora_salida"
                                                class="block text-sm font-semibold text-slate-700 mb-2">
                                                Hora de Salida (Inicio Comisión) <span class="text-red-500">*</span>
                                            </label>
                                            <div class="relative">
                                                <div
                                                    class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                    <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                        stroke="currentColor">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                                    </svg>
                                                </div>
                                                <input v-model="hora_salida" v-bind="horaSalidaProps" type="time"
                                                    id="hora_salida" :readonly="mode === 'retorno'" :class="[
                                                        'block w-full pl-10 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                                                        mode === 'retorno' ? 'bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed' : (errors.hora_salida ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100' : 'bg-white border-slate-200 hover:border-red-300 focus:border-red-500 focus:ring-red-100')
                                                    ]">
                                            </div>
                                            <p v-if="errors.hora_salida"
                                                class="mt-2 text-sm text-red-600 flex items-center gap-1">
                                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                                    <path fill-rule="evenodd"
                                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                                        clip-rule="evenodd" />
                                                </svg>
                                                {{ errors.hora_salida }}
                                            </p>
                                        </div>

                                        <!-- Hora de Retorno (Solo editable en modo retorno) -->
                                        <div class="group">
                                            <label for="hora_entrada"
                                                class="block text-sm font-semibold text-slate-700 mb-2">
                                                Hora de Retorno (Fin Comisión)
                                            </label>
                                            <div class="relative">
                                                <div
                                                    class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                    <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                        stroke="currentColor">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                                                    </svg>
                                                </div>
                                                <input v-model="hora_entrada" v-bind="horaEntradaProps" type="time"
                                                    id="hora_entrada" :readonly="mode === 'salida'" :class="[
                                                        'block w-full pl-10 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                                                        mode === 'salida' ? 'bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed' : (errors.hora_entrada ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100' : 'bg-white border-slate-200 hover:border-green-300 focus:border-green-500 focus:ring-green-100')
                                                    ]">
                                            </div>
                                            <p v-if="errors.hora_entrada"
                                                class="mt-2 text-sm text-red-600 flex items-center gap-1">
                                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                                    <path fill-rule="evenodd"
                                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                                        clip-rule="evenodd" />
                                                </svg>
                                                {{ errors.hora_entrada }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Sección 3: Detalles Adicionales -->
                            <div class="p-6 sm:p-8 bg-white">
                                <div class="flex items-center gap-3 mb-6">
                                    <div class="bg-indigo-100 rounded-lg p-2">
                                        <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                                            </path>
                                        </svg>
                                    </div>
                                    <h2 class="text-lg font-bold text-slate-800">Detalles Adicionales</h2>
                                </div>

                                <div class="space-y-6">
                                    <div class="group">
                                        <label for="motivo" class="block text-sm font-semibold text-slate-700 mb-2">
                                            Motivo <span class="text-red-500">*</span>
                                        </label>
                                        <textarea v-model="motivo" v-bind="motivoProps" id="motivo" rows="3"
                                            :readonly="mode === 'retorno'" :class="[
                                                'block w-full px-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out resize-none focus:outline-none focus:ring-4',
                                                mode === 'retorno' ? 'bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed' : (errors.motivo ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 bg-white hover:border-indigo-300 focus:border-indigo-500 focus:ring-indigo-100')
                                            ]" placeholder="Describa el motivo del ingreso/salida..."></textarea>
                                        <p v-if="errors.motivo"
                                            class="mt-2 text-sm text-red-600 flex items-center gap-1">
                                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            {{ errors.motivo }}
                                        </p>
                                    </div>

                                    <div class="group">
                                        <label for="papeleta" class="block text-sm font-semibold text-slate-700 mb-2">
                                            Número de Papeleta
                                        </label>
                                        <div class="relative">
                                            <div
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                <svg class="h-5 w-5 text-slate-400 group-focus-within:text-indigo-500 transition-colors"
                                                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                                </svg>
                                            </div>
                                            <input v-model="papeleta" v-bind="papeletaProps" type="text" id="papeleta"
                                                readonly :class="[
                                                    'block w-full pl-10 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                                                    'bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed'
                                                ]" placeholder="Generado automáticamente">
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Footer / Actions -->
                            <div
                                class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-end gap-3">
                                <button type="button" @click="$emit('close')"
                                    class="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 border-2 border-slate-300 rounded-xl text-sm font-semibold text-slate-700 bg-white hover:bg-slate-50 hover:border-slate-400 focus:outline-none focus:ring-4 focus:ring-slate-200 transition-all duration-200 ease-in-out">
                                    Cancelar
                                </button>
                                <button type="submit" :disabled="isSubmitting"
                                    class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-transparent rounded-xl text-sm font-bold text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-4 focus:ring-green-300 shadow-lg hover:shadow-xl transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed">
                                    <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                        </path>
                                    </svg>
                                    <svg v-else class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M5 13l4 4L19 7" />
                                    </svg>
                                    {{ isSubmitting ? 'Guardando...' : (mode === 'salida' ? 'Registrar Salida' :
                                        'Registrar Retorno') }}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import * as yup from 'yup';
import api from '../api';
import Swal from 'sweetalert2';

const props = defineProps({
    initialEntry: {
        type: Object,
        default: null
    }
});

const emit = defineEmits(['close', 'saved']);

const dni = ref('');
const searching = ref(false);
const searchMessage = ref('');
const searchMessageType = ref('');
const mode = ref('salida'); // 'salida' | 'retorno'
const currentEntryId = ref(null);
let messageTimeout = null;

onMounted(() => {
    console.log('Modal Mounted. InitialEntry:', props.initialEntry);
    if (props.initialEntry) {
        mode.value = 'retorno';
        // Usar entry_id que es como viene del backend, o id como fallback
        currentEntryId.value = props.initialEntry.entry_id || props.initialEntry.id;
        console.log('Set currentEntryId to:', currentEntryId.value);
        setFieldValue('personal', props.initialEntry.personal);
        setFieldValue('hora_salida', props.initialEntry.hora_salida);
        setFieldValue('motivo', props.initialEntry.motivo);
        setFieldValue('papeleta', props.initialEntry.papeleta || '');
        setFieldValue('tipo_regimen', props.initialEntry.tipo_regimen || '');

        if (props.initialEntry.dni) {
            dni.value = props.initialEntry.dni;
        }

        // Pre-llenar hora de retorno actual
        const now = new Date();
        const timeString = now.toTimeString().slice(0, 5);
        setFieldValue('hora_entrada', timeString);

        searchMessage.value = 'Registrando retorno para el registro seleccionado.';
        searchMessageType.value = 'info';
    }
});

const schema = computed(() => {
    return toTypedSchema(
        yup.object({
            personal: yup.string().required('El nombre del personal es obligatorio'),
            hora_salida: yup.string().required('La hora de salida es obligatoria'),
            hora_entrada: mode.value === 'retorno'
                ? yup.string().required('La hora de retorno es obligatoria')
                : yup.string().nullable(),
            motivo: yup.string().required('El motivo es obligatorio'),
            papeleta: yup.string().nullable(),
            tipo_regimen: yup.string().required('El tipo de régimen es obligatorio'),
        })
    );
});

const { errors, defineField, handleSubmit, setFieldValue, resetForm } = useForm({
    validationSchema: schema,
    initialValues: {
        personal: '',
        hora_entrada: '',
        hora_salida: '',
        motivo: '',
        papeleta: '',
        tipo_regimen: '',
    },
    validateOnBlur: true,
    validateOnChange: true,
    validateOnInput: false,
    validateOnModelUpdate: true,
});

const [personal, personalProps] = defineField('personal');
const [hora_entrada, horaEntradaProps] = defineField('hora_entrada');
const [hora_salida, horaSalidaProps] = defineField('hora_salida');
const [motivo, motivoProps] = defineField('motivo');
const [papeleta, papeletaProps] = defineField('papeleta');
const [tipo_regimen, tipoRegimenProps] = defineField('tipo_regimen');

const searchPersonal = async () => {
    if (!dni.value || dni.value.length < 8) return;

    if (messageTimeout) clearTimeout(messageTimeout);
    searching.value = true;
    searchMessage.value = '';

    try {
        const response = await api.get(`/entry_exit/search_personal/${dni.value}`);
        if (response.data.nombre) {
            setFieldValue('personal', response.data.nombre);

            if (response.data.status === 'fuera') {
                mode.value = 'retorno';
                currentEntryId.value = response.data.entry_id;
                setFieldValue('hora_salida', response.data.hora_salida);
                setFieldValue('motivo', response.data.motivo);
                setFieldValue('tipo_regimen', response.data.tipo_regimen || '');

                // Pre-llenar hora de retorno actual
                const now = new Date();
                const timeString = now.toTimeString().slice(0, 5);
                setFieldValue('hora_entrada', timeString);

                searchMessage.value = 'Personal con salida pendiente. Registre retorno.';
                searchMessageType.value = 'info';
            } else {
                mode.value = 'salida';
                currentEntryId.value = null;
                setFieldValue('hora_entrada', '');
                setFieldValue('motivo', '');
                setFieldValue('papeleta', '');
                setFieldValue('tipo_regimen', '');

                // Pre-llenar hora de salida actual
                const now = new Date();
                const timeString = now.toTimeString().slice(0, 5);
                setFieldValue('hora_salida', timeString);

                searchMessage.value = 'Personal encontrado. Registre salida.';
                searchMessageType.value = 'success';
            }
        }
    } catch (error) {
        console.log('Personal no encontrado');
        searchMessage.value = 'No se encontró el DNI. Verifique o registre manualmente.';
        searchMessageType.value = 'warning';
        mode.value = 'salida'; // Default a salida si no se encuentra
    } finally {
        searching.value = false;
        if (searchMessage.value) {
            messageTimeout = setTimeout(() => {
                searchMessage.value = '';
                searchMessageType.value = '';
            }, 5000);
        }
    }
};

const isSubmitting = ref(false);

const submitForm = handleSubmit(async (values) => {
    if (isSubmitting.value) return;
    isSubmitting.value = true;

    try {
        const user = JSON.parse(localStorage.getItem('user'));

        const response = await api.post('/entry_exit/register', {
            ...values,
            dni: dni.value, // Include DNI in the payload
            username: user ? user.usuario : 'unknown',
            action: mode.value,
            entry_id: currentEntryId.value
        });

        const papeletaNum = response.data.papeleta;
        const newEntryId = response.data.entry_id;

        const result = await Swal.fire({
            icon: 'success',
            title: mode.value === 'salida' ? '¡Salida Registrada!' : '¡Retorno Registrado!',
            text: mode.value === 'salida'
                ? `Se ha registrado la salida del personal. Papeleta: ${papeletaNum || 'N/A'}`
                : 'Se ha registrado el retorno del personal.',
            showConfirmButton: mode.value === 'salida',
            showCancelButton: true,
            confirmButtonText: 'Descargar Papeleta',
            cancelButtonText: 'Cerrar',
            confirmButtonColor: '#10B981',
            cancelButtonColor: '#6B7280'
        });

        if (result.isConfirmed && mode.value === 'salida' && newEntryId) {
            window.open(`${api.defaults.baseURL}/entry_exit/generate_pdf/${newEntryId}`, '_blank');
        }

        emit('saved');
        emit('close');
        resetForm();
        dni.value = '';
        mode.value = 'salida';
        currentEntryId.value = null;

    } catch (error) {
        console.error(error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un problema al guardar el registro.',
        });
    } finally {
        isSubmitting.value = false;
    }
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.modal-enter-active .transform,
.modal-leave-active .transform {
    transition: all 0.3s ease-out;
}

.modal-enter-from .transform,
.modal-leave-to .transform {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
}
</style>
