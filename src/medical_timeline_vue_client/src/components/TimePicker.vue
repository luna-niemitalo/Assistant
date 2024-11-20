<template>
  <div id="timePicker"
       @click="$emit('close')"/>
  <div class="input-wrapper">
    <div class="header">
      <svg class="clock-lines" xmlns="http://www.w3.org/2000/svg" :width="250" :height="250" viewBox="0 0 250 250">
        <line
            v-if="selectedPosition"
            :x1="center.x"
            :y1="center.y"
            :x2="selectedPosition.x"
            :y2="selectedPosition.y"
            class="selected-line"
        />
        <line
            v-if="hoveredPosition"
            :x1="center.x"
            :y1="center.y"
            :x2="hoveredPosition.x"
            :y2="hoveredPosition.y"
            class="hovered-line"
        />
      </svg>
      <div class="hourSelector"
           v-if="display == 'hourSelector'">
        <div class="time_selector pm">
          <div
              class="selectable"
              :class="selectedClass(hour)"
              v-for="hour in pm_hours"
              :key="hour.id"
              :id="String(hour.id)"
              :ref="String('hour' + hour.id)"
              @click="selectHour(hour)"
          >
            {{ hour.label }}
          </div>
        </div>

        <div class="time_selector am">
          <div
              class="selectable"
              :class="selectedClass(hour)"
              v-for="hour in am_hours"
              :key="hour.id"
              :ref="String('hour' + hour.id)"
              :id="String(hour.id)"
              @click="selectHour(hour)"
          >
            {{ hour.label }}
          </div>
        </div>
      </div>
      <div
          class="time_selector minutes"
          v-if="display == 'minuteSelector'"
      >
        <div
            class="selectable"
            :class="selectedClass(min)"
            v-for="min in min_display"
            :key="min.id"
            :ref="String('min' + min.id)"
            :id="String(min.id)"
            @click="selectMinute(min)"
        >
          {{ min.label }}
        </div>
      </div>
      <div
          class="time_selector test"
          v-if="display == 'testSelector'"
      >
        <div
            class="selectable"
            :class="selectedClass(min)"
            v-for="min in min_display"
            :key="min.id"
            :ref="String('min' + min.id)"
            :id="String(min.id)"
            @click="selectMinute(min)"
        >
          {{ min.label }}
        </div>
      </div>
    </div>
    <div class="time_display">
      <div>
        <div class="selectable" @click.prevent.stop="showHourSelector = true">
          {{ internal_status.selectedHour?.label }}
        </div>
        <ScrollList v-if="showHourSelector"
                    :items="internal_status.hours"
                    :value="internal_status.selectedHour"
                    v-model="internal_status.selectedHour"
                    @change="showHourSelector = false"
                    @close="showHourSelector = false"
        />
      </div>
      /
      <div>
        <div class="selectable" @click.prevent.stop="showMinuteSelector = true">
          {{ internal_status.selectedMinute?.label }}
        </div>
        <ScrollList v-if="showMinuteSelector"
                    :items="internal_status.minutes"
                    :value="internal_status.selectedMinute"
                    v-model="internal_status.selectedMinute"
                    @change="showMinuteSelector = false"
                    @close="showMinuteSelector = false"
        />
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent, type PropType} from 'vue'
import ScrollList, {type IScrollListItem} from "@/components/ScrollList.vue";
import type {TimeSelection} from "@/components/DatePicker.vue";


type DataTypings = {
  internal_status: TimeSelection;
  showHourSelector: boolean;
  showMinuteSelector: boolean;
  closestElement: {
    element: HTMLElement | null,
    distance: number,
  };
  selectedElement: HTMLElement | null;
  display: 'hourSelector' | 'minuteSelector' | 'none' | 'testSelector';
}

