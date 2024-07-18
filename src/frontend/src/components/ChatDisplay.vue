<template>
  <div class="chat_display">
    <div v-for="message in messages" :key="message.id">
      <ChatMessage :message="message" />
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import ChatMessage from "@/components/ChatMessage.vue";
import { Message } from "@/components/ChatMessage.vue";

export default defineComponent({
  components: { ChatMessage },
  props: {
    messages: {
      type: Array as () => Message[],
      required: true,
    },
  },
});
</script>

<style scoped lang="scss">
.chat_display {
  padding: 5rem 1rem;
  max-height: calc(100vh - 14rem);
  overflow-y: auto;
}
</style>
