<template>
  <div class="p-4">
    <h1 class="text-3xl font-bold ">Welcome to Book Master</h1>
    <p class="text-lg">This web application empowers librarians to efficiently manage the library's wealth of resources
      and
      membership. Explore the following capabilities:</p>

    <ul class="pl-6 list-disc">
      <li v-for="(feature, idx) in features" :key="idx" class="text-base">{{ feature }}</li>
    </ul>

    <p class="text-lg">Navigate the menu above to harness these robust features and elevate your
      Book Master experience!</p>
  </div>
</template>
  
<script setup>
const features = [
  `Effortlessly enrich the library's collection by adding new books.`,
  'Browse and access the full catalog of available books in the library.',
  'Simplify membership management by seamlessly adding new members.',
  'Quickly locate books by title and author with our intuitive search.',
  'Connect with external sources and effortlessly import books via the Frappe API.',
  'Streamline the process of issuing books to library members.',
  'Handle book returns from members, complete with rental fee calculations.',
  'Efficiently oversee library members and their interactions with the library.'
]
</script>