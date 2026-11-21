<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const email = ref("");
const username = ref("");
const password = ref("");
const password_confirm = ref("");

const doRegister = async () => {
  if (password.value !== password_confirm.value) {
    alert("Passwords do not match!");
    password.value = "";
    password_confirm.value = "";
    return;
  }

  try {
    await auth.register(email.value, username.value, password.value);
    alert(
      "Registration complete! Please wait for admin to verify your account.",
    );
    router.push("/login");
  } catch (e) {
    alert("Error occured!");
    console.log(e);
  }
};
</script>

<template>
  <h1>Register Page</h1>
  <form @submit.prevent="doRegister">
    <input v-model="email" type="email" placeholder="email" required />
    <input v-model="username" type="text" placeholder="username" required />
    <input v-model="password" type="password" placeholder="password" required />
    <input
      v-model="password_confirm"
      type="password"
      placeholder="password_confirm"
      required
    />
    <button type="submit">Register</button>
  </form>
</template>