export default defineComponent({
  name: "TimePicker",
  components: {ScrollList},
  emits: ['update:modelValue', 'change', 'close'],
  props: {
    timeSelection: {
      type: Object as PropType<TimeSelection>,
      required: true,
    }
  },
  data(): DataTypings {
    return {
      internal_status: this.timeSelection,
      showHourSelector: false,
      showMinuteSelector: false,
      closestElement: {
        element: null,
        distance: Infinity,
      },
      selectedElement: null,
      display: 'testSelector'
    }
  },
  created() {
    document.addEventListener('mousemove', this.onmousemove)
    document.addEventListener('click', this.documentClick)
  },
  beforeUnmount() {
    document.removeEventListener('mousemove', this.onmousemove)
    document.removeEventListener('click', this.documentClick)
  },
  methods: {
    documentClick() {
      if (this.display === 'hourSelector') {
        console.log(this.closestElement)
        const hour = this.internal_status.hours.find(h => h.id === Number(this.closestElement.element?.id));
        this.internal_status.selectedHour = {
          id: hour?.id ?? 0,
          label: hour?.label ?? 0,
        }
        this.submitUpdate();
      }
      if (this.display ==='minuteSelector') {
        const minute = this.internal_status.minutes.find(m => m.id === Number(this.closestElement.element?.id));
        this.internal_status.selectedMinute = {
          id: minute?.id?? 0,
          label: minute?.label?? 0,
        }
        this.submitUpdate();
      }
    },
    selectHour(hour: IScrollListItem) {
      console.log(hour)
      this.internal_status.selectedHour = hour;
      this.submitUpdate();
    },
    selectMinute(min: IScrollListItem) {
      this.internal_status.selectedMinute = this.internal_status.minutes[min.id];
      this.submitUpdate();
    },
    selectedClass(input: IScrollListItem) {
      return this.internal_status.selectedMinute?.id === input.id ? 'selected' : ''
    },
    submitUpdate() {
      this.showHourSelector = false;
      this.showMinuteSelector = false;
      this.$emit('update:modelValue', this.internal_status)
      this.$emit('change', this.internal_status)
    },
    getElementCenter(element: HTMLElement) {
      const rect = element.getBoundingClientRect();
      const x = rect.left + rect.width / 2;
      const y = rect.top + rect.height / 2;
      const svgRect = document.querySelector('.header')?.getBoundingClientRect();
      if (!svgRect) return null;
      return {
        x: x - svgRect.left,
        y: y - svgRect.top,
      };
    },

    onmousemove(event: MouseEvent) {
      if (this.display == 'hourSelector') {
        const target = event.target as HTMLElement;
        if (target.classList.contains('selectable')) {
          for (const hour of this.internal_status.hours) {
            const hourElement = this.$refs['hour' + hour.label] as HTMLElement[];
            const element = hourElement[0];
            if (element) {
              element.classList.remove('nearby');
            }
          }
          this.closestElement = {
            element: target,
            distance: 0,
          };
          return;
        }

        const x = event.clientX;
        const y = event.clientY;
        this.closestElement = {
          element: null,
          distance: Infinity,
        }
        for (const hour of this.internal_status.hours) {
          const hourElement = this.$refs['hour' + hour.label] as HTMLElement[];
          const element = hourElement[0];
          if (element) {
            const rect = element.getBoundingClientRect();
            const distance = Math.sqrt((x - rect.left) ** 2 + (y - rect.top) ** 2);
            if (distance < this.closestElement.distance) {
              this.closestElement = {
                element,
                distance,
              }
            }
            if (this.internal_status.selectedHour?.id === hour.id) {
              this.selectedElement = element;
            }
            element.classList.remove('nearby');
          }
        }
        if (this.closestElement.element) {
          this.closestElement.element.classList.add('nearby');
        }
      }
      if (this.display == 'minuteSelector') {
        const target = event.target as HTMLElement;
        if (target.classList.contains('selectable')) {
          for (const min of this.internal_status.minutes) {
            const minElement = this.$refs['min' + min.id] as HTMLElement[];
            const element = minElement[0];
            if (element) {
              element.classList.remove('nearby');
            }
          }
          this.closestElement = {
            element: target,
            distance: 0,
          };
          return;
        }

        const x = event.clientX;
        const y = event.clientY;
        this.closestElement = {
          element: null,
          distance: Infinity,
        }
        for (const min of this.internal_status.minutes) {
          const minElement = this.$refs['min' + min.id] as HTMLElement[];
          const element = minElement[0];
          if (element) {
            const rect = element.getBoundingClientRect();
            const distance = Math.sqrt((x - rect.left) ** 2 + (y - rect.top) ** 2);
            if (distance < this.closestElement.distance) {
              this.closestElement = {
                element,
                distance,
              }
            }
            if (this.internal_status.selectedMinute?.id === min.id) {
              this.selectedElement = element;
            }
            element.classList.remove('nearby');
          }
        }
        if (this.closestElement.element) {
          this.closestElement.element.classList.add('nearby');
        }
      }
    },

  },
  computed: {
    am_hours: function () {
      return this.internal_status.hours.filter(hour => hour.id < 12)
    },
    pm_hours: function () {
      return this.internal_status.hours.filter(hour => hour.id >= 12)
    },
    min_display: function () {
      return this.internal_status.minutes.map(min => ({
        id: min.id,
        label: min.id % 5 ? '.' : min.label,
      }));
    },
    center() {
      // Center of the clock SVG
      return {x: 110, y: 110};
    },
    selectedPosition() {
      if (!this.selectedElement) return null;
      return this.getElementCenter(this.selectedElement);
    },
    hoveredPosition() {
      if (!this.closestElement.element) return null;
      return this.getElementCenter(this.closestElement.element);
    }
  },
  watch: {
    timeSelection: {
      deep: true,
      handler(newVal) {
        this.internal_status = newVal;
      }
    }
  }
})
</script>
<style scoped lang="scss">
@import "CircleMixin";

.selectable {
  padding: 5px;
  transition: unset;

  &:hover {
    outline: solid 1px var(--accent-color);
  }

  &.nearby {
    outline: solid 1px var(--accent-color);
  }
}

.clock-lines {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;

  .selected-line {
    stroke: var(--accent-color);
    stroke-width: 2px;
  }

  .hovered-line {
    stroke: var(--text-color);
    stroke-width: 1px;
    stroke-dasharray: 5, 5;
    transition: stroke 0.5s ease;
  }
}

#timePicker {
  position: fixed;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9;
  top: 0;
  left: 0;
}

.time_display {
  display: flex;
  flex-direction: row;
  gap: 5px;
  align-self: center;
  font-size: xx-large;
}

.input-wrapper {
  padding: .5rem;
  margin: .5rem;
  position: absolute;
  z-index: 10;
  display: flex;
  flex-direction: column;
  background-color: var(--button-hover-bg);
}

.header {
  background-color: var(--background-color);
  border-radius: 10px;
  //padding: 1rem;
  position: relative;

  width: 250px;
  height: 250px;

  .time_selector {
    left: 50%;
    transform: translate(-50%, -50%);
    top: 50%;

    &.am {
      @include on-circle($item-count: 12, $circle-size: 150px, $item-size: 30px);
      position: absolute;
    }

    &.pm {
      @include on-circle($item-count: 12, $circle-size: 200px, $item-size: 30px);
      position: absolute;
    }


    &.minutes {
      @include on-circle($item-count: 60, $circle-size: 200px, $item-size: 30px);
      position: absolute;
    }

  }
}


</style>