<template>
  <div class="p-4">
    <page-title title="Members"
      description="View and manage members with their ID, name, outstanding debt, borrowed books, and editing capabilities at your disposal." />

    <input v-if="filteredMembers.length || searchQuery" v-model="searchQuery" type="text" id="searchQuery"
      class="w-full p-2 border rounded-md" placeholder="Search by name">

    <table v-if="filteredMembers.length" class="w-full bg-white border border-collapse border-gray-300 shadow-md">
      <thead>
        <tr>
          <th class="px-4 py-2 border border-gray-300">ID</th>
          <th class="px-4 py-2 border border-gray-300">Name</th>
          <th class="px-4 py-2 border border-gray-300">Outstanding Debt</th>
          <th class="px-4 py-2 border border-gray-300">Borrowed Books</th>
          <th class="px-4 py-2 border border-gray-300">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="member in filteredMembers" :key="member.id">
          <td class="px-4 py-2 border border-gray-300">{{ member.id }}</td>
          <td class="px-4 py-2 border border-gray-300">{{ member.name }}</td>
          <td class="px-4 py-2 border border-gray-300">{{ member.outstanding_debt }}</td>
          <td class="px-4 py-2 border border-gray-300">
            <ul class="px-2 list-disc">
              <li v-for="book in member.borrowed_books" :key="book.id">
                {{ book.title }}
              </li>
            </ul>
          </td>
          <td class="px-4 py-2 border border-gray-300">
            <button @click="editMember(member)"
              class="px-2 py-1 text-sm text-white bg-blue-500 rounded-md hover:bg-blue-600">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="flex items-center justify-center h-40 bg-white rounded-lg">
      <p class="text-lg text-gray-500">
        {{
          searchQuery ?
          `Oops, no results match your search criteria. Please check the member's name and try again.` :
          'Begin by adding a new member to your list. Currently, no members have been found.'
        }}</p>
    </div>

    <!-- Modal for editing member details -->
    <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="p-6 space-y-2 bg-white rounded-md shadow-md w-96">
        <h2 class="text-lg font-semibold">Edit Member</h2>

        <div class="space-y-4">
          <div>
            <label for="editName" class="block text-sm font-medium">Name:</label>
            <input v-model="editedMember.name" type="text" id="editName" class="w-full p-2 border rounded-md">
          </div>

          <div>
            <label for="editDebt" class="block text-sm font-medium">Outstanding Debt:</label>
            <input v-model="editedMember.outstanding_debt" type="number" id="editDebt"
              class="w-full p-2 border rounded-md">
          </div>

          <div class="flex justify-end">
            <button @click="updateMember"
              class="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600">Update</button>
            <button @click="closeEditModal"
              class="px-4 py-2 ml-2 text-gray-700 bg-gray-300 rounded-md hover:bg-gray-400">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <ToastContainer />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useToast } from 'vue-toast-notification';

import axios from '@/api';
import PageTitle from './PageTitle.vue';

const editedMember = ref({ id: null, name: '', outstanding_debt: 0 });
const members = ref([]);
const searchQuery = ref('');
const showEditModal = ref(false);
const toast = useToast()

onMounted(async () => {
  try {
    const response = await axios.get('/members')
    members.value = response.data.members;
  } catch (err) {
    toast.error('Something went wrong while fetching the list of members.')
  }
})

const filteredMembers = computed(() => {
  return members.value.filter((member) => {
    const searchQueryIgnoringCase = searchQuery.value.toLocaleLowerCase()

    return member.name.toLowerCase().includes(searchQueryIgnoringCase)
  });
});

const closeEditModal = () => {
  showEditModal.value = false;
  editedMember.value.id = null;
  editedMember.value.name = '';
  editedMember.value.outstanding_debt = 0;
}

const editMember = (member) => {
  editedMember.value.id = member.id;
  editedMember.value.name = member.name;
  editedMember.value.outstanding_debt = member.outstanding_debt;
  showEditModal.value = true;
}

const updateMember = async () => {
  if (editedMember.value.id === null) {
    return;
  }

  try {

    const response = await axios.put(`/update-member/${editedMember.value.id}`, editedMember.value)
    if (response.data.message === 'Member updated successfully') {
      const memberToUpdate = members.value.find((member) => member.id === editedMember.value.id);
      if (memberToUpdate) {
        memberToUpdate.name = editedMember.value.name;
        memberToUpdate.outstanding_debt = editedMember.value.outstanding_debt;
      }

      toast.success(response.data.message);

      closeEditModal();
    }
  } catch (err) {
    toast.error(err.response.data.error)
  }
}
</script>
