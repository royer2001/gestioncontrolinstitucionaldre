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
                    class="inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">

                    <!-- Header -->
                    <div
                        class="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4 flex justify-between items-center">
                        <h3 class="text-xl font-bold text-white flex items-center gap-2">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                            </svg>
                            Registrar Visita Externa
                        </h3>
                        <button @click="$emit('close')" class="text-purple-100 hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Form Content -->
                    <div class="p-6 sm:p-8 bg-slate-50">
                        <Form :validation-schema="schema" @submit="submitForm" class="space-y-6" v-slot="{ errors }">

                            <!-- Visitor Details -->
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div class="group">
                                    <label class="block text-sm font-semibold text-slate-700 mb-2">DNI Visitante <span
                                            class="text-red-500">*</span></label>
                                    <Field name="dni" type="text" maxlength="8"
                                        :class="errors.dni ? 'border-red-500 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 focus:border-purple-500 focus:ring-purple-100'"
                                        class="block w-full px-4 py-3 border-2 rounded-xl transition-all outline-none"
                                        placeholder="Ingrese DNI" />
                                    <ErrorMessage name="dni" class="text-red-500 text-xs mt-1 font-medium" />
                                </div>

                                <div class="group">
                                    <label class="block text-sm font-semibold text-slate-700 mb-2">Nombre Completo <span
                                            class="text-red-500">*</span></label>
                                    <Field name="visitorName" type="text"
                                        :class="errors.visitorName ? 'border-red-500 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 focus:border-purple-500 focus:ring-purple-100'"
                                        class="block w-full px-4 py-3 border-2 rounded-xl transition-all outline-none uppercase"
                                        placeholder="Nombre del visitante" />
                                    <ErrorMessage name="visitorName" class="text-red-500 text-xs mt-1 font-medium" />
                                </div>
                            </div>

                            <!-- Area Selection -->
                            <div class="group">
                                <label class="block text-sm font-semibold text-slate-700 mb-2">Área a Visitar <span
                                        class="text-red-500">*</span></label>
                                <Field name="selectedArea" as="select"
                                    :class="errors.selectedArea ? 'border-red-500 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 focus:border-purple-500 focus:ring-purple-100'"
                                    class="block w-full px-4 py-3 border-2 rounded-xl transition-all outline-none appearance-none bg-white">
                                    <option value="" disabled>Seleccione un área</option>
                                    <option v-for="area in areas" :key="area" :value="area">{{ area }}</option>
                                </Field>
                                <ErrorMessage name="selectedArea" class="text-red-500 text-xs mt-1 font-medium" />
                            </div>

                            <!-- Reason -->
                            <div class="group">
                                <label class="block text-sm font-semibold text-slate-700 mb-2">Motivo de Visita <span
                                        class="text-red-500">*</span></label>
                                <Field name="reason" as="textarea" rows="3"
                                    :class="errors.reason ? 'border-red-500 focus:border-red-500 focus:ring-red-100' : 'border-slate-200 focus:border-purple-500 focus:ring-purple-100'"
                                    class="block w-full px-4 py-3 border-2 rounded-xl transition-all outline-none resize-none"
                                    placeholder="Describa el motivo..." />
                                <ErrorMessage name="reason" class="text-red-500 text-xs mt-1 font-medium" />
                            </div>

                            <!-- Actions -->
                            <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-200">
                                <button type="button" @click="$emit('close')"
                                    class="px-6 py-3 border-2 border-slate-300 rounded-xl text-slate-700 font-semibold hover:bg-slate-50 transition-colors">
                                    Cancelar
                                </button>
                                <button type="submit" :disabled="isSubmitting"
                                    class="px-8 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all transform disabled:opacity-70 disabled:cursor-not-allowed flex items-center">
                                    <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                        </path>
                                    </svg>
                                    {{ isSubmitting ? 'Registrando...' : 'Registrar Visita' }}
                                </button>
                            </div>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import api from '../api';
import Swal from 'sweetalert2';

const emit = defineEmits(['close', 'saved']);
const isSubmitting = ref(false);
const areas = ref([]);

const schema = yup.object().shape({
    dni: yup.string()
        .required('El DNI es obligatorio')
        .matches(/^[0-9]+$/, 'Solo se permiten números')
        .length(8, 'El DNI debe tener exactamente 8 dígitos'),
    visitorName: yup.string()
        .required('El nombre es obligatorio')
        .min(3, 'El nombre debe tener al menos 3 caracteres'),
    selectedArea: yup.string()
        .required('Debe seleccionar un área'),
    reason: yup.string()
        .required('El motivo es obligatorio')
        .min(5, 'El motivo debe ser más detallado')
});

const fetchAreas = async () => {
    try {
        const response = await api.get('/visitor/areas');
        areas.value = response.data;
    } catch (error) {
        console.error("Error fetching areas:", error);
        Swal.fire('Error', 'No se pudieron cargar las áreas', 'error');
    }
};

const submitForm = async (values) => {
    if (isSubmitting.value) return;
    isSubmitting.value = true;

    try {
        const user = JSON.parse(localStorage.getItem('user'));
        const response = await api.post('/visitor/register', {
            visitor_name: values.visitorName.toUpperCase(),
            dni: values.dni,
            area: values.selectedArea,
            reason: values.reason,
            username: user ? user.usuario : 'unknown'
        });

        const entryId = response.data.entry_id;

        const result = await Swal.fire({
            icon: 'success',
            title: '¡Visita Registrada!',
            text: `Se ha registrado la visita a ${values.selectedArea}.`,
            showCancelButton: true,
            confirmButtonColor: '#7C3AED',
            cancelButtonColor: '#6B7280',
            confirmButtonText: 'Imprimir Ticket',
            cancelButtonText: 'Cerrar'
        });

        if (result.isConfirmed && entryId) {
            window.open(`${api.defaults.baseURL}/visitor/ticket/${entryId}`, '_blank');
        }

        emit('saved');
        emit('close');
    } catch (error) {
        console.error(error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un problema al registrar la visita.',
        });
    } finally {
        isSubmitting.value = false;
    }
};

onMounted(() => {
    fetchAreas();
});
</script>
