<template>
    <div class="p-4">
        <page-title title="Return book"
            description="Choose between member ID or name, book ID or name, and we'll handle the rest of your book return." />

        <form @submit.prevent="returnBook" class="p-4 space-y-4 bg-white rounded-md shadow-md">
            <div class="flex flex-col space-y-2">
                <label for="memberInput" class="text-sm font-medium">Member:</label>
                <select id="memberSelect" v-model="memberOption" class="p-2 border rounded-md">
                    <option value="id">ID</option>
                    <option value="name">Name</option>
                </select>
                <input id="memberInput" v-model="memberInput" :placeholder="memberOptionIsId ? '123' : 'Jane Doe'"
                    :type="memberOptionIsId ? 'number' : 'text'" required class="p-2 border rounded-md">
            </div>

            <div class="flex flex-col space-y-2">
                <label for="bookInput" class="text-sm font-medium">Book:</label>
                <select id="bookSelect" v-model="bookOption" class="p-2 border rounded-md">
                    <option value="id">ID</option>
                    <option value="name">Name</option>
                </select>
                <input id="bookInput" v-model="bookInput" :placeholder="bookOptionIsId ? '123' : 'Seven Nights'"
                    :type="bookOptionIsId ? 'number' : 'text'" required class="p-2 border rounded-md">
            </div>

            <div class="flex flex-col space-y-2">
                <label for="returnDate" class="text-sm font-medium">Return Date:</label>
                <input id="returnDate" v-model="returnDate" :min="today" required type="date" class="p-2 border rounded-md">
            </div>

            <button :disabled="isLoading" type="submit"
                class="px-4 py-2 font-medium text-white bg-red-500 rounded-md hover:bg-red-600"
                :class="{ 'cursor-not-allowed': isLoading }">
                <span>
                    Return <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
                </span>
            </button>
        </form>
    </div>
</template>
  
<script setup>
import { computed, ref } from 'vue';
import { useToast } from 'vue-toast-notification';

import axios from '@/api';
import PageTitle from './PageTitle.vue';

const bookInput = ref('');
const bookOption = ref('id');
const isLoading = ref(false);
const memberInput = ref('');
const memberOption = ref('id');
const returnDate = ref('');
const toast = useToast();

const [today] = new Date().toISOString().split('T');

const bookOptionIsId = computed(() => {
    return bookOption.value === 'id'
})

const memberOptionIsId = computed(() => {
    return memberOption.value === 'id'
})

const returnBook = async () => {
    try {
        isLoading.value = true

        const response = await axios
            .post('/return-book', {
                member: memberInput.value,
                book: bookInput.value,
                return_date: returnDate.value,
            })

        const { info, message } = response.data
        info && toast.info(info)

        // Show success toast
        toast.success(message);

        // Clear form fields
        memberInput.value = '';
        bookInput.value = '';
        returnDate.value = today;
    } catch (err) {
        toast.error(err.response.data.error)
    } finally {
        isLoading.value = false
    }
};
</script>
  