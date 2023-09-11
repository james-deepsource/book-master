<template>
  <div>
    <Navbar />
    <router-view class="hidden min-h-screen space-y-4 bg-gray-100 rounded-md md:block" />

    <div class="flex items-center justify-center h-40 rounded-lg md:hidden">
      <p class="text-lg text-gray-500">Not optimized for smaller screens.</p>
    </div>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';
</script>
