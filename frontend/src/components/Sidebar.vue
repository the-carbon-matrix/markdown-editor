<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { AtSign, SquareArrowRightExit } from "@lucide/vue";

const auth = useAuthStore();
const router = useRouter();

const props = defineProps({
  title: String,
});

const username = ref(auth.user?.username);

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
  <div class="sidebar">
    <h1>{{ title || "Sidebar" }}</h1>
    <hr />
    <div class="user-info">
      <p><AtSign style="margin-right: 10px" />{{ username }}</p>
      <button @click="doLogout"><SquareArrowRightExit /></button>
    </div>
  </div>
</template>

<style scoped src="../assets/sidebar.css"></style>
