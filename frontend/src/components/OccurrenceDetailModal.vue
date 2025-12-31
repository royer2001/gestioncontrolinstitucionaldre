<template>
    <transition name="modal">
        <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
            aria-modal="true">
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
                        class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex justify-between items-center">
                        <h3 class="text-xl font-bold text-white flex items-center gap-2">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Detalle de Ocurrencia
                        </h3>
                        <button @click="$emit('close')" class="text-blue-100 hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Content -->
                    <div class="p-6 sm:p-8 bg-slate-50">
                        <div v-if="occurrence" class="space-y-6">

                            <!-- Status and Type Badge -->
                            <div class="flex flex-wrap items-center justify-between gap-4">
                                <span class="px-4 py-2 inline-flex text-sm font-bold rounded-xl shadow-sm" :class="{
                                    'bg-gradient-to-r from-red-500 to-red-600 text-white': occurrence.tipo === 'Emergencia' || occurrence.tipo === 'Robo',
                                    'bg-gradient-to-r from-yellow-500 to-yellow-600 text-white': occurrence.tipo === 'Incidente',
                                    'bg-gradient-to-r from-green-500 to-green-600 text-white': occurrence.tipo === 'Rutina',
                                    'bg-gradient-to-r from-blue-500 to-blue-600 text-white': occurrence.tipo === 'Aviso',
                                    'bg-gradient-to-r from-gray-500 to-gray-600 text-white': occurrence.tipo === 'Otros'
                                }">
                                    {{ occurrence.tipo }}
                                </span>
                                <span
                                    class="px-4 py-2 inline-flex text-sm font-bold rounded-xl bg-white border border-slate-200 text-slate-700 shadow-sm">
                                    Estado: {{ occurrence.estado }}
                                </span>
                            </div>

                            <!-- Date and Time -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Fecha</p>
                                    <p class="text-lg font-semibold text-slate-800">{{ occurrence.fecha }}</p>
                                </div>
                                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Hora</p>
                                    <p class="text-lg font-semibold text-slate-800">{{ occurrence.hora }}</p>
                                </div>
                            </div>

                            <!-- Description -->
                            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Descripción
                                </p>
                                <p class="text-slate-700 whitespace-pre-wrap leading-relaxed">{{ occurrence.descripcion
                                }}</p>
                            </div>

                            <!-- Actions Taken -->
                            <div v-if="occurrence.acciones"
                                class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Acciones
                                    Tomadas</p>
                                <p class="text-slate-700 whitespace-pre-wrap leading-relaxed">{{ occurrence.acciones }}
                                </p>
                            </div>

                            <!-- Responsible -->
                            <div
                                class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
                                <div
                                    class="h-12 w-12 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-lg font-bold text-white shadow-md">
                                    {{ String(occurrence.vigilante || '?').charAt(0) }}
                                </div>
                                <div>
                                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-0.5">
                                        Responsable</p>
                                    <p class="text-lg font-semibold text-slate-800">{{ occurrence.vigilante }}</p>
                                </div>
                            </div>

                        </div>
                        <div v-else class="text-center py-8 text-slate-500">
                            No se ha seleccionado ninguna ocurrencia.
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="px-6 py-4 bg-slate-100 border-t border-slate-200 flex justify-end">
                        <button @click="$emit('close')"
                            class="px-6 py-2.5 border-2 border-slate-300 rounded-xl text-sm font-bold text-slate-700 bg-white hover:bg-slate-50 hover:border-slate-400 focus:outline-none focus:ring-4 focus:ring-slate-200 transition-all duration-200 ease-in-out">
                            Cerrar
                        </button>
                    </div>

                </div>
            </div>
        </div>
    </transition>
</template>

<script setup>
defineProps({
    show: {
        type: Boolean,
        default: false
    },
    occurrence: {
        type: Object,
        default: null
    }
});

defineEmits(['close']);
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
