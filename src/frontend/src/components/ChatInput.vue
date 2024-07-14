<template>
  <div class="chat-input">
    <input
      v-model="messageText"
      placeholder="Type your message..."
      @keyup.enter="sendMessage"
    />
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
    };
  },
  methods: {
    sendMessage() {
      if (this.messageText.trim() === "") return;
      this.$emit("new-message", this.messageText.trim());
      this.messageText = "";
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
}

.chat-input input {
  flex-grow: 1;
  margin-right: 1rem;
  padding: 0.5rem;
  font-size: 1rem;
}

.chat-input button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
}
</style>
