<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import api from "@/api";

const auth = useAuthStore();

const email = ref("");
const username = ref("");
const password = ref("");
const output = ref("");

async function doLogin() {
  try {
    await auth.login(email.value, username.value, password.value);
    output.value = `Logged in as: ${auth.user?.username}`;
  } catch (e) {
    output.value = "Check the console!";
    console.error(e);
  }
}

async function callProtected() {
  try {
    const data = await api.get("/api/user/profile");
    output.value = JSON.stringify(data, null, 2);
  } catch (e) {
    output.value = "Check the console!";
    console.error(e);
  }
}
</script>

<template>
  <h1>Temporary Authentication Test Page</h1>

  <form @submit.prevent="doLogin">
    <input v-model="email" type="email" placeholder="email" />
    <input v-model="username" type="text" placeholder="username" />
    <input v-model="password" type="password" placeholder="password" />
    <button type="submit">Login</button>
  </form>

  <button @click="callProtected">Call protected route</button>
  <button @click="auth.refresh()">Force refresh</button>
  <button @click="auth.logout()">Logout</button>

  <p>Authenticated: {{ auth.isAuthenticated }}</p>
  <pre>{{ output }}</pre>
</template>

<style scoped></style>
