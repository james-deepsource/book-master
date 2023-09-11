<template>
  <div class="p-4">
    <page-title title="Add member"
      description="For effortless member additions, provide the necessary information, and we'll handle the rest." />

    <form @submit.prevent="addMember" class="p-4 space-y-4 bg-white rounded-md shadow-md">
      <div class="flex flex-col space-y-2">
        <label for="name" class="text-sm font-medium">Member Name:</label>
        <input id="name" v-model="name" type="text" required placeholder="Jane Doe" class="p-2 border rounded-md">
      </div>

      <button :disabled="isLoading" type="submit"
        class="px-4 py-2 font-medium text-white bg-blue-500 rounded-md hover:bg-blue-600"
        :class="{ 'cursor-not-allowed': isLoading }">
        <span>
          Add <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
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

const name = ref('');
const isLoading = ref(false);
const toast = useToast()

const addMember = async () => {
  try {
    isLoading.value = true;
    const response = await axios.post('/add-member', { name: name.value })

    // Clear form input
    name.value = '';

    // Show success toast
    toast.success(response.data.message)
  } catch (err) {
    toast.error(err.response.data.error)
  } finally {
    isLoading.value = false;
  }
};
</script>
