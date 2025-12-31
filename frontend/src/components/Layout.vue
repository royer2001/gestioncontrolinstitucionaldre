<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex">
        <!-- Sidebar -->
        <aside
            :class="[isCollapsed ? 'w-20' : 'w-72', 'bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 text-white flex-shrink-0 hidden md:flex flex-col transition-all duration-300 ease-in-out shadow-2xl h-screen sticky top-0']">

            <!-- Toggle Button -->
            <button @click="toggleSidebar"
                class="absolute -right-3 top-24 bg-blue-600 text-white p-1 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none z-50 transform hover:scale-110 transition-all duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path v-if="!isCollapsed" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 19l-7-7 7-7" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
            </button>

            <!-- Logo Header -->
            <div class="h-24 flex items-center border-b border-slate-700/50 bg-slate-900/80 backdrop-blur-sm transition-all duration-300"
                :class="isCollapsed ? 'justify-center px-0' : 'justify-center px-4'">
                <div class="flex items-center font-bold text-xl tracking-wider transition-all duration-300"
                    :class="isCollapsed ? 'space-x-0' : 'space-x-3'">
                    <div class="bg-white p-1.5 rounded-xl shadow-lg ring-2 ring-blue-400/30">
                        <img src="../assets/logo.png" alt="DRE Huánuco" class="h-12 w-12 object-contain" />
                    </div>
                    <div class="flex flex-col transition-opacity duration-200" v-if="!isCollapsed">
                        <span
                            class="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent font-extrabold whitespace-nowrap">SGCI-DREH</span>
                        <span
                            class="text-[9px] text-slate-500 font-medium tracking-wide uppercase whitespace-nowrap leading-tight">Sistema
                            de Gestión<br />y Control Institucional</span>
                    </div>
                </div>
            </div>


            <!-- Navigation - Scrollable area -->
            <div
                class="flex-1 overflow-y-auto py-6 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
                <div class="px-4 mb-4 transition-opacity duration-200" v-if="!isCollapsed">
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest px-3">Menú Principal</p>
                </div>
                <nav class="padding-transition space-y-1.5" :class="isCollapsed ? 'px-2' : 'px-4'">
                    <router-link to="/"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path === '/' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/30 ring-1 ring-blue-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Dashboard' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path === '/' ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path === '/' ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed"
                            class="whitespace-nowrap transition-opacity duration-200">Dashboard</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/occurrence/list')" to="/occurrence/list"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path === '/occurrence/list' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/30 ring-1 ring-blue-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Libro de Ocurrencias' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path === '/occurrence/list' ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path === '/occurrence/list' ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Libro de
                            Ocurrencias</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/entry-exit/list')" to="/entry-exit/list"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path.startsWith('/entry-exit') ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg shadow-emerald-500/30 ring-1 ring-emerald-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Control de Personal' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path.startsWith('/entry-exit') ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path.startsWith('/entry-exit') ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Control de
                            Personal</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/visitor/list')" to="/visitor/list"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path.startsWith('/visitor') ? 'bg-gradient-to-r from-purple-600 to-fuchsia-600 text-white shadow-lg shadow-purple-500/30 ring-1 ring-purple-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Visitas Externas' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path.startsWith('/visitor') ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path.startsWith('/visitor') ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Visitas
                            Externas</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/vehicle/control')" to="/vehicle/control"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path.startsWith('/vehicle') ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-lg shadow-cyan-500/30 ring-1 ring-cyan-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Control Vehicular' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path.startsWith('/vehicle') ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path.startsWith('/vehicle') ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 012-2v0a2 2 0 012 2m0 0a2 2 0 012-2h2a2 2 0 012 2m0 0a2 2 0 012-2h2a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Control
                            Vehicular</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/citas/gestion')" to="/citas/gestion"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path.startsWith('/citas') ? 'bg-gradient-to-r from-pink-600 to-rose-600 text-white shadow-lg shadow-pink-500/30 ring-1 ring-pink-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Gestión de Citas' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path.startsWith('/citas') ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path.startsWith('/citas') ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Gestión de
                            Citas</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/license/management')" to="/license/management"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path.startsWith('/license') ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-500/30 ring-1 ring-purple-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Control de Licencias' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path.startsWith('/license') ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path.startsWith('/license') ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Control de
                            Licencias</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/hr/management')" to="/hr/management"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path.startsWith('/hr') ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg shadow-emerald-500/30 ring-1 ring-emerald-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Recursos Humanos' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path.startsWith('/hr') ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path.startsWith('/hr') ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Recursos
                            Humanos</span>
                    </router-link>

                    <router-link v-if="hasAccessTo('/turn/management')" to="/turn/management"
                        class="group flex items-center text-sm font-semibold rounded-xl transition-all duration-200 ease-in-out relative"
                        :class="[
                            $route.path.startsWith('/turn') ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-white shadow-lg shadow-orange-500/30 ring-1 ring-orange-400/50' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white',
                            isCollapsed ? 'justify-center py-3 px-0' : 'px-4 py-3.5'
                        ]" :title="isCollapsed ? 'Gestión de Turnos' : ''">
                        <div class="rounded-lg transition-colors duration-200 ease-in-out flex-shrink-0" :class="[
                            $route.path.startsWith('/turn') ? 'bg-white/20' : 'bg-slate-700/80 group-hover:bg-slate-600',
                            isCollapsed ? 'p-2' : 'mr-4 p-2'
                        ]">
                            <svg class="h-5 w-5"
                                :class="$route.path.startsWith('/turn') ? 'text-white' : 'text-slate-400 group-hover:text-white'"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                                <line x1="16" y1="2" x2="16" y2="6" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                                <line x1="8" y1="2" x2="8" y2="6" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                                <line x1="3" y1="10" x2="21" y2="10" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                            </svg>
                        </div>
                        <span v-if="!isCollapsed" class="whitespace-nowrap transition-opacity duration-200">Gestión de
                            Turnos</span>
                    </router-link>
                </nav>
            </div>

            <!-- User Profile - Fixed at bottom -->
            <div class="flex-shrink-0 border-t border-slate-700/50 p-4 bg-gradient-to-t from-slate-900 to-slate-800/80 backdrop-blur-sm transition-all duration-300"
                :class="isCollapsed ? 'items-center justify-center p-2' : 'p-4'">
                <div class="flex items-center gap-3 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 transition-colors duration-200"
                    :class="isCollapsed ? 'p-2 justify-center' : 'p-3'">
                    <div class="flex-shrink-0">
                        <div
                            class="h-11 w-11 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-sm font-bold text-white shadow-lg ring-2 ring-blue-400/30">
                            {{ user?.nombre?.charAt(0) || 'U' }}
                        </div>
                    </div>
                    <div class="flex-1 min-w-0 transition-opacity duration-200" v-if="!isCollapsed">
                        <p class="text-sm font-bold text-white truncate">{{ user?.nombre || 'Usuario' }}</p>
                        <p class="text-xs text-slate-400 flex items-center gap-1">
                            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                            {{ getRoleName }}
                        </p>
                    </div>
                    <button @click="logout"
                        class="flex-shrink-0 bg-slate-700/80 rounded-lg text-slate-400 hover:text-white hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-200 ease-in-out"
                        :class="isCollapsed ? 'hidden group-hover:block absolute left-full ml-2 p-2' : 'p-2.5'"
                        :title="isCollapsed ? 'Cerrar Sesión' : 'Cerrar Sesión'">
                        <span class="sr-only">Cerrar Sesión</span>
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                    </button>
                </div>
            </div>
        </aside>

        <!-- Mobile Header -->
        <div
            class="md:hidden fixed top-0 w-full bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white z-10 flex items-center justify-between px-4 h-16 shadow-lg">
            <div class="flex items-center space-x-2 font-bold text-lg">
                <div class="bg-gradient-to-br from-blue-500 to-indigo-600 p-1.5 rounded-lg">
                    <svg class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                </div>
                <span>DRE Huánuco</span>
            </div>
            <button @click="mobileMenuOpen = !mobileMenuOpen"
                class="text-slate-300 hover:text-white focus:outline-none p-2 rounded-lg hover:bg-slate-700 transition-colors duration-200 ease-in-out">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 6h16M4 12h16M4 18h16" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>

        <!-- Mobile Menu Overlay -->
        <div v-if="mobileMenuOpen"
            class="fixed inset-0 z-40 flex md:hidden transition-opacity duration-300 ease-in-out">
            <div class="fixed inset-0 bg-slate-900/80 backdrop-blur-sm transition-opacity duration-300 ease-in-out"
                @click="mobileMenuOpen = false"></div>
            <div
                class="relative flex-1 flex flex-col max-w-xs w-full bg-gradient-to-b from-slate-900 to-slate-800 shadow-2xl transform transition-transform duration-300 ease-in-out">
                <div class="pt-5 pb-4 px-4 overflow-y-auto h-full">
                    <nav class="space-y-2">
                        <router-link to="/" @click="mobileMenuOpen = false"
                            class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold transition-all duration-200 ease-in-out"
                            :class="$route.path === '/'
                                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg'
                                : 'text-slate-300 hover:bg-slate-700 hover:text-white'">
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                            </svg>
                            Dashboard
                        </router-link>
                        <router-link v-if="hasAccessTo('/occurrence/list')" to="/occurrence/list"
                            @click="mobileMenuOpen = false"
                            class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold transition-all duration-200 ease-in-out"
                            :class="$route.path === '/occurrence/list'
                                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg'
                                : 'text-slate-300 hover:bg-slate-700 hover:text-white'">
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                            Ocurrencias
                        </router-link>
                        <router-link v-if="hasAccessTo('/entry-exit/list')" to="/entry-exit/list"
                            @click="mobileMenuOpen = false"
                            class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold transition-all duration-200 ease-in-out"
                            :class="$route.path.startsWith('/entry-exit')
                                ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-lg'
                                : 'text-slate-300 hover:bg-slate-700 hover:text-white'">
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            Registro de Personal
                        </router-link>
                        <router-link v-if="hasAccessTo('/visitor/list')" to="/visitor/list"
                            @click="mobileMenuOpen = false"
                            class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold transition-all duration-200 ease-in-out"
                            :class="$route.path.startsWith('/visitor')
                                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg'
                                : 'text-slate-300 hover:bg-slate-700 hover:text-white'">
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            Visitas Externas
                        </router-link>
                        <router-link v-if="hasAccessTo('/vehicle/control')" to="/vehicle/control"
                            @click="mobileMenuOpen = false"
                            class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold transition-all duration-200 ease-in-out"
                            :class="$route.path.startsWith('/vehicle')
                                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-lg'
                                : 'text-slate-300 hover:bg-slate-700 hover:text-white'">
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 012-2v0a2 2 0 012 2m0 0a2 2 0 012-2h2a2 2 0 012 2m0 0a2 2 0 012-2h2a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                            Control Vehicular
                        </router-link>
                        <router-link v-if="hasAccessTo('/citas/gestion')" to="/citas/gestion"
                            @click="mobileMenuOpen = false"
                            class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold transition-all duration-200 ease-in-out"
                            :class="$route.path.startsWith('/citas')
                                ? 'bg-gradient-to-r from-pink-600 to-rose-600 text-white shadow-lg'
                                : 'text-slate-300 hover:bg-slate-700 hover:text-white'">
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            Gestión de Citas
                        </router-link>
                        <button @click="logout"
                            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold text-slate-300 hover:bg-red-600 hover:text-white transition-all duration-200 ease-in-out mt-4 border-t border-slate-700 pt-6">
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                            </svg>
                            Cerrar Sesión
                        </button>
                    </nav>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto pt-20 md:pt-0">
            <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                    <component :is="Component" />
                </transition>
            </router-view>
        </main>
    </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { ref, onMounted, watch, computed } from 'vue';

