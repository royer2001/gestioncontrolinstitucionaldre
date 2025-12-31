<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header Card -->
      <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 mb-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Nueva Ocurrencia
            </h1>
            <p class="mt-2 text-slate-600">Complete los detalles del incidente para su registro</p>
          </div>
          <div class="bg-gradient-to-br from-blue-500 to-indigo-600 text-white px-5 py-3 rounded-xl shadow-md">
            <div class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-sm font-medium capitalize">{{ currentTime }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Form Card -->
      <div class="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
        <form @submit.prevent="submitForm" class="divide-y divide-slate-100">

          <!-- Sección 1: Información General -->
          <div class="p-8">
            <div class="flex items-center gap-3 mb-6">
              <div class="bg-blue-100 rounded-lg p-2">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <h2 class="text-xl font-bold text-slate-800">Información General</h2>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="group">
                <label for="turno" class="block text-sm font-semibold text-slate-700 mb-2">
                  Turno Actual
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <select v-model="turno" v-bind="turnoProps" id="turno" disabled
                    class="block w-full pl-10 pr-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-xl text-slate-500 cursor-not-allowed focus:outline-none transition-all duration-200 ease-in-out">
                    <option value="Mañana">🌅 Mañana</option>
                    <option value="Tarde">☀️ Tarde</option>
                    <option value="Noche">🌙 Noche</option>
                  </select>
                </div>
              </div>

              <div class="group">
                <label for="tipo" class="block text-sm font-semibold text-slate-700 mb-2">
                  Tipo de Ocurrencia <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" fill="none"
                      viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                  </div>
                  <select v-model="tipo" v-bind="tipoProps" id="tipo" :class="[
                    'block w-full pl-10 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                    errors.tipo
                      ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100'
                      : 'border-slate-200 bg-white hover:border-blue-300 focus:border-blue-500 focus:ring-blue-100'
                  ]">
                    <option value="Incidente">⚠️ Incidente</option>
                    <option value="Aviso">📢 Aviso</option>
                    <option value="Emergencia">🚨 Emergencia</option>
                    <option value="Rutina">✅ Rutina</option>
                    <option value="Robo">🔒 Robo</option>
                    <option value="Otros">📋 Otros</option>
                  </select>
                </div>
                <p v-if="errors.tipo" class="mt-2 text-sm text-red-600 flex items-center gap-1">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clip-rule="evenodd" />
                  </svg>
                  {{ errors.tipo }}
                </p>
              </div>
            </div>
          </div>

          <!-- Sección 2: Detalles del Evento -->
          <div class="p-8 bg-slate-50/50">
            <div class="flex items-center gap-3 mb-6">
              <div class="bg-indigo-100 rounded-lg p-2">
                <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                  </path>
                </svg>
              </div>
              <h2 class="text-xl font-bold text-slate-800">Detalles del Evento</h2>
            </div>

            <div class="space-y-6">
              <div class="group">
                <label for="descripcion" class="block text-sm font-semibold text-slate-700 mb-2">
                  Descripción Detallada <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                  <textarea v-model="descripcion" v-bind="descripcionProps" id="descripcion" rows="5" :class="[
                    'block w-full px-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out resize-none focus:outline-none focus:ring-4',
                    errors.descripcion
                      ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100'
                      : 'border-slate-200 bg-white hover:border-indigo-300 focus:border-indigo-500 focus:ring-indigo-100'
                  ]"
                    placeholder="Describa detalladamente qué sucedió, dónde ocurrió, quiénes estuvieron involucrados, y cualquier otro detalle relevante del incidente..."></textarea>
                  <div class="absolute bottom-3 right-3 text-xs text-slate-400">
                    {{ descripcion?.length || 0 }} caracteres
                  </div>
                </div>
                <p v-if="errors.descripcion" class="mt-2 text-sm text-red-600 flex items-center gap-1">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clip-rule="evenodd" />
                  </svg>
                  {{ errors.descripcion }}
                </p>
              </div>

              <div class="group">
                <label for="acciones" class="block text-sm font-semibold text-slate-700 mb-2">
                  Acciones Tomadas
                </label>
                <textarea v-model="acciones" v-bind="accionesProps" id="acciones" rows="4"
                  class="block w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white hover:border-indigo-300 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 focus:outline-none transition-all duration-200 ease-in-out resize-none"
                  placeholder="Describa las medidas inmediatas que se tomaron, quién las ejecutó, y los resultados obtenidos..."></textarea>
              </div>
            </div>
          </div>

          <!-- Sección 3: Evidencia -->
          <div class="p-8">
            <div class="flex items-center gap-3 mb-6">
              <div class="bg-green-100 rounded-lg p-2">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z">
                  </path>
                </svg>
              </div>
              <h2 class="text-xl font-bold text-slate-800">Evidencia Digital</h2>
            </div>

            <div class="group">
              <label for="evidencia_url" class="block text-sm font-semibold text-slate-700 mb-2">
                Enlace a Google Drive
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-slate-400 group-focus-within:text-green-500 transition-colors" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <input v-model="evidencia_url" v-bind="evidenciaUrlProps" type="url" id="evidencia_url" :class="[
                  'block w-full pl-12 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                  errors.evidencia_url
                    ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100'
                    : 'border-slate-200 bg-white hover:border-green-300 focus:border-green-500 focus:ring-green-100'
                ]" placeholder="https://drive.google.com/...">
              </div>
              <p v-if="errors.evidencia_url" class="mt-2 text-sm text-red-600 flex items-center gap-1">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd" />
                </svg>
                {{ errors.evidencia_url }}
              </p>
              <div class="mt-3 flex items-start gap-2 p-4 bg-blue-50 border border-blue-200 rounded-xl">
                <svg class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-sm text-blue-800">
                  <span class="font-semibold">Opcional:</span> Comparta el enlace a la carpeta o archivo de evidencia
                  (fotos, videos, documentos) alojado en Google Drive.
                </p>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="p-8 bg-slate-50 flex flex-col sm:flex-row items-stretch sm:items-center justify-end gap-4">
            <router-link to="/"
              class="inline-flex items-center justify-center px-6 py-3 border-2 border-slate-300 rounded-xl text-sm font-semibold text-slate-700 bg-white hover:bg-slate-50 hover:border-slate-400 focus:outline-none focus:ring-4 focus:ring-slate-200 transition-all duration-200 ease-in-out">
              <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Cancelar
            </router-link>
            <button type="submit" :disabled="isSubmitting"
              class="inline-flex items-center justify-center px-8 py-3 border border-transparent rounded-xl text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-300 shadow-lg hover:shadow-xl transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed">
              <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              <svg v-else class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ isSubmitting ? 'Registrando...' : 'Registrar Ocurrencia' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Footer Info -->
      <div class="mt-6 text-center text-sm text-slate-500">
        <p>Los campos marcados con <span class="text-red-500 font-semibold">*</span> son obligatorios</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import * as yup from 'yup';
