<template>
  <div class="chat_display" ref="chatDisplay" @scroll="handleScroll">
    <div v-for="message in sorted_and_merged_messages" :key="message.timestamp">
      <ChatMessage :message="message" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, nextTick } from "vue";
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
  data: function () {
    return {
      chatDisplay: ref<HTMLDivElement | null>(null),
      scrollTop: 0,
      clientHeight: 0,
      scrollHeight: 0,
    };
  },
  mounted() {
    this.chatDisplay = this.$refs.chatDisplay as HTMLDivElement;
    console.log(this.chatDisplay);
  },
  watch: {
    async messages() {
      await nextTick();
      console.log("Message watcher");
      if (this.isScrolledToBottom && this.chatDisplay) {
        this.scrollTop = this.chatDisplay.scrollHeight;
      }
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
    isScrolledToBottom(): boolean {
      console.log(
        "IscScrolledTobottom",
        this.scrollTop,
        " : ",
        this.clientHeight,
        " : ",
        this.scrollHeight,
        " : Math result: ",
        this.scrollHeight - (this.scrollTop + this.clientHeight)
      );
      return this.scrollHeight - (this.scrollTop + this.clientHeight) < 1;
    },
  },
  methods: {
    handleScroll() {
      if (this.chatDisplay) {
        this.scrollTop = this.chatDisplay.scrollTop;
        this.clientHeight = this.chatDisplay.clientHeight;
        this.scrollHeight = this.chatDisplay.scrollHeight;
      }
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
