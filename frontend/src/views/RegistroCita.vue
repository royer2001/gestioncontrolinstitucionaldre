<template>
    <div class="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-4xl">
            <div class="text-center mb-8">
                <img src="../assets/logo.png" alt="DRE Huánuco" class="mx-auto h-20 w-auto">
                <h2 class="mt-6 text-3xl font-extrabold text-slate-900">
                    Portal de Citas en Línea
                </h2>
                <p class="mt-2 text-sm text-slate-600">
                    Dirección Regional de Educación Huánuco
                </p>
            </div>

            <div class="bg-white py-8 px-4 shadow-xl sm:rounded-xl sm:px-10 border border-slate-100">
                <!-- Tabs -->
                <div class="border-b border-gray-200 mb-6">
                    <nav class="-mb-px flex space-x-8" aria-label="Tabs">
                        <button @click="activeTab = 'register'"
                            :class="[activeTab === 'register' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center']">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4v16m8-8H4" />
                            </svg>
                            Nueva Cita
                        </button>
                        <button @click="activeTab = 'consult'"
                            :class="[activeTab === 'consult' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center']">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            Consultar Estado
                        </button>
                    </nav>
                </div>

                <!-- Registration Form -->
                <div v-if="activeTab === 'register'">
                    <form @submit.prevent="handleRegister" class="space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- DNI -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">DNI <span
                                        class="text-red-500">*</span></label>
                                <input v-model="dni" v-bind="dniProps" type="text" maxlength="8"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.dni ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                <p v-if="formErrors.dni" class="mt-1 text-sm text-red-600">{{ formErrors.dni }}</p>
                            </div>

                            <!-- Oficina -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Oficina de Destino <span
                                        class="text-red-500">*</span></label>
                                <select v-model="oficina" v-bind="oficinaProps"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.oficina ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                    <option value="">Seleccione una oficina</option>
                                    <option>Dirección</option>
                                    <option>Administración</option>
                                    <option>Gestión Pedagógica</option>
                                    <option>Gestión Institucional</option>
                                    <option>Asesoría Jurídica</option>
                                    <option>Recursos Humanos</option>
                                    <option>Mesa de Partes</option>
                                </select>
                                <p v-if="formErrors.oficina" class="mt-1 text-sm text-red-600">{{ formErrors.oficina }}
                                </p>
                            </div>

                            <!-- Apellidos -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Apellidos <span
                                        class="text-red-500">*</span></label>
                                <input v-model="apellidos" v-bind="apellidosProps" type="text"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.apellidos ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                <p v-if="formErrors.apellidos" class="mt-1 text-sm text-red-600">{{ formErrors.apellidos
                                }}</p>
                            </div>

                            <!-- Nombres -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Nombres <span
                                        class="text-red-500">*</span></label>
                                <input v-model="nombres" v-bind="nombresProps" type="text"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.nombres ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                <p v-if="formErrors.nombres" class="mt-1 text-sm text-red-600">{{ formErrors.nombres }}
                                </p>
                            </div>

                            <!-- Celular -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Número de Celular <span
                                        class="text-red-500">*</span></label>
                                <input v-model="celular" v-bind="celularProps" type="tel" maxlength="9"
                                    placeholder="9XXXXXXXX"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.celular ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                <p v-if="formErrors.celular" class="mt-1 text-sm text-red-600">{{ formErrors.celular }}
                                </p>
                            </div>

                            <!-- Correo -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Correo Electrónico <span
                                        class="text-red-500">*</span></label>
                                <input v-model="correo" v-bind="correoProps" type="email"
                                    placeholder="ejemplo@correo.com"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.correo ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                <p v-if="formErrors.correo" class="mt-1 text-sm text-red-600">{{ formErrors.correo }}
                                </p>
                            </div>

                            <!-- Fecha -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Fecha de Cita <span
                                        class="text-red-500">*</span></label>
                                <input v-model="fecha" v-bind="fechaProps" type="date" :min="today"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.fecha ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                <p v-if="formErrors.fecha" class="mt-1 text-sm text-red-600">{{ formErrors.fecha }}</p>
                            </div>

                            <!-- Hora -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Horario Disponible <span
                                        class="text-red-500">*</span></label>
                                <select v-model="hora" v-bind="horaProps"
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.hora ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                    <option value="">Seleccione una hora</option>
                                    <option v-for="time in timeSlots" :key="time" :value="time">{{ time }}</option>
                                </select>
                                <p v-if="formErrors.hora" class="mt-1 text-sm text-red-600">{{ formErrors.hora }}</p>
                            </div>

                            <!-- Asunto -->
                            <div class="md:col-span-2">
                                <label class="block text-sm font-medium text-gray-700">Asunto de la Reserva <span
                                        class="text-red-500">*</span></label>
                                <textarea v-model="asunto" v-bind="asuntoProps" rows="3"
                                    placeholder="Describa el motivo de su cita..."
                                    :class="['mt-1 block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        formErrors.asunto ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']"></textarea>
                                <p v-if="formErrors.asunto" class="mt-1 text-sm text-red-600">{{ formErrors.asunto }}
                                </p>
                            </div>

                            <!-- CAPTCHA -->
                            <div class="md:col-span-2 bg-gray-50 rounded-lg p-4 border border-gray-200">
                                <div class="flex items-center gap-4">
                                    <div class="flex items-center gap-2">
                                        <svg class="w-5 h-5 text-blue-500" fill="none" viewBox="0 0 24 24"
                                            stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                        </svg>
                                        <span class="text-sm font-medium text-gray-700">Verificación de seguridad</span>
                                    </div>
                                    <button type="button" @click="generateCaptcha"
                                        class="text-blue-600 hover:text-blue-800 text-sm">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                        </svg>
                                    </button>
                                </div>
                                <div class="mt-3 flex items-center gap-4">
                                    <div
                                        class="bg-white border-2 border-dashed border-gray-300 rounded-lg px-4 py-2 font-mono text-lg font-bold text-gray-700 select-none">
                                        {{ captcha.num1 }} {{ captcha.operator }} {{ captcha.num2 }} = ?
                                    </div>
                                    <div>
                                        <input v-model="captchaAnswer" type="number" placeholder="Respuesta"
                                            @keyup.enter="handleRegister"
                                            :class="['w-28 rounded-md shadow-sm sm:text-sm border p-2 text-center font-semibold transition-colors',
                                                captchaError ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                        <p v-if="captchaError" class="mt-1 text-sm text-red-600">{{ captchaError }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="flex justify-end pt-4">
                            <button type="submit" :disabled="loading"
                                class="ml-3 inline-flex justify-center py-3 px-6 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
                                <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none"
                                    viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                        stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                    </path>
                                </svg>
                                {{ loading ? 'Procesando...' : 'Reservar Cita' }}
                            </button>
                        </div>
                    </form>
                </div>

                <!-- Consult Status -->
                <div v-if="activeTab === 'consult'" class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Ingrese su DNI para consultar sus
                            citas</label>
                        <div class="flex gap-4">
                            <div class="flex-1">
                                <input v-model="consultDniInput" type="text" placeholder="Ingrese su DNI (8 dígitos)"
                                    maxlength="8" @keyup.enter="consultCitas"
                                    :class="['block w-full rounded-md shadow-sm sm:text-sm border p-2 transition-colors',
                                        consultDniError ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500']">
                                <p v-if="consultDniError" class="mt-1 text-sm text-red-600">{{ consultDniError }}</p>
                            </div>
                            <button @click="consultCitas" :disabled="consultLoading"
                                class="inline-flex justify-center py-2 px-6 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none h-fit disabled:opacity-50 disabled:cursor-not-allowed transition-opacity">
                                <svg v-if="consultLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                                    fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                        stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                    </path>
                                </svg>
                                <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                                {{ consultLoading ? 'Buscando...' : 'Buscar' }}
                            </button>
                        </div>
                    </div>

                    <!-- Skeleton Loader -->
                    <div v-if="consultLoading" class="mt-6 space-y-6">
                        <div v-for="i in 2" :key="i" class="border rounded-xl p-6 bg-white animate-pulse">
                            <div class="flex justify-between items-start mb-4">
                                <div class="space-y-2">
                                    <div class="h-6 bg-gray-200 rounded w-48"></div>
                                    <div class="h-4 bg-gray-100 rounded w-32"></div>
                                    <div class="h-3 bg-gray-50 rounded w-24"></div>
                                </div>
                                <div class="h-10 bg-gray-200 rounded-full w-28"></div>
                            </div>
                            <div class="py-4 border-t border-b border-gray-100 mt-4">
                                <div class="h-3 bg-gray-100 rounded w-20 mb-4"></div>
                                <div class="flex justify-center items-center gap-12 relative h-20">
                                    <div class="w-12 h-12 bg-gray-200 rounded-full"></div>
                                    <div class="w-20 h-[2px] bg-gray-100"></div>
                                    <div class="w-12 h-12 bg-gray-200 rounded-full"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="consultResults.length > 0 && !consultLoading" class="mt-6 space-y-6">
                        <div v-for="cita in consultResults" :key="cita.id"
                            class="border rounded-xl p-6 bg-white shadow-sm hover:shadow-md transition-shadow">

                            <!-- Header -->
                            <div class="flex flex-wrap justify-between items-start gap-4 mb-4">
                                <div>
                                    <p class="font-bold text-lg text-gray-800">{{ cita.fecha }} - {{ cita.hora }}</p>
                                    <p class="text-sm text-gray-600">{{ cita.oficina }}</p>
                                    <p class="text-xs text-gray-400 mt-1 font-mono">ID: {{ cita.id.slice(0, 8) }}...</p>
                                </div>
                                <span :class="{
                                    'bg-yellow-100 text-yellow-800 border-yellow-300': cita.estado === 'PENDIENTE',
                                    'bg-green-100 text-green-800 border-green-300': cita.estado === 'ATENDIDO',
                                    'bg-red-100 text-red-800 border-red-300': cita.estado === 'CANCELADO'
                                }" class="px-4 py-2 rounded-full text-sm font-bold border">
                                    {{ cita.estado }}
                                </span>
                            </div>

                            <!-- Stepper Horizontal - Fixed Steps -->
                            <div class="mb-4 py-4 border-t border-b border-gray-100">
                                <p class="text-xs text-gray-500 uppercase tracking-wider mb-4 font-semibold">Estado de
                                    la Cita</p>

                                <!-- Stepper Container -->
                                <div class="relative flex items-start justify-center">
                                    <!-- Connecting Line (behind circles) -->
                                    <div class="absolute top-6 left-1/2 -translate-x-1/2 w-[120px] h-[2px]"
                                        :class="cita.estado !== 'PENDIENTE' ? 'bg-gradient-to-r from-blue-400 to-green-400' : 'bg-gray-300'">
                                    </div>

                                    <!-- Step 1: Registrada -->
                                    <div class="flex flex-col items-center z-10">
                                        <div
                                            class="w-12 h-12 rounded-full flex items-center justify-center font-semibold text-lg bg-white border-[3px] border-blue-500 text-blue-500">
                                            1
                                        </div>
                                        <p class="mt-2 text-sm font-medium text-blue-600">Registrada</p>
                                        <p class="text-xs text-gray-400">{{ cita.created_at ?
                                            formatHistorialDate(cita.created_at) : '' }}</p>
                                    </div>

                                    <!-- Spacer -->
                                    <div class="w-[72px]"></div>

                                    <!-- Step 2: Finalizado -->
                                    <div class="flex flex-col items-center z-10">
                                        <div :class="{
                                            'border-green-500 text-green-500': cita.estado === 'ATENDIDO',
                                            'border-red-500 text-red-500': cita.estado === 'CANCELADO',
                                            'border-gray-300 text-gray-300': cita.estado === 'PENDIENTE'
                                        }"
                                            class="w-12 h-12 rounded-full flex items-center justify-center font-semibold text-lg bg-white border-[3px]">
                                            <svg v-if="cita.estado === 'ATENDIDO'" class="w-6 h-6" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                                                    d="M5 13l4 4L19 7" />
                                            </svg>
                                            <svg v-else-if="cita.estado === 'CANCELADO'" class="w-6 h-6" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                                                    d="M6 18L18 6M6 6l12 12" />
                                            </svg>
                                            <span v-else>2</span>
                                        </div>
                                        <p class="mt-2 text-sm font-medium" :class="{
                                            'text-green-600': cita.estado === 'ATENDIDO',
                                            'text-red-600': cita.estado === 'CANCELADO',
                                            'text-gray-400': cita.estado === 'PENDIENTE'
                                        }">
                                            {{ cita.estado === 'ATENDIDO' ? 'Atendida' : cita.estado === 'CANCELADO' ?
                                                'Cancelada' : 'Finalización' }}
                                        </p>
                                        <p v-if="cita.estado !== 'PENDIENTE'" class="text-xs text-gray-400">
                                            {{ getFinalizationDate(cita) }}
                                        </p>
                                        <p v-else class="text-xs text-gray-300">Pendiente</p>
                                    </div>
                                </div>
                            </div>

                            <!-- Finalization Observation (Reason) -->
                            <div v-if="cita.estado !== 'PENDIENTE' && getLatestObservation(cita)"
                                class="mt-4 p-4 bg-slate-50 rounded-xl border border-slate-200 mb-4">
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

                            <!-- Action -->
                            <div class="flex justify-end">
                                <button @click="generateVoucher(cita)"
                                    class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
                                    <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    Ver Voucher
                                </button>
                            </div>
                        </div>
                    </div>
                    <div v-else-if="consultSearched" class="text-center text-gray-500 py-8">
                        No se encontraron citas para el DNI ingresado.
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import * as yup from 'yup';
import api from '../api';
import Swal from 'sweetalert2';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import logoUrl from '../assets/logo.png';

