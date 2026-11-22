<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import { SquareArrowUpRightExit, Trash, FilePlus, Save } from "@lucide/vue";

import { onBeforeMount, ref, computed } from "vue";
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

const sortedNotes = computed(() =>
  [...notes.value].sort(
    (a, b) => Date.parse(b.modified_at) - Date.parse(a.modified_at),
  ),
);

const currentNote = ref(sortedNotes.value[0]); // open the most recent note by default
const original_content = ref("");
const new_content = ref("");

const original_title = ref(currentNote.value?.title);
const new_title = ref(original_title.value);

const editMode = ref(true); // true = edit mode, false = preview mode

const getAllNotes = async () => {
  try {
    const userID = auth.user?.id;
    notes.value = await api.get(`/backend/api/user/${userID}/get_all_notes`);
    currentNote.value = sortedNotes.value[0];
    original_title.value = currentNote.value?.title;
    new_title.value = original_title.value;
  } catch (e) {
    alert("Failed to fetch notes, please see console for more information.");
    console.log(e);
  }
};

const createNote = async () => {
  const title = prompt("Enter the note title", "My New Note");
  if (!title) return;

  try {
    await api.post("/backend/api/user/create_note", { title, content: "" });
    await getAllNotes();
    alert("Note successfully created!");
  } catch (e) {
    alert("Failed to create note, please see console for more information.");
    console.log(e);
  }
};

const readNote = async (id: number): Promise<string> => {
  try {
    const data: Note & { content: string } = await api.get(
      `/backend/api/user/get_note/${id}`,
    );
    return data.content;
  } catch (e) {
    alert(
      `Failed to read note with id: ${id}. Please check console for more information.`,
    );
    console.log(e);
    return "";
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

  if (currentNote.value?.id) {
    original_content.value = await readNote(currentNote.value?.id);
    new_content.value = original_content.value;
  }
});
</script>

<template>
  <div class="dashboard">
    <Sidebar :title="title">
      <template v-slot:entries>
        <div
          class="entry"
          v-for="note in sortedNotes"
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
    <div class="editor">
      <div class="options">
        <input type="text" id="title" v-model="new_title" />
        <button
          @click="
            () => {
              editMode = !editMode;
            }
          "
        >
          Switch to {{ editMode ? "Preview" : "Edit" }} Mode
        </button>
        <button class="save"><Save /></button>
      </div>
    </div>
  </div>
</template>

<style scoped src="../assets/editor.css"></style>
