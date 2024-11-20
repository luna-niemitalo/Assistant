<template>
  <div id="datePicker" @click="$emit('close')"/>

  <div class="calendar_container input-wrapper">
    <div class="calendar_header">
      <div class="calendar_controls">
        <!--<button @click="previousMonth">{{ prevIcon }}</button>-->
        <div class="slot">
          <div @click.prevent.stop="showYearSelector = true">{{ internal_status.selectedYear?.label }}</div>
          <ScrollList v-if="showYearSelector"
                      :items="internal_status.years"
                      :value="internal_status.selectedYear"
                      v-model="internal_status.selectedYear"
                      @change="submitUpdate"
                      @close="showYearSelector = false"
          />
        </div>
        /
        <div class="slot">
          <div @click.prevent.stop="showMonthSelector = true">{{ internal_status.selectedMonth?.label }}</div>
          <ScrollList v-if="showMonthSelector"
                      :items="internal_status.months"
                      :value="internal_status.selectedMonth"
                      v-model="internal_status.selectedMonth"
                      @change="submitUpdate"
                      @close="showMonthSelector = false"
          />
        </div>
      <!--<button @click="nextMonth">{{ nextIcon }}</button>-->
      </div>
      <div class="week_headers">
        <div class="week_header_day" v-for="day in weekdays" :key="day">{{ day }}</div>
      </div>
    </div>
    <div class="calendar_display" v-if="internal_days">
      <div
          class="selectable"
          v-for="day in internal_days"
          :key="day.id + Number(day.weekday)"
          :style="{ 'grid-column': String(day.weekday) }"
          @click="dayChange(day)">
        {{ day.label }}
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent, type PropType} from 'vue'
import ScrollList from "@/components/ScrollList.vue";
import type {DateSelection} from "@/components/DatePicker.vue";

export interface CalendarItem {
  id: number;
  weekday?: number;
  label: string | number;
}

type DataTypings = {
  weekdays: string[];
  internal_status: DateSelection;
  showYearSelector: boolean;
  showMonthSelector: boolean;
  internal_days: CalendarItem[];
}

export default defineComponent({
  name: "CalendarDatePicker",
  components: {ScrollList},
  emits: ['update:modelValue', 'change', 'close'],
  props: {
    dateSelection: {
      type: Object as PropType<DateSelection>,
      required: true,
    }
  },
  data(): DataTypings {
    return {
      weekdays: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      internal_status: this.dateSelection,
      showYearSelector: false,
      showMonthSelector: false,
      internal_days: []
    }
  },
  mounted() {
    this.calculateInternalDays(this.dateSelection);
  },
  methods: {
    submitUpdate() {
      this.showYearSelector = false;
      this.showMonthSelector = false;
      this.$emit('update:modelValue', this.internal_status)
      this.$emit('change', this.internal_status)
    },
    dayChange(item: CalendarItem) {
      this.internal_status.selectedDay = item;
      this.submitUpdate();
      this.$emit('close');
    },
    calculateInternalDays(newVal: DateSelection) {
      this.internal_days = [];
      const internal_days = [];
      for (const day of newVal.days) {
        const dayDate = new Date(
            Number(newVal.selectedYear?.label),
            Number(newVal.selectedMonth?.id),
            day.id
        );
        internal_days.push({...day, weekday: dayDate.getDay()});
      }
      this.internal_days = internal_days;
      this.$forceUpdate();
    }
  },
  watch: {
    dateSelection: {
      deep: true,
      handler(newVal) {
        this.calculateInternalDays(newVal);
        this.internal_status = newVal;
      }
    }
  }
})
</script>
<style scoped lang="scss">

#datePicker {
  position: fixed;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9;
  top: 0;
  left: 0;
}

.calendar_header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  .calendar_title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom:.5rem;

    div {
      cursor: pointer;
      transition: color 0.2s ease;

      &:hover {
        color: var(--button-hover-bg);
      }
    }
  }

  .week_headers {
    display: grid;
    grid-template-columns: repeat(7, auto);

    .week_header_day {
      text-align: center;
    }

  }
}
.calendar_controls {
  display: flex;
  flex-direction: row;
  gap: 5px;
}
.calendar_container {
  padding: .5rem;
  position: absolute;
  z-index: 10;
  display: flex;
  flex-direction: column;
  background-color: var(--button-hover-bg);
  border-radius: 10px;
}

.calendar_display {
  background-color: var(--background-color);
  border-radius: 10px;

  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(7, auto);
}



</style>