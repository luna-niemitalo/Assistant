<template>
  <div
      class="input-wrapper"
      :class="[{ 'toggle-active': isActive }, size, {'disabled': disabled}]"
      @click="clickHandler"
  >
    <span class="input-label"> {{label}}<span v-if="showIcons">:</span> </span>
    <span v-if="showIcons" class="toggle-label" :class="iconSize" >{{ isActive ? activeLabel : inactiveLabel }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import './base.css';

export default defineComponent({
  name: 'BaseButton',
  props: {
    value: {
      type: Boolean as PropType<boolean>,
      default: false
    },
    label: {
      type: String,
      default: 'Button'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'toggle'
    },
    success: {
      type: Boolean,
      default: null
    },
    activeLabel: {
      type: String,
      default: '✓'
    },
    inactiveLabel: {
      type: String,
      default: '⤫'
    },
    size: {
      type: String,
      default:'medium'
    },
    iconSize: {
      type: String,
      default: 'large'
    }
  },
  data() {
    return {
      isActive_internal: this.value,
    };
  },
  watch: {
    value(newVal) {
      this.isActive_internal = newVal;
    }
  },
  computed: {
    isActive: function () {
      if (this.type === 'toggle') return this.isActive_internal;
      if (this.type === "submit") {
        return this.success;
      }
      return false;
    },
    showIcons: function () {
      if (this.type === 'toggle') return true;
      if (this.type === 'submit') {
        if (this.success === null) {
          return false;
        }
        return true;
      }
      return false;
    }
  },
  methods: {
    clickHandler() {
      if (this.disabled) return;
      if (this.type !== 'toggle') {
        this.$emit('customClick');
        return;
      }
      this.isActive_internal = !this.isActive_internal;
      this.$emit('update:modelValue', this.isActive_internal);
    }
  }
});
</script>

<style scoped>

.input-label {
  position: relative;
  background-color: transparent;
  margin: unset;
  padding: unset;
  left: unset;
  font-size: unset;
  color: var(--text-color);
}
.input-wrapper {
  min-height: unset;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-color: var(--button-normal-bg);
  color: var(--button-normal-text);
  border: var(--input-border-width) solid var(--button-active-bg);
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
  padding: 10px 20px;
  height: min-content;
  gap: 10px;
}

.input-wrapper:hover {
  background-color: var(--button-hover-bg);
  color: var(--button-hover-text);
}

.input-wrapper:active {
  background-color: var(--button-normal-pressed-bg);
  color: var(--button-normal-pressed-text);
}

.input-wrapper.disabled {
  background-color: var(--button-disabled-bg);
  color: var(--button-disabled-text);
  border-color: var(--button-disabled-border);
  cursor: not-allowed; /* Change the cursor to indicate it's disabled */
}

.toggle-active.disabled {
  background-color: var(--button-disabled-bg);
  color: var(--button-disabled-text);
  border-color: var(--button-disabled-border);
  cursor: not-allowed;
}


.toggle-active {
  background-color: var(--button-active-bg);
  color: var(--button-active-text);
}

.toggle-active:hover {
  background-color: var(--button-active-hover-bg);
  color: var(--button-active-hover-text);
}

.toggle-active:active {
  background-color: var(--button-active-pressed-bg);
  color: var(--button-active-pressed-text);
}

.toggle-label {
  user-select: none;

  margin: unset;
  padding: unset;
}
</style>
