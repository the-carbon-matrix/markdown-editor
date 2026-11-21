<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const doLogout = async () => {
  try {
    await auth.logout();
    router.push("/login");
  } catch (e) {
    console.log(e);
  }
};
</script>

<template>
  <h1>Admin Page</h1>
  <button @click="doLogout">Logout</button>
</template>
