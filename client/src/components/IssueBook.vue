<template>
  <div class="p-4">
    <page-title title="Issue a book"
      description="Choose whether you prefer to provide the member's ID or name, as well as the book's ID or name. Leave the rest to us." />

    <form @submit.prevent="issueBook" class="p-4 space-y-4 bg-white rounded-md shadow-md">
      <div class="flex flex-col space-y-2">
        <label for="memberSelect" class="text-sm font-medium">Parameter:</label>
        <select id="memberSelect" v-model="memberOption" class="p-2 border rounded-md">
          <option value="id">ID</option>
          <option value="name">Name</option>
        </select>
      </div>
      <div class="flex flex-col space-y-2">
        <label for="memberInput" class="text-sm font-medium">
          {{ memberOptionIsId ? 'Member ID:' : 'Member Name:' }}
        </label>
        <input id="memberInput" v-model="memberModel" :type="memberOptionIsId ? 'number' : 'text'"
          :placeholder="memberOptionIsId ? '123' : 'Jane Doe'" required class="p-2 border rounded-md" />
      </div>

      <div class="flex flex-col space-y-2">
        <label for="bookSelect" class="text-sm font-medium">Parameter:</label>
        <select id="bookSelect" v-model="bookOption" class="p-2 border rounded-md">
          <option value="id">ID</option>
          <option value="name">Name</option>
        </select>
      </div>
      <div class="flex flex-col space-y-2">
        <label for="bookInput" class="text-sm font-medium">
          {{ bookOptionIsId ? 'Book ID:' : 'Book Name:' }}
        </label>
        <input id="bookInput" v-model="bookModel" :type="bookOptionIsId ? 'number' : 'text'"
          :placeholder="bookOptionIsId ? '123' : 'Seven Nights'" required class="p-2 border rounded-md" />
      </div>

      <button :disabled="isLoading" type="submit"
        class="px-4 py-2 font-medium text-white bg-blue-500 rounded-md hover:bg-blue-600"
        :class="{ 'cursor-not-allowed': isLoading }">
        <span>
          Issue <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
        </span>
      </button>
    </form>

    <ToastContainer />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useToast } from 'vue-toast-notification';

import axios from '@/api';
import PageTitle from './PageTitle.vue';

const bookOption = ref('id');
const bookModel = ref(null);
const isLoading = ref(false);
const memberModel = ref(null);
const memberOption = ref('id');
const toast = useToast();

const bookOptionIsId = computed(() => {
  return bookOption.value === 'id'
})

const memberOptionIsId = computed(() => {
  return memberOption.value === 'id'
})

const issueBook = async () => {
  try {
    isLoading.value = true;

    const response = await axios
      .post('/issue-book', {
        member: memberModel.value,
        book: bookModel.value,
      })

    // Clear the form
    memberModel.value = null;
    bookModel.value = null;

    // Show success toast
    toast.success(response.data.message);
  } catch (err) {
    toast.error(err.response.data.error)
  } finally {
    isLoading.value = false;
  }
};
</script>
