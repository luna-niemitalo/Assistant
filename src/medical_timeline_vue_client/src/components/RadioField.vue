<template>
  <div class="input-wrapper">
    <span class="input-label"> {{ label }}</span>
    <div class="tags">

      <BaseButton
          v-for="option in options"
          type="toggle"
          :label="String(option)"
          :key="option"
          :value="option == selectedOption"
          @update:modelValue="clickHandler(option, $event)"
          active-label="◉︎"
          inactive-label="◎︎"
          size="small"
          icon-size="small"
      />

    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent, type PropType} from 'vue'
import BaseButton from "@/components/BaseButton.vue";

type DataTypings = {
  selectedOption: string | number | null;
}

export default defineComponent({
  name: "RadioField",
  components: {BaseButton},
  props: {
    options: {
      type: Array as PropType<(string | number)[]>,
      required: true
    },
    label: {
      type: String,
      default: ""
    },
    value: {
      type: [String, Number],
      default: null
    }
  },
  data(): DataTypings {
    return {
      selectedOption: this.value
    }
  },
  methods: {
    clickHandler(option: string | number, newValue: boolean) {
      console.log(option, newValue)
      if (newValue) {
        this.selectedOption = option
      } else {

        this.selectedOption = null;
      }
      this.$emit("update:modelValue", this.selectedOption);
    }
  }
})
</script>
<style scoped lang="scss">
.tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  flex-direction: row;
  padding-top: 40px;
}
</style>