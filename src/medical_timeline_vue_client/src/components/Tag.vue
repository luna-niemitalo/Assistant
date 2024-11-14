<template>
  <div class="tag" :class="{ selected: tag.selected }">
    {{tag.name}}
  </div>
</template>
<script lang="ts">
import {defineComponent, type PropType} from 'vue'

export interface ITag {
  name: string,
  key: number,
  selected: boolean,
}

export default defineComponent({
  name: "TagComponent",
  props: {
    tag: {
      type: Object as PropType<ITag>,
      required: true,
    },
  },
})
</script>
<style scoped lang="scss">
@import '../assets/base.css';

.tag {
  margin: 5px;
  padding: 5px 10px;
  border: 1px solid var(--button-normal-text);
  background-color: var(--button-normal-bg);
  color: var(--button-normal-text);
  border-radius: 10px;
  cursor: pointer;
  width: min-content;
  transition: background-color 0.3s;

  height: min-content;
  white-space: nowrap;

  &:hover {
    background-color: var(--button-hover-bg);
    color: var(--button-hover-text);
  }

  &.selected {
    background-color: var(--button-active-bg);
    color: var(--button-active-text);
  }
}

</style>