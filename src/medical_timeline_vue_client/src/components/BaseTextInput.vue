<template>
  <div class="input-wrapper">
    <label v-if="label" class="input-label">{{ label }}:</label>
    <input
        class="input-field"
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
.input-wrapper {
  border: unset;

}

.input-label {
  position: absolute;
  top: 0.3rem;
  left: var(--input-padding);
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--text-alt-color);
  pointer-events: none;
  text-transform: capitalize;
}

.input-field {
  width: 100%;
  padding: var(--input-padding);
  font-size: var(--input-font-size);
  color: var(--text-color);
  background: var(--input-background);
  border: 3px solid var(--input-border-color);
  border-radius: var(--input-border-radius);
  outline: none;
  transition: border-color 0.2s ease-in-out;
  padding-top: 2rem; /* Offset for label */

  text-overflow: unset;
}

.input-field:focus {

  border-color: var(--accent-color);
}
</style>
