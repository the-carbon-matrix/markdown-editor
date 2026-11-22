<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import { SquareArrowUpRightExit, Trash, FilePlus } from "@lucide/vue";

import { onBeforeMount, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import api from "@/api";

const title = ref("Editor Dashboard");
const auth = useAuthStore();

interface Note {
  created_at: string;
  modified_at: string;
  id: number;
  title: string;
}

const notes = ref([] as Note[]);

const getAllNotes = async () => {
  try {
    const userID = auth.user?.id;
    notes.value = await api.get(`/backend/api/user/${userID}/get_all_notes`);
  } catch (e) {
    alert("Failed to fetch notes, please see console for more information.");
    console.log(e);
  }
};

const createNote = async () => {
  const title = prompt("Enter the note title", "My New Note");
  try {
    await api.post("/backend/api/user/create_note", { title, content: "" });
    await getAllNotes();
    alert("Note successfully created!");
  } catch (e) {
    alert("Failed to create note, please see console for more information.");
    console.log(e);
  }
};

const deleteNote = async (id: number) => {
  if (!confirm("Are you sure you want to delete this note?")) return;

  try {
    await api.delete(`/backend/api/user/delete_note/${id}`);
    await getAllNotes();
    alert("Note successfully deleted!");
  } catch (e) {
    alert("Failed to delete note, please see console for more information.");
    console.log(e);
  }
};

onBeforeMount(async () => {
  await getAllNotes();
});
</script>

<template>
  <Sidebar :title="title">
    <template v-slot:entries>
      <div
        class="entry"
        v-for="note in notes"
        :key="Date.parse(note.modified_at)"
      >
        <p>{{ note.title }}</p>
        <button class="open"><SquareArrowUpRightExit /></button>
        <button class="delete" @click="() => deleteNote(note.id)">
          <Trash />
        </button>
      </div>
    </template>

    <template v-slot:button>
      <button @click="createNote"><FilePlus /></button>
    </template>
  </Sidebar>
</template>

<style scoped src="../assets/editor.css"></style>
