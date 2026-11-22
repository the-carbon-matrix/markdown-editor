<script setup lang="ts">
import { Mail, UserRound, KeyRound } from "@lucide/vue";

import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const email = ref("");
const username = ref("");
const password = ref("");

async function doLogin() {
  if (!email.value && !username.value) {
    alert("Please enter either email or username.");
    return;
  }

  try {
    await auth.login(email.value, username.value, password.value);
    router.push("/");
  } catch (e) {
    console.error(e);
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Login Page</h1>

      <form @submit.prevent="doLogin">
        <div class="input-grp">
          <label for="email"><Mail color="#333333" /></label>
          <input v-model="email" id="email" type="email" placeholder="Email" />
        </div>

        <p class="subtitle">OR</p>

        <div class="input-grp">
          <label for="username"><UserRound color="#333333" /></label>
          <input
            v-model="username"
            id="username"
            type="text"
            placeholder="Username"
          />
        </div>

        <hr />

        <div class="input-grp">
          <label for="username"><KeyRound color="#333333" /></label>
          <input
            v-model="password"
            id="password"
            type="password"
            placeholder="Password"
            required
          />
        </div>

        <button type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<style scoped src="../assets/form.css"></style>
