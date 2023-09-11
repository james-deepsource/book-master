<template>
    <div class="p-4">
        <page-title title="Add book"
            description="For hassle-free book additions, simply input book details and we'll take care of the rest." />

        <form @submit.prevent="addBook" class="p-4 space-y-4 bg-white rounded-md shadow-md">
            <div class="flex flex-col space-y-2">
                <label for="title" class="text-sm font-medium">Title:</label>
                <input v-model="title" type="text" id="title" placeholder="Seven Nights" class="p-2 border rounded-md">
            </div>

            <div class="flex flex-col space-y-2">
                <label for="authors" class="text-sm font-medium">Authors:</label>
                <input v-model="authors" type="text" id="authors" placeholder="Jorge Luis Borges/Eliot Weinberger"
                    class="p-2 border rounded-md">
            </div>

            <button :disabled="isLoading" type="submit"
                class="px-4 py-2 font-medium text-white bg-green-500 rounded-md hover:bg-green-600"
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

const authors = ref('');
const title = ref('');
const isLoading = ref(false);
const toast = useToast()

const addBook = async () => {
    try {
        isLoading.value = true;
        const response = await axios.post('/add-book', { title: title.value, authors: authors.value })

        // Clear the form
        authors.value = ''
        title.value = ''

        // Show success toast
        toast.success(response.data.message)
    } catch (err) {
        toast.error(err.response.data.error)
    } finally {
        isLoading.value = false;
    }
};
</script>
