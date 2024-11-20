

<template>
  <div class="input-wrapper">
    <label v-if="label" class="input-label">{{ label }}:
      <span class="date_label">{{selectedDate}}</span>
    </label>
    <div class="custom-input-general">

      <DatePicker v-model="selectedDate" />
    </div>

  </div>

</template>
<script lang="ts">
import {defineComponent} from 'vue'
import DatePicker from "@/components/DatePicker.vue";

export default defineComponent({
  name: "DateTimePicker",
  components: {DatePicker},
  props: {
    label: {
      type: String,
      default: ''
    },
    value: {
      type: Date,
      default: new Date()
    }
  },
  data() {
    return {
      selectedDate: this.value
    }
  }
})
</script>
<style scoped lang="scss">
.date_label {
  color: var(--text-color);
  font-size: var(--font-small);
}

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