const activeTab = ref('register');
const loading = ref(false);
const today = new Date().toISOString().split('T')[0];

// Validation Schema for Registration Form
const registrationSchema = toTypedSchema(
    yup.object({
        dni: yup.string()
            .required('El DNI es obligatorio')
            .matches(/^\d{8}$/, 'El DNI debe tener 8 dígitos'),
        oficina: yup.string()
            .required('Debe seleccionar una oficina'),
        apellidos: yup.string()
            .required('Los apellidos son obligatorios')
            .min(2, 'Mínimo 2 caracteres'),
        nombres: yup.string()
            .required('Los nombres son obligatorios')
            .min(2, 'Mínimo 2 caracteres'),
        celular: yup.string()
            .required('El celular es obligatorio')
            .matches(/^9\d{8}$/, 'El celular debe tener 9 dígitos y empezar con 9'),
        correo: yup.string()
            .required('El correo es obligatorio')
            .email('Ingrese un correo válido'),
        fecha: yup.string()
            .required('Debe seleccionar una fecha'),
        hora: yup.string()
            .required('Debe seleccionar una hora'),
        asunto: yup.string()
            .required('El asunto es obligatorio')
            .min(10, 'El asunto debe tener al menos 10 caracteres')
    })
);

const { errors: formErrors, defineField, handleSubmit: validateForm, resetForm } = useForm({
    validationSchema: registrationSchema,
});

