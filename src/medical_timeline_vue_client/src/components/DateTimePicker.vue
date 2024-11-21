

<template>

    <div class="">

      <DatePicker v-model="selectedDate" />
    </div>


</template>
<script lang="ts">
import {defineComponent} from 'vue'
import DatePicker from "@/components/DatePicker.vue";

export default defineComponent({
  name: "DateTimePicker",
  components: {DatePicker},
  props: {
  },
  data() {
    return {
      selectedDate: new Date()
    }
  }
})
</script>
<style scoped lang="scss">


.custom-input-general {
  width: 600px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  input {
    background-color: var(--background-color);
    color: var(--text-color);
    border: unset;
    cursor: pointer;
    &:focus-visible {
      border: unset;
      outline: none;
    }
  }
}

</style>