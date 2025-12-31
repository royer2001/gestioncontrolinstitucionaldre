<template>
  <div class="flex min-h-screen w-full bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
    <!-- Left Side Image -->
    <div class="w-1/2 hidden lg:flex relative overflow-hidden">
      <img class="absolute inset-0 w-full h-full object-cover" src="/login-bg.png" alt="DRE Huánuco Building">
      <div class="absolute inset-0 bg-gradient-to-br from-blue-900/60 via-indigo-900/50 to-purple-900/40"></div>

      <!-- Decorative Elements -->
      <div class="absolute top-10 right-10 w-32 h-32 bg-white/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 left-20 w-40 h-40 bg-blue-400/20 rounded-full blur-3xl"></div>

      <div class="absolute inset-0 flex flex-col justify-end p-12">
        <div class="max-w-lg">
          <div
            class="inline-flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-md rounded-full mb-6 border border-white/30">
            <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span class="text-white text-sm font-semibold">Sistema Integral Activo</span>
          </div>
          <h2 class="text-4xl font-bold text-white mb-4 leading-tight">Sistema de Gestión y Control Institucional</h2>
          <p class="text-xl text-blue-100 leading-relaxed font-light">SGCI-DREH | Administración Integral</p>
          <div class="mt-8 flex items-center gap-4">
            <div class="flex items-center gap-2 text-white/80">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <span class="text-sm font-medium">Seguro</span>
            </div>
            <div class="flex items-center gap-2 text-white/80">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span class="text-sm font-medium">Eficiente</span>
            </div>
            <div class="flex items-center gap-2 text-white/80">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span class="text-sm font-medium">Centralizado</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side Form -->
    <div class="w-full lg:w-1/2 flex flex-col items-center justify-center p-8 bg-white/50 backdrop-blur-sm">
      <div class="w-full max-w-md">
        <!-- Logo/Header Card -->
        <div class="text-center mb-10">
          <div
            class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-700 to-indigo-700 rounded-3xl shadow-2xl mb-6 ring-4 ring-blue-50 transform hover:scale-105 transition-transform duration-300">
            <img src="../assets/logo.png" alt="Logo" class="w-12 h-12 object-contain filter brightness-0 invert" />
          </div>
          <h2
            class="text-3xl font-extrabold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent mb-2">
            Bienvenido de nuevo
          </h2>
          <p class="text-slate-500 text-sm font-medium">SGCI-DREH | Sistema de Gestión y Control Institucional</p>
        </div>

        <!-- Error Alert -->
        <div v-if="loginError"
          class="mb-6 bg-red-50 border-2 border-red-200 rounded-xl p-4 animate-shake transition-all duration-300 ease-in-out">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd" />
              </svg>
            </div>
            <p class="text-sm font-semibold text-red-800">{{ loginError }}</p>
          </div>
        </div>

        <!-- Login Form Card -->
        <div class="bg-white rounded-2xl shadow-xl border-2 border-slate-200 p-8">
          <form class="space-y-8" @submit.prevent="handleLogin">
            <!-- DNI Field -->
            <div class="group relative">
              <label for="dni" class="block text-sm font-semibold text-slate-700 mb-2">
                DNI <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                  </svg>
                </div>
                <input v-model="dni" v-bind="dniProps" type="text" id="dni" maxlength="8" :class="[
                  'block w-full pl-10 pr-4 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                  errors.dni
                    ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100'
                    : 'border-slate-200 bg-white hover:border-blue-300 focus:border-blue-500 focus:ring-blue-100'
                ]" placeholder="DNI (8 dígitos)">
              </div>
              <p v-if="errors.dni" class="absolute left-0 top-full mt-1 text-sm text-red-600 flex items-center gap-1">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd" />
                </svg>
                {{ errors.dni }}
              </p>
            </div>

            <!-- Password Field -->
            <div class="group relative">
              <label for="password" class="block text-sm font-semibold text-slate-700 mb-2">
                Contraseña <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input v-model="password" v-bind="passwordProps" :type="showPassword ? 'text' : 'password'" id="password" :class="[
                  'block w-full pl-10 pr-12 py-3 border-2 rounded-xl transition-all duration-200 ease-in-out focus:outline-none focus:ring-4',
                  errors.password
                    ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-100'
                    : 'border-slate-200 bg-white hover:border-blue-300 focus:border-blue-500 focus:ring-blue-100'
                ]" placeholder="••••••••">
                <!-- Toggle Password Visibility Button -->
                <button 
                  type="button" 
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-blue-600 transition-colors duration-200"
                  :title="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                >
                  <!-- Eye Icon (show password) -->
                  <svg v-if="!showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <!-- Eye Off Icon (hide password) -->
                  <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
              <p v-if="errors.password"
                class="absolute left-0 top-full mt-1 text-sm text-red-600 flex items-center gap-1">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd" />
                </svg>
                {{ errors.password }}
              </p>
            </div>

            <!-- Submit Button -->
            <button type="submit" :disabled="isLoading"
              class="w-full inline-flex items-center justify-center px-8 py-3 border border-transparent rounded-xl text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-300 shadow-lg hover:shadow-xl transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed">
              <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              <svg v-else class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              {{ isLoading ? 'Ingresando...' : 'Ingresar al Sistema' }}
            </button>
          </form>
        </div>

        <!-- Footer -->
        <div class="mt-6 text-center">
          <p class="text-sm text-slate-500">
            © 2025 DRE Huánuco. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import * as yup from 'yup';
import api from '../api';

const router = useRouter();
const loginError = ref('');

const schema = toTypedSchema(
  yup.object({
    dni: yup.string().required('El DNI es obligatorio').matches(/^\d{8}$/, 'El DNI debe tener exactamente 8 dígitos numéricos'),
    password: yup.string().required('La contraseña es obligatoria'),
  })
);

const { errors, defineField, handleSubmit } = useForm({
  validationSchema: schema,
});

const [dni, dniProps] = defineField('dni');
const [password, passwordProps] = defineField('password');

const isLoading = ref(false);
const showPassword = ref(false);

const handleLogin = handleSubmit(async (values) => {
  if (isLoading.value) return;
  isLoading.value = true;
  loginError.value = '';
  try {
    const response = await api.post('/auth/login', {
      dni: values.dni,
      password: values.password,
    });

    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      router.push('/');
    }
  } catch (err) {
    loginError.value = err.response?.data?.message || 'Error al iniciar sesión';
  } finally {
    isLoading.value = false;
  }
});
</script>
