<template>
  <div class="input-wrapper">
    <label v-if="label" class="input-label">{{ label }}:</label>
    <input
        class="custom-input-general"
        type="text"
        :placeholder="placeholder"
        v-model="localValue"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import './base.css';

export default defineComponent({
  name: 'BaseTextInput',
  props: {
    value: {
      type: String as PropType<string>,
      default: ''
    },
    placeholder: {
      type: String as PropType<string>,
      default: ''
    },
    label: {
      type: String as PropType<string>,
      default: ''
    }
  },
  data() {
    return {
      localValue: this.value as string
    };
  },
  watch: {
    value(newValue: string) {
      this.localValue = newValue;
    },
    localValue(newValue: string) {
      this.$emit('update:modelValue', newValue);
    }
  },
});
</script>

<style scoped>






.custom-input-general:focus {

  border-color: var(--accent-color);
}
</style>
