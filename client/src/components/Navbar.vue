<template>
    <nav class="bg-gray-800">
        <div class="px-2 sm:px-6 lg:px-8">
            <div class="relative flex items-center justify-between h-16">
                <div class="absolute inset-y-0 left-0 flex items-center md:hidden">
                    <button type="button"
                        class="relative inline-flex items-center justify-center p-2 text-gray-400 rounded-md hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                        aria-controls="mobile-menu" aria-expanded="false">
                        <span class="absolute -inset-0.5"></span>
                        <span class="sr-only">Open main menu</span>
                        <svg class="block w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                            aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                        </svg>
                        <svg class="hidden w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                            aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <span class="hidden font-mono text-lg text-white md:inline">Book Master</span>

                <ul class="items-center hidden h-full overflow-x-scroll hide-scrollbar md:flex gap-x-2 lg:gap-x-4">
                    <li v-for="item in navItems" :key="item.title">
                        <router-link :to="item.route"
                            class="px-3 py-2 text-sm font-medium text-gray-300 truncate rounded-md hover:bg-gray-700 hover:text-white"
                            :class="{ 'text-white bg-gray-700': $route.path === item.route }">{{ item.title }}</router-link>
                    </li>
                </ul>
            </div>
        </div>

        <!-- Mobile menu -->
        <div class="md:hidden" id="mobile-menu">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <router-link v-for="item in navItems" :key="item.title" :to="item.route"
                    class="block px-3 py-2 text-base font-medium text-white bg-gray-900 rounded-md"
                    :class="{ 'text-white bg-gray-700': $route.path === item.route }">
                    {{ item.title }}</router-link>
            </div>
        </div>
    </nav>
</template>

<script setup>
const navItems = [
    {
        title: 'Home',
        route: '/'
    },
    {
        title: 'Books',
        route: '/books'
    },
    {
        title: 'Add Book',
        route: '/add-book'
    },
    {
        title: 'Members',
        route: '/members'
    },
    {
        title: 'Add Member',
        route: '/add-member'
    },
    {
        title: 'Import Books',
        route: '/import-books'
    },
    {
        title: 'Issue Book',
        route: '/issue-book'
    },
    {
        title: 'Return Book',
        route: '/return-book'
    }
]
</script>
  

<style>
.hide-scrollbar {
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.hide-scrollbar::-webkit-scrollbar {
    display: none;
}
</style>