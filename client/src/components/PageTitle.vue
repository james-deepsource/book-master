<template>
    <div class="space-y-4 text-center rounded-md">
        <h1 class="text-3xl font-bold text-slate-700">{{ title }}</h1>

        <p class="text-gray-700 ">
            {{ description }}
        </p>
    </div>
</template>

<script setup>
const { title, description } = defineProps({
    title: String,
    description: String,
});
</script>