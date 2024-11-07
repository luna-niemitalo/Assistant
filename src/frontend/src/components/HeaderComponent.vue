<template>
  <div class="header">
    <div class="container">
      <theme-selector />
    </div>
    <div class="container" id="title">
      <span>Assistant</span>
      <AssistantSelector
        :label="assistant_selection.selection"
        :options="assistant_selection.options"
        @change="assistantChanged"
      />
    </div>
    <div class="container header_thread">
      <span>Thread ID: {{ thread_id }}</span>
      <div class="thread_controls">
        <font-awesome-icon icon="plus" @click="newThread" />
        <font-awesome-icon icon="sync" @click="$emit('forceUpdate')" />
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import AssistantSelector from "@/components/AssistantSelector.vue";
import ThemeSelector from "@/components/ThemeSelector.vue";
import { defineComponent } from "vue";
import { buildApiUrl } from "@/utils";

export default defineComponent({
  name: "HeaderComponent",
  components: { AssistantSelector, ThemeSelector },
  data() {
    return {
      thread_id: "",
      assistant_selection: {
        selection: "",
        options: [],
      },
    };
  },
  mounted() {
    this.get_thread_id();
    this.get_assistant_selection();
  },
  methods: {
    get_assistant_selection: async function () {
      const response = await fetch(buildApiUrl("assistant"));
      const data = await response.json();
      console.log(data);
      this.assistant_selection = data;
    },
    async assistantChanged(assistant: Event) {
      const target = assistant.target as HTMLSelectElement;
      console.log(target.value);
      await fetch(buildApiUrl("assistant"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ selection: target.value }),
      });

      this.$emit("initialize");
    },
    get_thread_id: async function () {
      const eventSource = new EventSource(buildApiUrl("thread"));
      eventSource.onmessage = (event) => {
        this.thread_id = event.data;
      };
    },
    newThread: async function () {
      await fetch(buildApiUrl("thread"), {
        method: "POST",
      });
    },
  },
});
</script>
<style lang="scss" scoped>
body {
  background-color: var(--background-color);
  color: var(--text-color);
}

.header {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  gap: 1rem;
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
</style>