import { ref, onMounted, onUnmounted } from 'vue';
import api from '../api';
import Swal from 'sweetalert2';

const router = useRouter();
const currentTime = ref('');
let timer = null;

const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleString('es-PE', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

onMounted(() => {
  updateTime();
  timer = setInterval(updateTime, 1000);
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});

const getShift = () => {
  const now = new Date();
  const hour = now.getHours();

  if (hour >= 6 && hour < 14) {
    return 'Mañana';
  } else if (hour >= 14 && hour < 22) {
    return 'Tarde';
  } else {
    return 'Noche';
  }
};

const schema = toTypedSchema(
  yup.object({
    turno: yup.string().required('El turno es obligatorio'),
    tipo: yup.string().required('El tipo de ocurrencia es obligatorio'),
    descripcion: yup.string().required('La descripción es obligatoria').min(10, 'La descripción debe tener al menos 10 caracteres'),
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
  validateOnBlur: true,
  validateOnChange: true,
  validateOnInput: false,
  validateOnModelUpdate: true,
});

const [turno, turnoProps] = defineField('turno', { validateOnBlur: true, validateOnChange: true, validateOnInput: false });
const [tipo, tipoProps] = defineField('tipo', { validateOnBlur: true, validateOnChange: true, validateOnInput: false });
const [descripcion, descripcionProps] = defineField('descripcion', { validateOnBlur: true, validateOnChange: true, validateOnInput: false });
const [acciones, accionesProps] = defineField('acciones', { validateOnBlur: true, validateOnChange: true, validateOnInput: false });
const [evidencia_url, evidenciaUrlProps] = defineField('evidencia_url', { validateOnBlur: true, validateOnChange: true, validateOnInput: false });

const isSubmitting = ref(false);

const submitForm = handleSubmit(async (values) => {
  if (isSubmitting.value) return;
  isSubmitting.value = true;
  try {
    const user = JSON.parse(localStorage.getItem('user'));
    await api.post('/occurrence/register', {
      ...values,
      username: user ? user.usuario : 'unknown'
    });

    await Swal.fire({
      icon: 'success',
      title: '¡Ocurrencia Registrada!',
      text: 'La ocurrencia ha sido registrada exitosamente.',
      timer: 2000,
      showConfirmButton: false
    });

    router.push('/');
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