<template>
  <v-app class="app-container">
    <!-- Top Navigation Bar -->
    <v-app-bar app color="#151515" class="px-5">
      <!-- App Title -->
      <v-toolbar-title class="text-h5 font-weight-black"
        >Sender</v-toolbar-title
      >

      <!-- Navigation Tabs -->
      <v-tabs v-model="activeTab" class="mx-5" color="deep-purple-lighten-2">
        <v-tab
          :class="{ 'active-tab': isActiveTab('dashboard') }"
          value="dashboard"
        >
          <v-icon
            left
            class="me-1"
            :class="{ 'active-icon': isActiveTab('dashboard') }"
            >mdi-view-dashboard</v-icon
          >
          <span :class="{ 'active-text': isActiveTab('dashboard') }"
            >Dashboard</span
          >
        </v-tab>
        <v-tab :class="{ 'active-tab': isActiveTab('chats') }" value="chats">
          <v-icon
            left
            class="me-1"
            :class="{ 'active-icon': isActiveTab('chats') }"
            >mdi-chat</v-icon
          >
          <span :class="{ 'active-text': isActiveTab('chats') }"
            >Send a Message</span
          >
        </v-tab>
      </v-tabs>

      <v-spacer></v-spacer>

      <!-- Notification Icon with Badge -->
      <v-btn size="x-small" variant="tonal" icon class="mr-3">
        <v-badge color="#9575CD" dot>
          <v-icon>mdi-bell</v-icon>
        </v-badge>
      </v-btn>

      <!-- User Settings Menu -->
      <v-menu transition="slide-y-transition">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar :image="avatarImage"></v-avatar>
          </v-btn>
        </template>

        <v-sheet class="pa-0 mt-2 me-1 menu-card" color="grey-darken-3">
          <div>
            <v-btn
              class="justify-start"
              rounded="0"
              variant="text"
              size="large"
              block
              @click="handleLogoutClick"
              style="text-transform: none"
            >
              <v-row align="center" no-gutters>
                <v-col cols="auto">
                  <v-icon class="me-3" left>mdi-logout</v-icon>
                </v-col>
                <v-col @click="logout"> Logout </v-col>
              </v-row>
            </v-btn>
          </div>
        </v-sheet>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="custom-main">
      <v-container fluid class="main-container pa-8 rounded-lg">
        <v-row justify="center" v-if="activeTab === 'dashboard'" class="mb-4">
          <v-col cols="3">
            <v-card class="bg-card">
              <!-- count total user -->
              <v-container class="px-12 py-8">
                <h1>{{ totalUsers }}</h1>
                <h4 class="font-weight-regular">User</h4>
              </v-container>
            </v-card>
          </v-col>

          <v-col cols="3">
            <v-card class="bg-card">
              <!-- count total admin -->
              <v-container class="px-12 py-8">
                <h1>{{ totalAdmins }}</h1>
                <h4 class="font-weight-regular">Admin</h4>
              </v-container>
            </v-card>
          </v-col>
        </v-row>
        <v-row v-if="activeTab === 'dashboard'" justify="center">
          <v-col cols="7" lg="7" md="7" sm="12">
            <UserTable :userData="users" />
          </v-col>
        </v-row>
        <v-row v-else-if="activeTab === 'chats'">
          <v-col cols="12">
            <ChatBox />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth"; // Import the auth store
import UserTable from "@/views/dashboard/UserTable.vue";
import ChatBox from "@/components/ChatBox.vue"; // Import ChatBox component
import avatarImage from "@/assets/images/user.png";

const users = ref([]);
const totalUsers = ref(0);
const totalAdmins = ref(0);
const activeTab = ref(localStorage.getItem("activeTab") || "dashboard"); // Retrieve activeTab from local storage

const fetchUsers = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/users/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    users.value = response.data.data.users.map((user) => ({
      username: user.name,
      email: user.email,
      status: "active",
      is_superuser: user.is_superuser,
    }));
    console.log("users", users.value.is_superuser);
    console.log("users", users.value);
  } catch (err) {
    console.error("Error fetching users:", err.message);
  }
};

const fetchUserCounts = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/user-counts/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    totalUsers.value = response.data.total_users;
    totalAdmins.value = response.data.total_admins;
  } catch (err) {
    console.error("Error fetching user counts:", err.message);
  }
};

const logout = () => {
  const authStore = useAuthStore();
  authStore.logout(); // Clear the auth token in Pinia store
};

onMounted(() => {
  fetchUsers();
  fetchUserCounts();
});

// Watch for changes in activeTab and save it to local storage
watch(activeTab, (newTab) => {
  localStorage.setItem("activeTab", newTab);
});

const isActiveTab = (tab) => {
  return activeTab.value === tab;
};
</script>

<style scoped>
.custom-main {
  padding-top: 64px; /* To account for the app bar height */
}

.active-icon {
  color: #9575cd !important;
}

.active-text {
  color: #9575cd !important;
}

.bg-card {
  /* From https://css.glass */
  background: rgba(149, 117, 205, 0.138);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid rgba(149, 117, 205, 0.3);
}
</style>
