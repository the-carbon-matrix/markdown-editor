<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const email = ref("");
const username = ref("");
const password = ref("");

async function doLogin() {
  try {
    await auth.login(email.value, username.value, password.value);
    router.push("/");
  } catch (e) {
    console.error(e);
  }
}
</script>

<template>
  <h1>Login Page</h1>

  <form @submit.prevent="doLogin">
    <input v-model="email" type="email" placeholder="email" />
    <input v-model="username" type="text" placeholder="username" />
    <input v-model="password" type="password" placeholder="password" />
    <button type="submit">Login</button>
  </form>
</template>

<style scoped></style>