const [dni, dniProps] = defineField('dni');
const [oficina, oficinaProps] = defineField('oficina');
const [apellidos, apellidosProps] = defineField('apellidos');
const [nombres, nombresProps] = defineField('nombres');
const [celular, celularProps] = defineField('celular');
const [correo, correoProps] = defineField('correo');
const [fecha, fechaProps] = defineField('fecha');
const [hora, horaProps] = defineField('hora');
const [asunto, asuntoProps] = defineField('asunto');

// Consult Form Validation
const consultDniInput = ref('');
const consultDniError = ref('');

// CAPTCHA
const captcha = ref({ num1: 0, num2: 0, operator: '+', answer: 0 });
const captchaAnswer = ref('');
const captchaError = ref('');

const generateCaptcha = () => {
    const operators = ['+', '-', 'x'];
    const operator = operators[Math.floor(Math.random() * operators.length)];
    let num1, num2, answer;

    if (operator === '+') {
        num1 = Math.floor(Math.random() * 20) + 1;
        num2 = Math.floor(Math.random() * 20) + 1;
        answer = num1 + num2;
    } else if (operator === '-') {
        num1 = Math.floor(Math.random() * 20) + 10;
        num2 = Math.floor(Math.random() * num1);
        answer = num1 - num2;
    } else {
        num1 = Math.floor(Math.random() * 10) + 1;
        num2 = Math.floor(Math.random() * 10) + 1;
        answer = num1 * num2;
    }

    captcha.value = { num1, num2, operator, answer };
    captchaAnswer.value = '';
    captchaError.value = '';
};

