<template>
  <div class="input-wrapper">
    <label v-if="label" class="input-label">{{ label }}:</label>
    <textarea
        class="custom-input-general textarea-field"
        :placeholder="placeholder"
        v-model="localValue"
        @input="handleTextAreaInput"
    ></textarea>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import './base.css';

export default defineComponent({
  name: 'BaseTextArea',
  props: {
    value: {
      type: String as PropType<string>,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    label: {
      type: String,
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
  methods: {
    handleTextAreaInput(event: Event) {
      const target = event.target as HTMLTextAreaElement;
      this.localValue = target.value;
      this.$emit('update:modelValue', target.value);
    }
  }
});
</script>

<style scoped>
.input-wrapper {
  position: relative;
  border-radius: var(--input-border-radius);
  min-width: 100px;
  flex-grow: unset;
}



.textarea-field {
  min-height: 100px;
  min-width: 100px;
  width: 300px;
  resize: both;
  left: var(--input-border-width);
  top: var(--input-border-width);
  margin-left: -3px;

}
.input-label {
  width: 100%;
  z-index: 1;
  left: 0;
  padding-left: 14px;
  padding-top: 5px;
}

.textarea-field:focus {
  border-color: var(--accent-color);
}
</style>
