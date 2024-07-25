<template>
  <div id="app">
    <HeaderComponent :url="url" @forceUpdate="forceUpdate" />
    <ChatDisplay :messages="messages" :status_messages="status_messages" />
    <chat-input @new-message="handleNewUserMessage" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ChatDisplay from "@/components/ChatDisplay.vue";
import ChatInput from "@/components/ChatInput.vue";
import {
  Message,
  ServerMessage,
  StatusMessage,
} from "@/components/ChatMessage.vue";
import HeaderComponent from "@/components/HeaderComponent.vue";

type Data = {
  messages: {
    [key: string]: ServerMessage;
  };
  serverTime: string;
  thread_id: string;
  url: string;
  status_messages: StatusMessage[];
};

export default defineComponent({
  name: "App",
  components: {
    HeaderComponent,
    ChatInput,
    ChatDisplay,
  },
  data(): Data {
    return {
      serverTime: "",
      messages: {},
      thread_id: "",
      url: "http://127.0.0.1:5000/api",
      status_messages: [],
    };
  },
  mounted() {
    this.initialize();
  },
  methods: {
    get_status_messages() {
      const eventSource = new EventSource(this.url + "/status");
      eventSource.onmessage = (event) => {
        console.log("Status message");
        const status_messages: StatusMessage[] = JSON.parse(event.data);
        console.log(status_messages);
        this.status_messages = status_messages;
      };
    },
    messageStream: async function () {
      const eventSource = new EventSource(this.url + "/message/stream");
      eventSource.onmessage = (event) => {
        const parsed = JSON.parse(event.data);
        const localEvent = this.messages[parsed.id];
        if (localEvent) {
          const newText = parsed.content[0].text.value;
          if (!localEvent.text) {
            localEvent.text = parsed.content[0].text.value;
          } else {
            localEvent.text += newText;
          }
        }
      };
    },
    initialize: async function () {
      this.clearMessages();
      this.fetchData();
      this.messageStream();
      this.get_status_messages();
    },
    clearMessages: function () {
      this.messages = {};
      this.status_messages = [];
    },
    fetchData: async function () {
      const eventSource = new EventSource(this.url + "/messages");
      eventSource.onmessage = (event) => {
        console.log("Received message");
        const serverMessages = JSON.parse(event.data);
        console.log(serverMessages);
        this.messages = {};
        for (const serverMessage of serverMessages) {
          this.messages[serverMessage.id] = serverMessage;
        }
      };
    },

    forceUpdate: function () {
      fetch(this.url + "/force_update");
    },

    handleNewUserMessage: async function (message: Message) {
      console.log(message);
      const response = await fetch(this.url + "/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(message),
      });
      console.log(response);
      const serverMessage: ServerMessage = await response.json();
      if (serverMessage.id) {
        this.messages[serverMessage.id] = serverMessage;
      }
    },
  },
});
</script>

<style lang="scss">
body {
  background-color: var(--background-color);
  color: var(--text-color);
  margin: unset !important;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);

  height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