// Initialize CAPTCHA on mount
generateCaptcha();

// Generate Time Slots
const timeSlots = computed(() => {
    const slots = [];
    let startHour = 8;
    let startMin = 0;
    const endHour = 17;
    const endMin = 30;

    while (startHour < endHour || (startHour === endHour && startMin <= endMin)) {
        const h = startHour.toString().padStart(2, '0');
        const m = startMin.toString().padStart(2, '0');
        slots.push(`${h}:${m}`);

        startMin += 30;
        if (startMin >= 60) {
            startMin = 0;
            startHour++;
        }
    }
    return slots;
});

// CAPTCHA Validation Function
const validateCaptcha = () => {
    captchaError.value = '';
    if (!captchaAnswer.value) {
        captchaError.value = 'Por favor resuelva la operación matemática';
        return false;
    }
    if (parseInt(captchaAnswer.value) !== captcha.value.answer) {
        captchaError.value = 'Respuesta incorrecta. Intente nuevamente.';
        generateCaptcha();
        return false;
    }
    return true;
};

// Form Submit Handler
const onSubmitForm = validateForm(async (values) => {
    loading.value = true;
    try {
        const response = await api.post('/citas/request', values);
        const citaData = { ...values, id: response.data.id, estado: 'PENDIENTE' };

        await Swal.fire({
            icon: 'success',
            title: 'Cita Registrada',
            text: 'Su cita ha sido registrada con éxito. Se generará su constancia.',
            confirmButtonText: 'Descargar Voucher',
        }).then((result) => {
            if (result.isConfirmed) {
                generateVoucher(citaData);
            }
        });

        // Reset form
        resetForm();
        generateCaptcha();
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.response?.data?.message || 'Hubo un error al registrar la cita'
        });
    } finally {
        loading.value = false;
    }
});

