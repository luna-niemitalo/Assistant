<template>
  <div class="chat_display">
    <div v-for="message in sorted_and_merged_messages" :key="message.timestamp">
      <ChatMessage :message="message" />
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import ChatMessage, {
  ServerMessage,
  StatusMessage,
} from "@/components/ChatMessage.vue";

export default defineComponent({
  components: { ChatMessage },
  props: {
    messages: {
      type: Object as () => { [key: string]: ServerMessage },
      required: true,
    },
    status_messages: {
      type: Array as () => StatusMessage[],
      required: true,
    },
  },
  computed: {
    sorted_and_merged_messages(): ServerMessage[] {
      const messages = Object.values(this.messages);
      const status_messages: ServerMessage[] = this.status_messages.map(
        (status_message) => {
          return {
            text: status_message.message,
            role: "system",
            timestamp: status_message.timestamp,
          };
        }
      );
      const all_messages = messages.concat(status_messages);
      return all_messages.sort((a, b) => a.timestamp - b.timestamp);
    },
  },
});
</script>

<style scoped lang="scss">
.chat_display {
  flex: 1;
  overflow-y: auto;
}
</style>
