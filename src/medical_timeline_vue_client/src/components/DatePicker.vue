<template>
  <div class="date_time">
    <div class="selectable">
      <div @click.prevent.stop="showYearSelector = true">{{ dateSelection.selectedYear?.label }}</div>
      <ScrollList v-if="showYearSelector"
                  :items="dateSelection.years"
                  :value="dateSelection.selectedYear"
                  v-model="dateSelection.selectedYear"
                  @change="handleClose"
                  @close="handleClose"
      />
    </div>
    /
    <div class="selectable">
      <div @click.prevent.stop="showMonthSelector = true">{{ dateSelection.selectedMonth?.label }}</div>
      <ScrollList v-if="showMonthSelector"
                  :items="dateSelection.months"
                  :value="dateSelection.selectedMonth"
                  v-model="dateSelection.selectedMonth"
                  @change="handleClose"
                  @close="handleClose"
      />
    </div>
    /
    <div class="selectable">
      <div @click.prevent.stop="showDaySelector = true">{{ dateSelection.selectedDay?.label }}</div>
      <ScrollList v-if="showDaySelector"
                  :items="dateSelection.days"
                  :value="dateSelection.selectedDay"
                  v-model="dateSelection.selectedDay"
                  @change="handleClose"
                  @close="handleClose"
      />
    </div>
    :
    <div class="selectable">
      <div @click="showCalendarSelector = true"> 📅︎︎</div>
        <CalendarDatePicker
            v-if="showCalendarSelector"
            :key="calendarKey"
            :dateSelection="dateSelection"
            @close="handleClose"
            @change="calendarSelectionChange"
        />
    </div>
    <div class="selectable">
      <div @click="showTimeSelector = true">{{timeDisplay}}</div>
      <TimePicker v-if="showTimeSelector" :timeSelection="timeSelection" v-model="timeSelection" @close="handleClose" />
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent} from 'vue'
import ScrollList, {type IScrollListItem} from "@/components/ScrollList.vue";
import CalendarDatePicker from "@/components/CalendarDatePicker.vue";
import TimePicker, {type TimeSelection} from "@/components/TimePicker.vue";

type DataTypings = {
  showCalendar: boolean;
  weekdays: string[];
  dateSelection: DateSelection;
  timeSelection: TimeSelection;
  showYearSelector: boolean;
  showMonthSelector: boolean;
  showDaySelector: boolean;
  showCalendarSelector: boolean;
  showTimeSelector: boolean;
  calendarKey: number;
}

export type DateSelection = {
  years: IScrollListItem[];
  months: IScrollListItem[];
  days: IScrollListItem[];
  selectedYear?: IScrollListItem;
  selectedMonth?: IScrollListItem;
  selectedDay?: IScrollListItem;
}



export default defineComponent({
  name: "DatePicker",
  components: {CalendarDatePicker, ScrollList, TimePicker},
  props: {
    value: {
      type: Date,
      default: new Date()
    },

  },
  data(): DataTypings {
    return {
      showCalendar: false,
      weekdays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
      dateSelection: {
        years: [],
        months: [],
        days: [],
        selectedYear: undefined,
        selectedMonth: undefined,
        selectedDay: undefined,
      },
      timeSelection: {
        selectedHour: undefined,
        selectedMinute: undefined,
      },
      showYearSelector: false,
      showMonthSelector: false,
      showDaySelector: false,
      showCalendarSelector: false,
      showTimeSelector: false,
      calendarKey: 0,
    }
  },
  mounted: function () {
    this.constructYears();
    this.constructMonths();
    this.constructDays();
    this.constructTime();
  },
  watch: {
    selectedDate(newDate) {
      this.$emit('update:modelValue', newDate);
    }
  },
  computed: {
    selectedDate() {
      const currentDate = this.value;
      return new Date(
          this.dateSelection?.selectedYear?.id ?? currentDate.getFullYear(),
          this.dateSelection?.selectedMonth?.id ?? currentDate.getMonth(),
          this.dateSelection?.selectedDay?.id ?? currentDate.getDate(),
          this.timeSelection.selectedHour?.id ?? currentDate.getHours(),
          this.timeSelection.selectedMinute?.id ?? currentDate.getMinutes(),
          currentDate.getSeconds(),
          currentDate.getMilliseconds(),
      )
    },
    timeDisplay() {
      if (this.timeSelection.selectedHour && this.timeSelection.selectedMinute) {
        return `${this.timeSelection.selectedHour.label}:${this.timeSelection.selectedMinute.label}`;
      }
      return '';
    }
  },
  methods: {
    handleClose() {
      this.showYearSelector = false;
      this.showMonthSelector = false;
      this.showDaySelector = false;
      this.showCalendarSelector = false;
      this.showTimeSelector = false;
      this.dateSelection.days = [];
      this.constructDays();
    },
    calendarSelectionChange(newValue: DateSelection) {
      console.log(newValue.selectedMonth?.label);
      this.dateSelection = newValue;
      this.constructDays();
      this.calendarKey++;
    },
    constructYears() {
      const currentYear = new Date().getFullYear();
      for (let i = 0; i < 200; i++) {
        if (1970 + i == currentYear) {
          this.dateSelection.selectedYear = {
            id: 1970 + i,
            label: 1970 + i
          }
        }
        this.dateSelection.years.push({
          id: 1970 + i,
          label: 1970 + i
        })
      }
    },
    constructMonths(value?: DateSelection) {
      const currentMonth = value?.selectedMonth?.id || new Date().getMonth();

      const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
      this.dateSelection.months = months.map((month, index) => {
        if (index == currentMonth) {
          this.dateSelection.selectedMonth = {
            id: index,
            label: month,
          };
        }
        return {
          id: index,
          label: month,
        };
      });
    },
    constructDays() {
      console.log("Constructing days")
      const currentYear = this.selectedDate.getFullYear();
      const currentMonth = this.selectedDate.getMonth();
      const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
      console.log(daysInMonth)
      const currentDay = this.selectedDate.getDate();
      console.log(currentDay)
      this.dateSelection.days = [];

      for (let i = 1; i <= daysInMonth; i++) {
        if (currentDay == i) {
          this.dateSelection.selectedDay = {
            id: i,
            label: i,
          };
        }
        this.dateSelection.days.push({
          id: i,
          label: i,
        });
      }
    },
    constructTime() {
      const currentHour = this.selectedDate.getHours();
      const currentMinute = this.selectedDate.getMinutes();
      this.timeSelection.selectedHour = {
        id: currentHour,
        label: currentHour < 10? `0${currentHour}` : currentHour
      };
      this.timeSelection.selectedMinute = {
        id: currentMinute,
        label: currentMinute < 10? `0${currentMinute}` : currentMinute
      };
    }

  }
})
</script>
<style scoped lang="scss">
.date_time {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}

.selectable {
  min-width: 50px;
  width: fit-content;
  display: flex;
  justify-content: center;
  flex-direction: row;
  align-items: center;
  height: 25px;
  border-radius: unset;
}

</style>