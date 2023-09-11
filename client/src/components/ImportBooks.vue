<template>
  <div class="p-4">
    <page-title title="Import books" description="Easily import your book collection with a single click." />

    <form @submit.prevent="importBooks" class="p-4 space-y-4 bg-white rounded-md shadow-md">
      <div class="flex flex-col space-y-2">
        <label for="numBooks" class="text-sm font-medium">Number of Books to Import:</label>
        <input v-model="numBooks" id="numBooks" required type="number" placeholder="20" class="p-2 border rounded-md">
      </div>

      <div class="flex flex-col space-y-2">
        <label for="title" class="text-sm font-medium">Title Filter:</label>
        <input v-model="title" id="title" type="text" placeholder="Harry Potter" class="p-2 border rounded-md">
      </div>

      <button :disabled="isLoading" type="submit"
        class="px-4 py-2 font-medium text-white bg-indigo-500 rounded-md hover:bg-indigo-600"
        :class="{ 'cursor-not-allowed': isLoading }">
        <span>
          Import <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
        </span>
      </button>
    </form>
  </div>
</template>
  
<script setup>
import { ref } from 'vue';
import { useToast } from 'vue-toast-notification';

import axios from '@/api'
import PageTitle from './PageTitle.vue';

const numBooks = ref(20);
const title = ref('')
const isLoading = ref(false); // Add loading state variable
const toast = useToast()

const importBooks = async () => {
  try {
    isLoading.value = true; // Set loading to true during request
    const response = await axios.post('/import-books', { num_books: numBooks.value })

    // Clear the form
    numBooks.value = 20
    title.value = ''

    // Show success toast
    toast.success(response.data.message)
  } catch (err) {
    toast.error(err.response.data.error)
  } finally {
    isLoading.value = false; // Reset loading to false after request completes
  }
};
</script>
