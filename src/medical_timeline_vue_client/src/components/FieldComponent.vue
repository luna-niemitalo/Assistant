<template>
<div class="field">
  <label class="label">{{label}}:</label>
  <slot class="content"></slot>
</div>
</template>
<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "FieldComponent",
  props: {
    label: {
      type: String,
      required: true
    }
  }
})
</script>
<style scoped lang="scss">

.field {
  min-width: 250px;
  width: min-content;
  display: flex;
  flex-direction: column;
  border-radius: 4px;
  border: 2px solid var(--button-hover-bg);
  padding: 10px;
  row-gap: 10px;
  background-color: var(--background-color);
  color: var(--text-color);

  label {
    font-weight: bold;
    font-size: larger;
    position: absolute;
    color: var(--text-color);
    padding: 5px;
  }
}
</style>