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
                    class="inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">

                    <!-- Header -->
                    <div
                        class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex justify-between items-center">
                        <h3 class="text-xl font-bold text-white flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            Registrar Nueva Ocurrencia
                        </h3>
                        <button @click="$emit('close')" class="text-blue-100 hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Form Content -->
                    <div class="bg-slate-50">
                        <form @submit="submitForm" class="divide-y divide-slate-100">

                            <!-- Sección 1: Información General -->
                            <div class="p-6">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div class="group">
                                        <label class="block text-sm font-semibold text-slate-700 mb-2">Turno
                                            Actual</label>
                                        <div class="relative">
                                            <div
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                    stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                            </div>
                                            <select v-model="turno" v-bind="turnoProps" disabled
                                                class="block w-full pl-10 pr-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-xl text-slate-500 cursor-not-allowed focus:outline-none">
                                                <option value="Mañana">🌅 Mañana</option>
                                                <option value="Tarde">☀️ Tarde</option>
                                                <option value="Noche">🌙 Noche</option>
                                            </select>
                                        </div>
                                    </div>

                                    <div class="group">
                                        <label class="block text-sm font-semibold text-slate-700 mb-2">Tipo de
                                            Ocurrencia <span class="text-red-500">*</span></label>
                                        <div class="relative">
                                            <div
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24"
                                                    stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                                </svg>
                                            </div>
                                            <select v-model="tipo" v-bind="tipoProps"
                                                :class="['block w-full pl-10 pr-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 transition-all', errors.tipo ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 bg-white focus:border-blue-500 focus:ring-blue-100']">
                                                <option value="Incidente">⚠️ Incidente</option>
                                                <option value="Aviso">📢 Aviso</option>
                                                <option value="Emergencia">🚨 Emergencia</option>
                                                <option value="Rutina">✅ Rutina</option>
                                                <option value="Robo">🔒 Robo</option>
                                                <option value="Otros">📋 Otros</option>
                                            </select>
                                        </div>
                                        <p v-if="errors.tipo" class="mt-1 text-xs text-red-600 font-medium">{{
                                            errors.tipo }}</p>
                                    </div>
                                </div>
                            </div>

                            <!-- Sección 2: Detalles -->
                            <div class="p-6 bg-slate-50/50">
                                <div class="space-y-4">
                                    <div class="group">
                                        <label class="block text-sm font-semibold text-slate-700 mb-2">Descripción
                                            Detallada <span class="text-red-500">*</span></label>
                                        <textarea v-model="descripcion" v-bind="descripcionProps" rows="4"
                                            :class="['block w-full px-4 py-3 border-2 rounded-xl resize-none focus:outline-none focus:ring-4 transition-all', errors.descripcion ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 bg-white focus:border-blue-500 focus:ring-blue-100']"
                                            placeholder="Describa el incidente..."></textarea>
                                        <p v-if="errors.descripcion" class="mt-1 text-xs text-red-600 font-medium">{{
                                            errors.descripcion }}</p>
                                    </div>

                                    <div class="group">
                                        <label class="block text-sm font-semibold text-slate-700 mb-2">Acciones
                                            Tomadas</label>
                                        <textarea v-model="acciones" v-bind="accionesProps" rows="3"
                                            class="block w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-100 focus:outline-none transition-all resize-none"
                                            placeholder="Medidas tomadas..."></textarea>
                                    </div>

                                    <div class="group">
                                        <label class="block text-sm font-semibold text-slate-700 mb-2">Enlace a
                                            Evidencia (Drive)</label>
                                        <input v-model="evidencia_url" v-bind="evidenciaUrlProps" type="url"
                                            :class="['block w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 transition-all', errors.evidencia_url ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 bg-white focus:border-blue-500 focus:ring-blue-100']"
                                            placeholder="https://drive.google.com/...">
                                        <p v-if="errors.evidencia_url" class="mt-1 text-xs text-red-600 font-medium">{{
                                            errors.evidencia_url }}</p>
                                    </div>
                                </div>
                            </div>

                            <!-- Footer Actions -->
                            <div class="px-6 py-4 bg-slate-100 border-t border-slate-200 flex justify-end gap-3">
                                <button type="button" @click="$emit('close')"
                                    class="px-6 py-2.5 border-2 border-slate-300 rounded-xl text-slate-700 font-semibold hover:bg-slate-50 transition-colors">
                                    Cancelar
                                </button>
                                <button type="submit" :disabled="isSubmitting"
                                    class="px-8 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all transform disabled:opacity-70 disabled:cursor-not-allowed flex items-center">
                                    <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                        </path>
                                    </svg>
                                    {{ isSubmitting ? 'Registrando...' : 'Registrar' }}
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
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import * as yup from 'yup';
import { ref } from 'vue';
import api from '../api';
import Swal from 'sweetalert2';

const emit = defineEmits(['close', 'saved']);
const isSubmitting = ref(false);

const getShift = () => {
    const now = new Date();
    const hour = now.getHours();
    if (hour >= 6 && hour < 14) return 'Mañana';
    else if (hour >= 14 && hour < 22) return 'Tarde';
    else return 'Noche';
};

const schema = toTypedSchema(
    yup.object({
        turno: yup.string().required('El turno es obligatorio'),
        tipo: yup.string().required('El tipo de ocurrencia es obligatorio'),
        descripcion: yup.string().required('La descripción es obligatoria').min(10, 'Mínimo 10 caracteres'),
        acciones: yup.string().nullable(),
        evidencia_url: yup.string().url('Debe ser una URL válida').nullable(),
    })
);

const { errors, defineField, handleSubmit } = useForm({
    validationSchema: schema,
    initialValues: {
        turno: getShift(),
        tipo: 'Incidente',
        descripcion: '',
        acciones: '',
        evidencia_url: '',
    },
});

const [turno, turnoProps] = defineField('turno');
const [tipo, tipoProps] = defineField('tipo');
const [descripcion, descripcionProps] = defineField('descripcion');
const [acciones, accionesProps] = defineField('acciones');
const [evidencia_url, evidenciaUrlProps] = defineField('evidencia_url');

const submitForm = handleSubmit(async (values) => {
    if (isSubmitting.value) return;
    isSubmitting.value = true;
    try {
        const user = JSON.parse(localStorage.getItem('user'));

        // Construir nombre completo con título si existe
        const tituloUsuario = user?.titulo || '';
        const nombreUsuario = user?.nombre || 'Desconocido';
        const dniUsuario = user?.dni || 'unknown';
        const nombreCompleto = tituloUsuario ? `${tituloUsuario} ${nombreUsuario}` : nombreUsuario;

        await api.post('/occurrence/register', {
            ...values,
            // Datos del responsable que registra la ocurrencia
            responsable_dni: dniUsuario,
            responsable_nombre: nombreCompleto,
            responsable_rol_id: user?.rol_id || ''
        });

        await Swal.fire({
            icon: 'success',
            title: '¡Registrado!',
            text: 'Ocurrencia registrada exitosamente.',
            timer: 2000,
            showConfirmButton: false
        });

        emit('saved');
        emit('close');
    } catch (error) {
        console.error(error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un problema al registrar la ocurrencia.',
        });
    } finally {
        isSubmitting.value = false;
    }
});
</script>
