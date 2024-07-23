<template>
  <div class="assistant-selector">
    <label :for="dropdownId">{{ label }}</label>
    <select :id="dropdownId" @change="handleChange">
      <option
        v-for="option in options"
        :key="option"
        :value="option"
        :selected="selectedOption(option)"
      >
        {{ option }}
      </option>
    </select>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "AssistantSelector",
  props: {
    options: {
      type: Array as () => string[],
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  computed: {
    dropdownId(): string {
      return `${this.label.replace(/\s+/g, "-").toLowerCase()}-dropdown`;
    },
  },
  methods: {
    selectedOption(option: string): boolean {
      return option === this.label;
    },
  },
});
</script>

<style scoped>
.assistant-selector {
  display: flex;
  flex-direction: column;
}
</style>