const router = useRouter();
const route = useRoute();
const user = ref(null);
const mobileMenuOpen = ref(false);
const isCollapsed = ref(false);

// Definición de permisos por rol_id
// Cada rol tiene acceso a ciertas rutas
const rolePermissions = {
    // Vigilante - Solo acceso a vigilancia
    'ROL007': ['/', '/occurrence/list', '/entry-exit/list', '/visitor/list', '/vehicle/control', '/turn/management'],
    // Coordinador de Vigilante - Vigilancia + reportes
    'ROL006': ['/', '/occurrence/list', '/entry-exit/list', '/visitor/list', '/vehicle/control', '/turn/management'],
    // Director - Acceso completo
    'ROL002': ['/', '/occurrence/list', '/entry-exit/list', '/visitor/list', '/vehicle/control', '/citas/gestion', '/license/management', '/hr/management', '/turn/management'],
    // Subdirector - Acceso completo
    'ROL003': ['/', '/occurrence/list', '/entry-exit/list', '/visitor/list', '/vehicle/control', '/citas/gestion', '/license/management', '/hr/management', '/turn/management'],
    // Jefe RRHH - Solo RRHH
    'ROL004': ['/hr/management'],
    // Jefe Bienestar - Solo Licencias
    'ROL005': ['/license/management'],
    // Secretario - Gestión de citas
    'ROL008': ['/', '/citas/gestion', '/visitor/list', '/turn/management'],
    // Jefe Patrimonio
    'ROL009': ['/'],
    // Jefe Abastecimiento
    'ROL010': ['/'],
    // Jefe OCI - Lectura de todo
    'ROL011': ['/', '/occurrence/list', '/entry-exit/list', '/visitor/list', '/vehicle/control', '/citas/gestion', '/license/management', '/hr/management', '/turn/management'],
    // Admin - Acceso completo
    'ROL001': ['/', '/occurrence/list', '/entry-exit/list', '/visitor/list', '/vehicle/control', '/citas/gestion', '/license/management', '/hr/management', '/turn/management'],
};

