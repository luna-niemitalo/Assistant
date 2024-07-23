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
import { CustomImage } from "@/components/ChatMessage.vue";

export default defineComponent({
  name: "ChatInput",
  data() {
    return {
      messageText: "",
      images: [] as File[],
    };
  },
  methods: {
    sendMessage: async function () {
      if (this.messageText.trim() === "" && this.images.length === 0) return;
      console.log(this.messageText);
      console.log(this.images);

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
        this.images.map(async (image) => {
          const result: CustomImage = image;
          result.data = await readFileAsDataURL(image);
          return result;
        })
      );
      this.$emit("new-message", {
        text: this.messageText.trim(),
        images: imageContents,
        role: "user",
      });
      this.messageText = "";
      this.images = [];
    },
    handleFileUpload(event: Event) {
      const files = (event.target as HTMLInputElement).files;
      if (files) {
        this.images = Array.from(files);
      }
    },
    handleKeydown(event: KeyboardEvent) {
      if (event.key === "Enter") {
        if (event.shiftKey) return;
        this.sendMessage();
      }
    },
  },
});
</script>

<style scoped>
.chat-input {
  width: calc(100% - 2rem);
  padding: 1rem;
  background-color: var(--contrast-background-color);
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
    background-color: var(--background-color);
    color: var(--text-color);
    border-color: #454545;
  }

  input[type="file"] {
    margin-top: 8px;
  }
}
</style>
