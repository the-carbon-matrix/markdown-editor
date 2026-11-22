<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import { SquareArrowUpRightExit, Trash, FilePlus, Save } from "@lucide/vue";

import { onBeforeMount, ref, computed } from "vue";
import MarkdownIt from "markdown-it";
import { useAuthStore } from "@/stores/auth";
import api from "@/api";

const title = ref("Editor Dashboard");
const auth = useAuthStore();
const md = new MarkdownIt();

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

const result = computed(() => md.render(new_content.value));

const original_title = ref(currentNote.value?.title);
const new_title = ref(original_title.value);

const isEdited = computed(
  () =>
    new_content.value != original_content.value ||
    new_title.value != original_title.value,
);

const editMode = ref(true); // true = edit mode, false = preview mode
const noteIsOpen = ref(false);

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

const readNote = async (
  id: number,
): Promise<(Note & { content: string }) | undefined> => {
  try {
    const data: Note & { content: string } = await api.get(
      `/backend/api/user/get_note/${id}`,
    );
    return data;
  } catch (e) {
    alert(
      `Failed to read note with id: ${id}. Please check console for more information.`,
    );
    console.log(e);
  }
};

const switchNote = async (id: number | undefined) => {
  if (isEdited.value) {
    if (confirm("Would you like to save before switching files?")) {
      saveNote();
    }
  }

  if (!id) {
    currentNote.value = undefined;
    original_content.value = "";
    new_content.value = "";
    original_title.value = "";
    new_title.value = "";

    noteIsOpen.value = false;
    return;
  }

  const data = await readNote(id);
  currentNote.value = data;
  original_content.value = data?.content || "";
  new_content.value = original_content.value;

  original_title.value = currentNote.value?.title;
  new_title.value = original_title.value;
  noteIsOpen.value = true;
};

const saveNote = async () => {
  try {
    await api.patch(`/backend/api/user/edit_note/${currentNote.value?.id}`, {
      title: new_title.value,
      content: new_content.value,
    });

    original_content.value = new_content.value;
    original_title.value = new_title.value;
    await getAllNotes();
    alert("Note successfully saved!");
  } catch (e) {
    alert("Failed to save note, please check console for more info.");
    console.log(e);
  }
};

const deleteNote = async (id: number) => {
  if (!confirm("Are you sure you want to delete this note?")) return;

  try {
    await api.delete(`/backend/api/user/delete_note/${id}`);
    await getAllNotes();
    if (id == currentNote.value?.id) {
      switchNote(sortedNotes.value[0]?.id);
    }
    alert("Note successfully deleted!");
  } catch (e) {
    alert("Failed to delete note, please see console for more information.");
    console.log(e);
  }
};

onBeforeMount(async () => {
  await getAllNotes();
  switchNote(sortedNotes.value[0]?.id);
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
          <button class="open" @click="() => switchNote(note.id)">
            <SquareArrowUpRightExit />
          </button>
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
        <input
          type="text"
          id="title"
          v-model="new_title"
          :disabled="!noteIsOpen"
        />
        <button
          @click="
            () => {
              editMode = !editMode;
            }
          "
        >
          Switch to {{ editMode ? "Preview" : "Edit" }} Mode
        </button>
        <button class="save" @click="saveNote" :disabled="!noteIsOpen">
          <Save />
        </button>
      </div>
      <textarea
        name="md-editor"
        id="editor"
        v-if="editMode"
        v-model="new_content"
        :disabled="!noteIsOpen"
      ></textarea>
      <div class="preview" v-else v-html="result"></div>
    </div>
  </div>
</template>

<style scoped src="../assets/editor.css"></style>
