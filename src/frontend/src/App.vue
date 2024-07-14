<template>
  <div id="app">
    <div class="header">
      <div class="container">
        <span>Current time from server: {{ serverTime }}</span>
      </div>
      <div class="container" id="title">Assistant</div>
      <div class="container header_thread">
        <span>Thread ID: {{ thread_id }}</span>
        <div class="thread_controls">
          <font-awesome-icon icon="plus" @click="newThread" />
          <font-awesome-icon icon="sync" @click="initialize" />
        </div>
      </div>
    </div>
    <ChatDisplay :messages="messages" />
    <chat-input @new-message="handleNewUserMessage" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ChatDisplay from "@/components/ChatDisplay.vue";
import ChatInput from "@/components/ChatInput.vue";
import { Message } from "@/components/ChatMessage.vue";

type Data = {
  messages: {
    [key: string]: Message;
  };
  serverTime: string;
  thread_id: string;
  url: string;
};

export default defineComponent({
  name: "App",
  components: {
    ChatInput,
    ChatDisplay,
  },
  data(): Data {
    return {
      serverTime: "",
      messages: {},
      thread_id: "",
      url: "http://127.0.0.1:5000/api",
    };
  },
  mounted() {
    this.initialize();
  },
  methods: {
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
    newThread: async function () {
      this.clearMessages();
      const response = await fetch(this.url + "/thread/new", {
        method: "POST",
      });
      this.fetchData();
    },
    initialize: async function () {
      this.clearMessages();
      this.get_thread_id();
      this.fetchData();
      this.messageStream();
    },
    get_thread_id: async function () {
      const eventSource = new EventSource(this.url + "/thread/id");
      eventSource.onmessage = (event) => {
        this.thread_id = event.data;
      };
    },
    clearMessages: function () {
      this.messages = {};
    },
    fetchData: async function () {
      const eventSource = new EventSource(this.url + "/messages");
      eventSource.onmessage = (event) => {
        console.log("Received message");
        const serverMessages = JSON.parse(event.data);
        for (const serverMessage of serverMessages) {
          const message = this.serverMessageToMessage(serverMessage);
          this.messages[message.id] = message;
        }
      };
    },

    handleNewUserMessage: async function (message: string) {
      const response = await fetch(this.url + "/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(message),
      });
      message = await response.json();
      const serverMessage = this.serverMessageToMessage(message);
      this.messages[serverMessage.id] = serverMessage;
    },

    serverMessageToMessage: function (serverMessage: any): Message {
      return {
        id: serverMessage.id,
        text: serverMessage.content
          .map((content: { text: { value: any } }) => content.text?.value)
          .join(" "),
        role: serverMessage.role,
        timestamp: new Date().getTime(),
      };
    },
  },
});
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;

  .header {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    gap: 1rem;
    position: fixed;
    width: calc(100% - 3rem);
    z-index: 100;
    background-color: white;
    .container {
      border: solid 1px #ccc;
      flex: 2;
      align-content: center;
      align-items: center;
      text-align: center;
    }
    #title {
      font-size: 1.5rem;
      font-weight: bold;
      flex: 1;
    }
    &_thread {
      display: flex;
      justify-content: space-evenly;
      .thread_controls {
        display: flex;
        gap: 1rem;
      }
    }
  }
}
</style>
