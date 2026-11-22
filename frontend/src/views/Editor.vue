<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import api from "@/api";

const title = ref("Editor Dashboard");
const auth = useAuthStore();

interface Note {
  created_at: String;
  modified_at: String;
  id: Number;
  title: String;
}

const getAllNotes = async () => {
  try {
    const userID = auth.user?.id;
    const data: Note[] = await api.get(
      `/backend/api/user/${userID}/get_all_notes`,
    );
    console.log(data);
  } catch (e) {
    console.log(e);
  }
};

getAllNotes();
</script>

<template>
  <Sidebar :title="title" />
</template>
