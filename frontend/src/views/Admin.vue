<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import { ArrowRightCircle, Search, Trash, Eye } from "@lucide/vue";
import { computed, onBeforeMount, ref } from "vue";
import MarkdownIt from "markdown-it";
import api from "@/api";

const md = new MarkdownIt();
const result = ref("");

const title = ref("Admin Dashboard");
const search = ref("");

interface Editor {
  created_at: string;
  email: string;
  id: number;
  is_active: boolean;
  username: string;
}

interface Note {
  created_at: string;
  modified_at: string;
  id: number;
  user_id: number;
  title: string;
}

const editors = ref([] as Editor[]);
const filteredEditors = computed(() => {
  return search.value
    ? editors.value.filter((e) => {
        return (
          e.id.toString().includes(search.value) ||
          e.email.includes(search.value) ||
          e.username.includes(search.value)
        );
      })
    : editors.value;
});

const notes = ref([] as Note[]);
const filteredNotes = computed(() => {
  return search.value
    ? notes.value.filter((n) => {
        return (
          n.id.toString().includes(search.value) ||
          n.title.includes(search.value)
        );
      })
    : notes.value;
});

const getAllEditors = async () => {
  try {
    editors.value = await api.get("/backend/api/admin/get_all_users");
  } catch (e) {
    alert("Failed to get editors, please see console for more info.");
    console.log(e);
  }
};

const activateEditor = async (id: number) => {
  try {
    await api.patch(`/backend/api/admin/activate_user/${id}`);
    await getAllEditors();
    alert("User successfully activated!");
  } catch (e) {
    alert("Failed to activate user, please see console for more info.");
    console.log(e);
  }
};

const deactivateEditor = async (id: number, checkBox: HTMLInputElement) => {
  if (
    !confirm(
      "Are you sure you want to deactivate this user's account? This will NOT delete their notes.",
    )
  ) {
    checkBox.checked = true;
    return;
  }

  try {
    await api.patch(`/backend/api/admin/deactivate_user/${id}`);
    await getAllEditors();
    alert("User successfully deactivated!");
  } catch (e) {
    alert("Failed to activate user, please see console for more info.");
    console.log(e);
  }
};

const toggleEditor = async (id: number, event: Event) => {
  const checkBox = event.target as HTMLInputElement;
  const isChecked = checkBox.checked;

  if (isChecked) {
    await activateEditor(id);
  } else {
    await deactivateEditor(id, checkBox);
  }
};

const deleteEditor = async (id: number) => {
  if (
    !confirm(
      "Are you sure you want to delete this user's account? This will also delete their notes.",
    )
  )
    return;

  try {
    await api.delete(`/backend/api/admin/delete_user/${id}`);
    await getAllEditors();
    await getAllNotes();
    alert("User successfully deleted!");
  } catch (e) {
    alert("Failed to delete note, please see console for more information.");
    console.log(e);
  }
};

const getAllNotes = async () => {
  try {
    notes.value = await api.get("/backend/api/admin/get_all_notes");
  } catch (e) {
    alert("Failed to get editors, please see console for more info.");
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

const renderText = async (id: number) => {
  const data = await readNote(id);
  result.value = md.render(data?.content || "");
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

const currentTab = ref("");
const switchTab = (tab: string) => {
  currentTab.value = tab;
  search.value = "";

  document.querySelectorAll(".entry").forEach((el) => {
    el.classList.remove("selected");
    if (el.textContent.toLowerCase() === currentTab.value) {
      el.classList.add("selected");
    }
  });
};

onBeforeMount(async () => {
  switchTab("editors");

  await getAllEditors();
  await getAllNotes();

  console.log(editors.value);
  console.log(notes.value);
});
</script>

<template>
  <div class="dashboard">
    <Sidebar :title="title">
      <template v-slot:entries>
        <div class="entry selected" @click="() => switchTab('editors')">
          <p>Editors</p>
          <div class="icon" v-if="currentTab == 'editors'">
            <ArrowRightCircle />
          </div>
        </div>
        <div class="entry" @click="() => switchTab('notes')">
          <p>Notes</p>
          <div class="icon" v-if="currentTab == 'notes'">
            <ArrowRightCircle />
          </div>
        </div>
      </template>
    </Sidebar>

    <div class="admin">
      <div class="options">
        <div class="input-grp">
          <label for="search">
            <Search />
          </label>
          <input
            type="text"
            id="search"
            v-model="search"
            placeholder="Search Query..."
          />
        </div>
      </div>
      <div class="editors-view" v-if="currentTab === 'editors'">
        <div class="table-header">
          <div>
            <h2>Editors</h2>
            <p>Manage registered editor accounts</p>
          </div>

          <span class="count"> {{ filteredEditors.length }} Editors </span>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Activated</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="editor in filteredEditors">
              <td>{{ editor.id }}</td>
              <td>{{ editor.username }}</td>
              <td>{{ editor.email }}</td>
              <td>
                <input
                  type="checkbox"
                  :checked="editor.is_active"
                  @change="(e) => toggleEditor(editor.id, e)"
                />
              </td>
              <td>
                <button
                  class="delete-btn"
                  @click="() => deleteEditor(editor.id)"
                >
                  <Trash />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="notes-view" v-if="currentTab === 'notes'">
        <div class="table-header">
          <div>
            <h2>Notes</h2>
            <p>Manage application notes</p>
          </div>

          <span class="count"> {{ filteredNotes.length }} Notes </span>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>User ID</th>
              <th>Title</th>
              <th>Preview</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="note in filteredNotes">
              <td>{{ note.id }}</td>
              <td>{{ note.user_id }}</td>
              <td>{{ note.title }}</td>
              <td>
                <button
                  class="preview-btn"
                  @click="() => renderText(note.id)"
                  command="show-modal"
                  commandfor="md-dialog"
                >
                  <Eye />
                </button>
              </td>
              <td>
                <button class="delete-btn" @click="() => deleteNote(note.id)">
                  <Trash />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <dialog id="md-dialog">
    <div v-html="result"></div>
    <button commandfor="md-dialog" command="close">Close</button>
  </dialog>
</template>

<style scoped src="../assets/admin.css"></style>
