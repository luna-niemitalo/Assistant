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
import { ServerMessage } from "@/components/ChatMessage.vue";

export default defineComponent({
  components: { ChatMessage },
  props: {
    messages: {
      type: Object as () => { [key: string]: ServerMessage },
      required: true,
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
