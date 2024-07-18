<template>
  <div id="app">
    <div class="header">
      <div class="container">
        <theme-selector />
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
import { CustomImage, Message } from "@/components/ChatMessage.vue";
import ThemeSelector from "@/components/ThemeSelector.vue";

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
    ThemeSelector,
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
        console.log(parsed);
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
        console.log(serverMessages);
        for (const serverMessage of serverMessages) {
          this.messages[serverMessage.id] = serverMessage;
        }
      };
    },

    createMessage: async function (message: { text: string; images: File[] }) {
      const result: Message = {
        role: "user",
        text: message.text,
      };

      const readFileAsDataURL = (file: File): Promise<string> => {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onloadend = () => {
            if (reader.result && typeof reader.result === "string") {
              resolve(reader.result);
            } else {
              reject(new Error("Failed to read file as data URL"));
            }
          };
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
      };

      const imageContents = await Promise.all(
        message.images.map(async (image) => {
          const result: CustomImage = image;
          result.data = await readFileAsDataURL(image);
          return result;
        })
      );
      if (!result.images) result.images = [];
      result.images.push(...imageContents);
      return result;
    },

    handleNewUserMessage: async function (message: {
      text: string;
      images: File[];
    }) {
      const userMessage = await this.createMessage(message);
      console.log(userMessage);
      const response = await fetch(this.url + "/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userMessage),
      });
      const serverMessage: Message = await response.json();
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
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);

  .header {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    gap: 1rem;
    position: fixed;
    width: calc(100% - 3rem);
    z-index: 100;
    background-color: var(--background-color);
    .container {
      border: solid 1px var(--text-color);
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
