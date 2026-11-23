<script setup lang="ts">
import { Mail, UserRound, KeyRound } from "@lucide/vue";

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
    alert(
      "Error occured during registration! Please check if username and email are unique",
    );
    console.log(e);
  }
};
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Register Page</h1>
      <form @submit.prevent="doRegister">
        <div class="input-grp">
          <label for="email"><Mail color="#333333" /></label>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="Email"
            required
          />
        </div>

        <div class="input-grp">
          <label for="username"><UserRound color="#333333" /></label>
          <input
            v-model="username"
            type="text"
            id="username"
            placeholder="Username"
            required
          />
        </div>

        <div class="input-grp">
          <label for="password"><KeyRound color="#333333" /></label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Password"
            required
          />
        </div>

        <div class="input-grp">
          <label for="password_confirm"> <KeyRound color="#333333" /> </label>
          <input
            v-model="password_confirm"
            type="password"
            id="password_confirm"
            placeholder="Confirm Password"
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
      <p>Or <a href="/login">Login</a> if you already have an account</p>
    </div>
  </div>
</template>

<style scoped src="../assets/form.css"></style>
