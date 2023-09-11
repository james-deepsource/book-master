<template>
  <div class="p-4 ">
    <page-title title="Books"
      description="View and manage books with their ID, title, authors and editing capabilities at your disposal." />

    <input v-model="searchQuery" type="text" id="searchQuery" class="w-full p-2 border rounded-md"
      placeholder="Search by title or author">

    <table v-if="filteredBooks.length" class="w-full bg-white border border-collapse border-gray-300">
      <thead>
        <tr>
          <th class="px-4 py-2 border border-gray-300">ID</th>
          <th class="px-4 py-2 border border-gray-300">Title</th>
          <th class="px-4 py-2 border border-gray-300">Authors</th>
          <th class="px-4 py-2 border border-gray-300">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="book in filteredBooks" :key="book.id">
          <td class="px-4 py-2 border border-gray-300">{{ book.id }}</td>
          <td class="px-4 py-2 border border-gray-300">{{ book.title }}</td>
          <td class="px-4 py-2 border border-gray-300">{{ book.authors }}</td>
          <td class="px-4 py-2 border border-gray-300">
            <button @click="editBook(book)"
              class="px-2 py-1 text-sm text-white bg-blue-500 rounded-md hover:bg-blue-600">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="flex items-center justify-center h-40 bg-white rounded-lg">
      <p class="text-lg text-gray-500">{{
        searchQuery ?
        `Oops, no books match your search criteria. Please check the book's title or author and try again.`
        : 'Start by importing books to begin your library. No books have been found yet.'
      }}</p>
    </div>

    <!-- Modal for editing book details -->
    <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="p-6 space-y-2 bg-white rounded-md shadow-md w-96">
        <h2 class="text-lg font-semibold">Edit Book</h2>

        <div class="space-y-4">
          <div>
            <label for="editTitle" class="block text-sm font-medium">Title:</label>
            <input v-model="editedBook.title" type="text" id="editTitle" class="w-full p-2 border rounded-md">
          </div>

          <div>
            <label for="editAuthors" class="block text-sm font-medium">Authors:</label>
            <input v-model="editedBook.authors" type="text" id="editAuthors" class="w-full p-2 border rounded-md">
          </div>

          <div class="flex justify-end">
            <button @click="updateBook"
              class="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600">Update</button>
            <button @click="closeEditModal"
              class="px-4 py-2 ml-2 text-gray-700 bg-gray-300 rounded-md hover:bg-gray-400">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useToast } from 'vue-toast-notification';

import axios from '@/api';
import PageTitle from './PageTitle.vue';

const books = ref([]);
const editedBook = ref({ id: null, title: '', authors: '' });
const searchQuery = ref('');
const showEditModal = ref(false);
const toast = useToast()

onMounted(async () => {
  try {
    const response = await axios.get('/books')
    books.value = response.data.books;
  } catch (err) {
    toast.error('Something went wrong while fetching the list of books.')
  }
})

const filteredBooks = computed(() => {
  return books.value.filter((book) => {
    const searchQueryIgnoringCase = searchQuery.value.toLocaleLowerCase()

    const matchInAuthors = book.authors.split('/').some((author) => author.toLowerCase().includes(searchQueryIgnoringCase))
    const matchInTitle = book.title.toLowerCase().includes(searchQueryIgnoringCase)

    return matchInAuthors || matchInTitle;
  });
});

const closeEditModal = () => {
  showEditModal.value = false;
  editedBook.value.id = null;
  editedBook.value.title = '';
  editedBook.value.authors = '';
}

const editBook = (book) => {
  editedBook.value.id = book.id;
  editedBook.value.title = book.title;
  editedBook.value.authors = book.authors;
  showEditModal.value = true;
}

const updateBook = async () => {
  if (editedBook.value.id === null) {
    return;
  }

  try {
    const response = await axios.put(`/update-book/${editedBook.value.id}`, editedBook.value)
    if (response.data.message === 'Book updated successfully') {
      const bookToUpdate = books.value.find((book) => book.id === editedBook.value.id);
      if (bookToUpdate) {
        bookToUpdate.title = editedBook.value.title;
        bookToUpdate.authors = editedBook.value.authors;
      }

      // Show success toast
      toast.success(response.data.message)

      // Close the modal
      closeEditModal();
    }

  } catch (err) {
    toast.error(err.response.data.error)
  }
}
</script>
