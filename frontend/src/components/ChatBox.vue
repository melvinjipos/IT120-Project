<template>
  <v-container>
    <v-row justify="center">
      <!-- Inbox (top section) -->
      <v-col cols="5">
        <v-card class="mb-3 bg-card" elevation="2">
          <v-card-title>
            <div class="headline text-center">Available Users</div>
          </v-card-title>
          <v-list>
            <v-list-item-group v-if="filteredUsers.length > 0">
              <v-list-item
                v-for="user in filteredUsers"
                :key="user.id"
                @click="selectReceiver(user)"
                class="my-2"
                :class="{
                  'selected-user':
                    selectedReceiver && selectedReceiver.id === user.id,
                }"
              >
                <v-list-item-content>
                  <v-list-item-title class="py-2">
                    <v-avatar image="@/assets/images/user.png"></v-avatar>
                    <span class="text-h6 ms-3">{{ user.name }}</span>
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
            <v-list-item v-else>
              <v-list-item-content>
                <v-list-item-title
                  >No conversations available...</v-list-item-title
                >
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center">
      <!-- Chat Box (bottom section) -->
      <v-col cols="8">
        <v-card v-if="selectedReceiver" class="pa-6 bg-card" elevation="2">
          <v-card-title>
            <div>
              <div class="headline">{{ selectedReceiver.name }}</div>
              <div class="caption">Chat with {{ selectedReceiver.name }}</div>
            </div>
          </v-card-title>

          <v-card-subtitle>
            <v-scroll-y class="message-list">
              <v-list class="bg-transparent">
                <v-list-item-group v-if="messages && messages.length > 0">
                  <v-list-item v-for="message in messages" :key="message.id">
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-card class="pa-6 mb-3 rounded-s-xl" color="#171717">
                          <h4>{{ message.content }}</h4>
                        </v-card>
                      </v-list-item-title>
                      <div class="mb-5">
                        <span class="mx-5">{{ message.timestamp }}</span>
                        <span class="mx-5"
                          >sent to: {{ message.receiver }}</span
                        >
                        <span class="mx-5"
                          >Ensure that your secrets are safe with us.</span
                        >
                      </div>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item v-else>
                  <v-list-item-content>
                    <v-list-item-title>No messages yet...</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-scroll-y>
          </v-card-subtitle>

          <!-- Message Input and button -->
          <v-card-actions>
            <v-row>
              <v-col>
                <div class="d-flex">
                  <v-textarea
                    v-model="newMessage"
                    color="deep-purple-lighten-2"
                    placeholder="Type your message here..."
                    rows="1"
                    variant="outlined"
                    rounded
                    class="flex-grow-1 me-2"
                  />
                  <v-btn
                    @click="sendMessage"
                    :disabled="!newMessage"
                    class="ms-2"
                    icon="mdi-send"
                    color="deep-purple-lighten-2"
                    variant="tonal"
                    size="large"
                  ></v-btn>
                </div>
              </v-col>
            </v-row>
          </v-card-actions>
        </v-card>

        <!-- Reply messages -->
        <v-card v-else class="pa-3 mt-3" elevation="2">
          <v-card-title>
            <div class="headline">No replies yet</div>
          </v-card-title>
        </v-card>

        <v-card v-else class="pa-3 bg-card" elevation="2">
          <v-card-title>
            <div class="headline">
              Select a user to whom you want to whisper.
            </div>
          </v-card-title>
          <v-card-subtitle>
            <div class="caption">
              Click on a user from the Inbox to start a chat. Ensure that your
              secrets are safe with us.
            </div>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user: {
        id: null,
        name: "",
        avatar: "",
      },
      users: [],
      selectedReceiver: null,
      newMessage: "",
      messages: [], // Default value is an empty array to avoid undefined errors
      replies: [], // Default value is an empty array to avoid undefined errors
    };
  },
  created() {
    this.fetchUserData();
    this.fetchUsers();
    this.startMessagePolling(); // Start polling for new replies
  },
  computed: {
    filteredUsers() {
      return this.users.filter((user) => user.id !== this.user.id);
    },
  },
  methods: {
    async fetchUserData() {
      try {
        const userResponse = await axios.get("http://localhost:8000/api/me/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.user = userResponse.data;
        this.fetchMessages();
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    async fetchUsers() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/users/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        if (
          response.data.status === "success" &&
          Array.isArray(response.data.data.users)
        ) {
          this.users = response.data.data.users;
        }
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    selectReceiver(user) {
      this.selectedReceiver = user;
      this.fetchMessages();
      this.replies = []; // Clear previous replies when switching users
    },
    async fetchMessages() {
      if (!this.selectedReceiver) return;
      try {
        const receiverId = this.selectedReceiver.id;

        const response = await axios.get(
          "http://127.0.0.1:8000/chat/api/conversation-messages/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: {
              receiver_id: receiverId,
              sender_id: this.user.id,
            },
          }
        );

        this.messages = response.data;
        this.fetchReplies(); // Fetch replies from the selected receiver
      } catch (error) {
        console.error("Error fetching messages:", error);
      }
    },
    async fetchReplies() {
      if (!this.selectedReceiver) return;
      try {
        const receiverId = this.selectedReceiver.id;

        const response = await axios.get(
          "http://127.0.0.1:8000/chat/api/conversation-messages/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: {
              sender_id: receiverId, // Get replies from the selected user
              receiver_id: this.user.id,
            },
          }
        );

        this.replies = response.data; // Store the replies
      } catch (error) {
        console.error("Error fetching replies:", error);
      }
    },
    startMessagePolling() {
      // Polling to fetch new messages every 5 seconds
      setInterval(() => {
        if (this.selectedReceiver) {
          this.fetchMessages();
          this.fetchReplies();
        }
      }, 2000);
    },
    async sendMessage() {
      if (!this.selectedReceiver || !this.newMessage) return;

      const messageData = {
        sender: this.user.id,
        receiver: this.selectedReceiver.id,
        content: this.newMessage,
        timestamp: new Date().toISOString(),
      };

      try {
        const response = await axios.post(
          "http://localhost:8000/chat/api/messages/",
          messageData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.messages.push({
          id: response.data.id,
          sender_name: this.user.name,
          content: this.newMessage,
        });

        this.newMessage = "";
      } catch (error) {
        console.error("Error sending message:", error);
      }
    },
  },
};
</script>

<style scoped>
.headline {
  font-size: 1.5em;
  font-weight: bold;
  font-family: "monospace";
}

.caption {
  font-size: 0.9em;
  color: grey;
}

.selected-user {
  background: rgba(149, 117, 205, 0.138);
  border: 1px solid rgba(149, 117, 205, 0.3);
}

.v-list-item {
  cursor: pointer;
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

.v-textarea {
  flex-grow: 1;
}

.message-list,
.reply-list {
  max-height: 100px; /* Adjust height as needed */
  overflow-y: auto;
}

:deep(textarea) {
  border-radius: 4rem !important;
  background-color: #15151571 !important;
  border-style: none;
}

:deep(.v-textarea .v-field__input) {
  mask-image: none;
}
</style>
