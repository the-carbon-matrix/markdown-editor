<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import { ref } from "vue";

const title = ref("Admin Dashboard");
</script>

<template>
  <Sidebar :title="title" />
</template>
