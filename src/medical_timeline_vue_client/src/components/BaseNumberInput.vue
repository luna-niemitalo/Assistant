<template>
  <div class="input-wrapper">
    <label v-if="label" class="input-label">
      {{ label }}({{min}} - {{max}}):
      <span v-if="isSlider" class="input-slider-label">{{ localValue }}</span>
    </label>
    <input
        v-if="isSlider"
        class="custom-input-general"
        type="range"
        :min="min"
        :max="max"
        :step="step"
        v-model="localValue"
    />
    <input
        v-else
        class="custom-input-general"
        type="text"
        :placeholder="placeholder"
        v-model="localValue"
        @input="handleNumberInput"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import './base.css';

export default defineComponent({
  name: 'BaseNumberInput',
  props: {
    value: {
      type: [String, Number] as PropType<string | number>,
      default: ''
    },
    min: {
      type: Number,
      default: null
    },
    max: {
      type: Number,
      default: null
    },
    step: {
      type: Number,
      default: 1
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
      localValue: this.value as string | number
    };
  },
  computed: {
    isSlider(): boolean {
      return this.min !== null && this.max !== null;
    }
  },
  watch: {
    value(newValue: string | number) {
      this.localValue = newValue;
    },
    localValue(newValue: string | number) {
      this.$emit('update:modelValue', newValue);
    }
  },
  methods: {
    handleNumberInput(event: Event) {
      const target = event.target as HTMLInputElement;
      const numericValue = target.value.replace(/\D/g, ''); // Removes non-numeric characters
      this.localValue = numericValue;
      this.$emit('update:modelValue', numericValue);
    }
  }
});
</script>

<style scoped>





.input-slider-label {
  color: var(--text-color);
}

.custom-input-general[type="range"] {
  border: unset;
  border-radius: var(--input-border-radius);
  cursor: pointer;

}

input[type="range"]::-moz-range-progress {
  background-color: var(--accent-color);
}
input[type="range"]::-moz-range-track {
  background-color: var(--input-border-color);
}

.custom-input-general:focus {
  border-color: var(--accent-color);
}
</style>
