<template>
  <div class="input-wrapper">
    <label v-if="label" class="input-label">
      {{ label }}:
      <span v-if="isSlider" class="input-slider-label">{{ localValue }}</span>
    </label>
    <input
        v-if="isSlider"
        class="input-field"
        type="range"
        :min="min"
        :max="max"
        :step="step"
        v-model="localValue"
    />
    <input
        v-else
        class="input-field"
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
.input-wrapper {
  border: unset;
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
}

.input-slider-label {
  color: var(--text-color);
}

.input-field[type="range"] {
  border: 3px solid var(--input-border-color);
  border-radius: var(--input-border-radius);
  cursor: pointer;

}

input[type="range"]::-moz-range-progress {
  background-color: var(--accent-color);
}
input[type="range"]::-moz-range-track {
  background-color: var(--input-border-color);
}

.input-field:focus {
  border-color: var(--accent-color);
}
</style>