// Main handler that validates CAPTCHA first
const handleRegister = () => {
    // Always validate CAPTCHA first (before vee-validate)
    if (!validateCaptcha()) {
        return;
    }
    // If CAPTCHA is valid, proceed with form validation
    onSubmitForm();
};

// Consult Logic
const consultResults = ref([]);
const consultSearched = ref(false);
const consultLoading = ref(false);

const validateConsultDni = () => {
    consultDniError.value = '';
    if (!consultDniInput.value) {
        consultDniError.value = 'Ingrese su DNI';
        return false;
    }
    if (!/^\d{8}$/.test(consultDniInput.value)) {
        consultDniError.value = 'El DNI debe tener 8 dígitos';
        return false;
    }
    return true;
};

const formatHistorialDate = (dateStr) => {
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

const getFinalizationDate = (cita) => {
    // Try to get the date from history first
    if (cita.historial && cita.historial.length > 1) {
        const lastEntry = cita.historial[cita.historial.length - 1];
        if (lastEntry?.fecha) {
            return formatHistorialDate(lastEntry.fecha);
        }
    }
    // Fallback to current date if no history available
    return formatHistorialDate(new Date().toISOString());
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

const consultCitas = async () => {
    if (!validateConsultDni()) return;

    consultLoading.value = true;
    try {
        const response = await api.get(`/citas/status/${consultDniInput.value}`);
        consultResults.value = response.data;
        consultSearched.value = true;
    } catch (error) {
        console.error(error);
        consultResults.value = [];
    } finally {
        consultLoading.value = false;
    }
};


const generateVoucher = (cita) => {
    const doc = new jsPDF();

    // Header
    // Add Logo if available
    try {
        doc.addImage(logoUrl, 'PNG', 20, 10, 25, 25);
    } catch (e) {
        console.warn('Could not add logo to PDF', e);
    }

    doc.setFontSize(22);
    doc.setTextColor(40, 50, 100);
    doc.text('DRE Huánuco', 105, 20, { align: 'center' });

    doc.setFontSize(12);
    doc.setTextColor(100);
    doc.text('Constancia de Cita Electrónica', 105, 30, { align: 'center' });

    // Status Badge
    const estado = cita.estado || 'PENDIENTE';
    let estadoColor = [200, 150, 0]; // Yellow for PENDIENTE
    if (estado === 'ATENDIDO') estadoColor = [0, 150, 50];
    if (estado === 'CANCELADO') estadoColor = [200, 50, 50];

    doc.setFillColor(...estadoColor);
    doc.roundedRect(75, 35, 60, 10, 3, 3, 'F');
    doc.setFontSize(10);
    doc.setTextColor(255, 255, 255);
    doc.text(`Estado: ${estado}`, 105, 42, { align: 'center' });

    // Content
    doc.setDrawColor(200);
    doc.line(20, 50, 190, 50);

    const startY = 60;
    const lineHeight = 12;

    doc.setFontSize(11);
    doc.setTextColor(50);

    const addRow = (label, value, y) => {
        doc.setFont('helvetica', 'bold');
        doc.text(`${label}:`, 30, y);
        doc.setFont('helvetica', 'normal');
        doc.text(String(value || 'N/A'), 85, y);
    };

    addRow('ID de Cita', cita.id, startY);
    addRow('Fecha', cita.fecha, startY + lineHeight);
    addRow('Hora', cita.hora, startY + lineHeight * 2);
    addRow('Oficina', cita.oficina, startY + lineHeight * 3);
    addRow('Solicitante', `${cita.nombres || ''} ${cita.apellidos || ''}`.trim() || 'N/A', startY + lineHeight * 4);
    addRow('DNI', cita.dni, startY + lineHeight * 5);
    addRow('Celular', cita.celular, startY + lineHeight * 6);
    addRow('Correo', cita.correo, startY + lineHeight * 7);

    // Asunto with text wrapping
    doc.setFont('helvetica', 'bold');
    doc.text('Asunto:', 30, startY + lineHeight * 8);
    doc.setFont('helvetica', 'normal');
    const asuntoLines = doc.splitTextToSize(String(cita.asunto || 'N/A'), 100);
    doc.text(asuntoLines, 85, startY + lineHeight * 8);

    // Footer
    doc.setFontSize(8);
    doc.setTextColor(150);
    doc.text('Este documento sirve como constancia de su reserva de cita.', 105, 270, { align: 'center' });
    doc.text('Presente este documento el día de su cita.', 105, 275, { align: 'center' });
    doc.text(`Generado el: ${new Date().toLocaleString()}`, 105, 280, { align: 'center' });

    // Open in new tab instead of downloading
    const pdfUrl = doc.output('bloburl');
    window.open(pdfUrl, '_blank');
};
</script>
