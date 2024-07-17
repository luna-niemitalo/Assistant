<template>
  <div class="chat-input">
    <input type="file" multiple @change="handleFileUpload" />
    <textarea
      v-model="messageText"
      placeholder="Type your message..."
      @keydown="handleKeydown"
    ></textarea>
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Message } from "@/components/ChatMessage.vue";

export default defineComponent({
  name: "ChatInput",
  data() {
    return {
      messageText: "",
      images: [] as File[],
    };
  },
  methods: {
    sendMessage() {
      if (this.messageText.trim() === "" && this.images.length === 0) return;
      console.log(this.messageText);
      console.log(this.images);
      this.$emit("new-message", {
        text: this.messageText.trim(),
        images: this.images,
      });
      //this.messageText = "";
      //this.images = [];
    },
    handleFileUpload(event: Event) {
      const files = (event.target as HTMLInputElement).files;
      if (files) {
        this.images = Array.from(files);
      }
    },
    handleKeydown(event: KeyboardEvent) {
      if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
        this.sendMessage();
      }
    },
  },
});
</script>

<style scoped>
.chat-input {
  position: fixed;
  bottom: 0;
  left: 0;
  width: calc(100% - 2rem);
  padding: 1rem;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;

  button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 8px;
  }
  textarea {
    flex-grow: 1;
    margin-right: 1rem;
    padding: 0.5rem;
    font-size: 1rem;
    resize: none;
  }

  input[type="file"] {
    margin-top: 8px;
  }
}
</style>
