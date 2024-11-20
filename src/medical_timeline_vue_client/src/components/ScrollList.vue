<template>
  <div id="listContainer" @click="$emit('close')"/>

    <div class="scroll_list input-wrapper">
      <div
          v-for="item in items"
          :key="item.id"
          :id="String(item.id)"
          class="selectable"
          @click="handleClick(item)"
      >
        {{ item.label }}
      </div>
    </div>
</template>
<script lang="ts">
import {defineComponent, type PropType} from 'vue'

export interface IScrollListItem {
  id: number;
  label: string | number;
}

export default defineComponent({
  name: "ScrollList",
  emits: ['update:modelValue', 'change', 'close' ],
  props: {
    items: {
      type: Array as PropType<IScrollListItem[]>,
      required: true
    },
    value: {
      type: Object as PropType<IScrollListItem>,
      default: () => ({id: 0, value: ''})
    },
  },
  created() {
    console.log(this.value.id);
    console.log("created")
    const id = this.value.id;
    this.$nextTick(() => {

      const element = document.getElementById(String(id))
      console.log(element)
      if (element) {
        element.scrollIntoView({behavior: 'instant', block: 'center'});
      }
    })
  },
  methods: {
    handleClick(item: IScrollListItem) {
      this.$emit('update:modelValue', item)
      this.$emit('change', item)
    }
  }
})
</script>
<style scoped lang="scss">

#listContainer {
  position: fixed;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9;
  top: 0;
  left: 0;
}
.scroll_list {
  min-width: 3rem;
  overflow-y: auto;
  height: 300px;
  position: absolute;
  z-index: 10;

}

.selectable {
  width: 100%;
  border-radius: unset;
}

</style>