// Verificar si el usuario tiene acceso a una ruta
const hasAccessTo = (routePath) => {
    if (!user.value) return false;
    const userRoleId = user.value.rol_id || '';
    const allowedRoutes = rolePermissions[userRoleId] || [];
    // Verificar si la ruta exacta o ruta padre está permitida
    return allowedRoutes.some(allowed => {
        if (routePath === allowed) return true;
        if (routePath.startsWith(allowed + '/')) return true;
        return false;
    });
};

// Obtener el nombre del rol para mostrar
const getRoleName = computed(() => {
    if (!user.value) return 'Usuario';
    const roleNames = {
        'ROL001': 'Administrador',
        'ROL002': 'Director',
        'ROL003': 'Subdirector',
        'ROL004': 'Jefe de RRHH',
        'ROL005': 'Jefe de Bienestar',
        'ROL006': 'Coord. Vigilante',
        'ROL007': 'Vigilante',
        'ROL008': 'Secretario',
        'ROL009': 'Jefe Patrimonio',
        'ROL010': 'Jefe Abastecimiento',
        'ROL011': 'Jefe OCI',
    };
    return roleNames[user.value.rol_id] || 'Usuario';
});

const toggleSidebar = () => {
    isCollapsed.value = !isCollapsed.value;
};

// Computed para la key de la transición
const routeKey = computed(() => route.path);

onMounted(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
        user.value = JSON.parse(userData);
    }
});

// Cerrar menú móvil automáticamente al cambiar de ruta
watch(() => route.path, () => {
    mobileMenuOpen.value = false;
});


const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
};
</script>

<style>
/* Transición fade solo para el contenido principal */
.fade-enter-active {
    transition: opacity 0.25s ease-in-out;
}

.fade-leave-active {
    transition: opacity 0.15s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
    opacity: 1;
}
</style>
