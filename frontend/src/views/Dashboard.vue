<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-8 px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
        Dashboard General
      </h1>
      <p class="mt-2 text-slate-600">Resumen de actividad del sistema - {{ currentDate }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="bg-white rounded-2xl shadow-lg border border-slate-200 px-6 py-24 text-center">
      <div class="flex flex-col items-center justify-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none"
          viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
          </path>
        </svg>
        <p class="text-lg font-medium text-slate-600">Cargando estadísticas...</p>
      </div>
    </div>

    <template v-else>
      <!-- Quick Access Section -->
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-4">
          <div class="bg-gradient-to-br from-blue-500 to-indigo-500 rounded-lg p-2">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-slate-800">Accesos Rápidos</h2>
        </div>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
          <!-- Acceso Libro de Ocurrencias -->
          <router-link to="/occurrence/list"
            class="group bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-blue-100 hover:shadow-xl hover:border-blue-300 transition-all duration-300 ease-in-out transform hover:scale-105 cursor-pointer">
            <div class="p-6">
              <div class="flex items-center gap-4">
                <div
                  class="flex-shrink-0 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 shadow-md group-hover:shadow-lg transition-shadow">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-bold text-slate-900 group-hover:text-blue-600 transition-colors">Libro de
                    Ocurrencias</h3>
                  <p class="text-sm text-slate-500 mt-1">Ver y registrar ocurrencias</p>
                </div>
                <svg class="w-6 h-6 text-slate-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-all"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </router-link>

          <!-- Acceso Control de Personal -->
          <router-link to="/entry-exit/list"
            class="group bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-emerald-100 hover:shadow-xl hover:border-emerald-300 transition-all duration-300 ease-in-out transform hover:scale-105 cursor-pointer">
            <div class="p-6">
              <div class="flex items-center gap-4">
                <div
                  class="flex-shrink-0 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl p-4 shadow-md group-hover:shadow-lg transition-shadow">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-bold text-slate-900 group-hover:text-emerald-600 transition-colors">Control de
                    Personal</h3>
                  <p class="text-sm text-slate-500 mt-1">Entradas y salidas del personal</p>
                </div>
                <svg
                  class="w-6 h-6 text-slate-400 group-hover:text-emerald-500 group-hover:translate-x-1 transition-all"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </router-link>

          <!-- Acceso Visitas Externas -->
          <router-link to="/visitor/list"
            class="group bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-purple-100 hover:shadow-xl hover:border-purple-300 transition-all duration-300 ease-in-out transform hover:scale-105 cursor-pointer">
            <div class="p-6">
              <div class="flex items-center gap-4">
                <div
                  class="flex-shrink-0 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-4 shadow-md group-hover:shadow-lg transition-shadow">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-bold text-slate-900 group-hover:text-purple-600 transition-colors">Visitas
                    Externas</h3>
                  <p class="text-sm text-slate-500 mt-1">Registro de visitantes</p>
                </div>
                <svg class="w-6 h-6 text-slate-400 group-hover:text-purple-500 group-hover:translate-x-1 transition-all"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </router-link>

          <!-- Acceso Control Vehicular -->
          <router-link to="/vehicle/control"
            class="group bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-cyan-100 hover:shadow-xl hover:border-cyan-300 transition-all duration-300 ease-in-out transform hover:scale-105 cursor-pointer">
            <div class="p-6">
              <div class="flex items-center gap-4">
                <div
                  class="flex-shrink-0 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-xl p-4 shadow-md group-hover:shadow-lg transition-shadow">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 012-2v0a2 2 0 012 2m0 0a2 2 0 012-2h2a2 2 0 012 2m0 0a2 2 0 012-2h2a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-bold text-slate-900 group-hover:text-cyan-600 transition-colors">Control
                    Vehicular</h3>
                  <p class="text-sm text-slate-500 mt-1">Gestión de comisiones</p>
                </div>
                <svg class="w-6 h-6 text-slate-400 group-hover:text-cyan-500 group-hover:translate-x-1 transition-all"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </router-link>
        </div>
      </div>


      <!-- Section: Ocurrencias -->
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-4">
          <div class="bg-blue-100 rounded-lg p-2">
            <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-slate-800">Libro de Ocurrencias</h2>
        </div>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <!-- Total Ocurrencias -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-blue-100 hover:shadow-xl hover:border-blue-200 transition-all duration-300 ease-in-out transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Total</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.occurrences.total }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Incidentes -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-yellow-100 hover:shadow-xl hover:border-yellow-200 transition-all duration-300 transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Incidentes</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.occurrences.incidentes }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Emergencias -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-red-100 hover:shadow-xl hover:border-red-200 transition-all duration-300 transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Emergencias</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.occurrences.emergencias }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Rutinas -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-green-100 hover:shadow-xl hover:border-green-200 transition-all duration-300 transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Rutinas</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.occurrences.rutinas }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section: Control de Personal -->
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-4">
          <div class="bg-emerald-100 rounded-lg p-2">
            <svg class="w-6 h-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-slate-800">Control de Personal</h2>
        </div>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
          <!-- Total Papeletas -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-emerald-100 hover:shadow-xl hover:border-emerald-200 transition-all duration-300 ease-in-out transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Total Papeletas</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.personnel.total }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Pendientes Retorno -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-orange-100 hover:shadow-xl hover:border-orange-200 transition-all duration-300 transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Pendiente Retorno</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.personnel.pending_return }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Hoy -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-teal-100 hover:shadow-xl hover:border-teal-200 transition-all duration-300 transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Hoy</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.personnel.today }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section: Visitantes Externos -->
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-4">
          <div class="bg-purple-100 rounded-lg p-2">
            <svg class="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-slate-800">Visitas Externas</h2>
        </div>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
          <!-- Total Visitas -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-purple-100 hover:shadow-xl hover:border-purple-200 transition-all duration-300 ease-in-out transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Total Visitas</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.visitors.total }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Activas -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-pink-100 hover:shadow-xl hover:border-pink-200 transition-all duration-300 transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">En Instalaciones</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.visitors.active }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Hoy -->
          <div
            class="bg-white overflow-hidden shadow-lg rounded-2xl border-2 border-indigo-100 hover:shadow-xl hover:border-indigo-200 transition-all duration-300 transform hover:scale-105">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl p-4 shadow-md">
                  <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Hoy</dt>
                    <dd>
                      <div class="text-3xl font-bold text-slate-900">{{ stats.visitors.today }}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api';

const isLoading = ref(false);
const stats = ref({
  occurrences: {
    total: 0,
    incidentes: 0,
    emergencias: 0,
    rutinas: 0
  },
  personnel: {
    total: 0,
    pending_return: 0,
    today: 0
  },
  visitors: {
    total: 0,
    active: 0,
    today: 0
  }
});

const currentDate = computed(() => {
  const now = new Date();
  return now.toLocaleDateString('es-PE', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
});

const fetchSummary = async () => {
  isLoading.value = true;
  try {
    const response = await api.get('/occurrence/summary');
    stats.value = response.data;
  } catch (error) {
    console.error('Error fetching summary:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchSummary();
});
</script>
