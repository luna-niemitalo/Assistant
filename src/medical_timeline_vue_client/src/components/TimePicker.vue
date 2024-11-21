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
           v-if="display == 'hourSelector'"
           :ref="'timeDisplay'"
      >
        <div class="time_selector pm">
          <div
              class="locator"
              :style="styleConstructor(hour)"
              v-for="hour in pm_hours"
              :key="hour.id"
              :id="String(hour.id)"
              :ref="String('hour' + hour.id)"
          >
            <div
              class="selectable"
              :class="selectedClass(hour)"
              @click="selectHour(hour)"
          >
            {{ hour.label }}
          </div>
          </div>
        </div>

        <div class="time_selector am">
          <div
              class="locator"
              :style="styleConstructor(hour)"
              v-for="hour in am_hours"
              :key="hour.id"
              :ref="String('hour' + hour.id)"
              :id="String(hour.id)"
          >
            <div
                class="selectable"
                :class="selectedClass(hour)"
                @click="selectHour(hour)"
            >
              {{ hour.label }}
            </div>
          </div>
        </div>
      </div>
      <div
          class="time_selector minutes"
          v-if="display == 'minuteSelector'"
          :ref="'timeDisplay'"
      >
        <div
            class="locator"
            :style="styleConstructor(min)"
            v-for="min in minutes"
            :key="min.id"
            :ref="String('min' + min.id)"
            :id="String(min.id)"
        >
          <div class="selectable"
               :class="selectedClass(min)"
               @click="selectMinute(min)"
          >
            {{ min.clockDisplay }}
          </div>
        </div>
      </div>
    </div>
    <div class="time_display">
      <div>
        <div class="selectable" @click.prevent.stop="display = 'hourSelector'">
          {{ selectedHour?.label }}
        </div>
      </div>
      /
      <div>
        <div class="selectable" @click.prevent.stop="display = 'minuteSelector'">
          {{ selectedMinute?.label }}
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent, type PropType} from 'vue'
import ScrollList, {type IScrollListItem} from "@/components/ScrollList.vue";

interface TimeItem extends IScrollListItem {
  clockDisplay?: string;
  radius?: number;
  position?: {
    x: number;
    y: number;
  }
}

export type TimeSelection = {
  selectedHour?: IScrollListItem;
  selectedMinute?: IScrollListItem;
}


type DataTypings = {
  showHourSelector: boolean;
  showMinuteSelector: boolean;
  selectedHour?: TimeItem;
  selectedMinute?: TimeItem;
  closestItem: {
    item: TimeItem | null,
    distance: number,
  };
  display: 'hourSelector' | 'minuteSelector' | 'none' | 'testSelector';
  size: {
    width: number;
    height: number;
  };
  center: {
    x?: number;
    y?: number;
  };
}

export default defineComponent({
  name: "TimePicker",
  emits: ['update:modelValue', 'change', 'close'],
  props: {
    timeSelection: {
      type: Object as PropType<TimeSelection>,
      required: true,
    }
  },
  data(): DataTypings {
    return {
      showHourSelector: false,
      showMinuteSelector: false,
      closestItem: {
        item: null,
        distance: Infinity,
      },
      selectedHour: undefined,
      selectedMinute: undefined,
      display: 'hourSelector',
      size: {
        width: 250,
        height: 250,
      },
      center: {
        x: undefined,
        y: undefined,
      }
    }
  },
  created() {
    this.center.x = this.size.width / 2;
    this.center.y = this.size.height / 2;
    if (this.timeSelection && this.timeSelection.selectedHour) {
      this.selectedHour = this.hours.find(h => h.id === Number(this.timeSelection.selectedHour!.id));
    }
    if (this.timeSelection.selectedMinute) {
      this.selectedMinute = this.timeSelection.selectedMinute;
    }
    document.addEventListener('mousemove', this.onmousemove)
    document.addEventListener('click', this.documentClick)
  },
  beforeUnmount() {
    document.removeEventListener('mousemove', this.onmousemove)
    document.removeEventListener('click', this.documentClick)
  },
  methods: {
    documentClick(e: Event) {
      console.log(e)
      if (e.target && (e.target as HTMLElement).classList.contains('scroll_item')) return;
      if (!this.closestItem.item) return;

      if (this.display === 'hourSelector') {
        //this.selectedHour = this.hours.find(h => h.id === Number(this.closestItem.item!.id));
        this.selectHour(this.closestItem.item)
        this.submitUpdate();
      } else if (this.display === 'minuteSelector') {
        //this.selectedMinute = this.minutes.find(m => m.id === Number(this.closestItem.item!.id));
        this.selectMinute(this.closestItem.item)
        this.submitUpdate();
      }
    },
    selectHour(hour: IScrollListItem) {
      console.log(hour)
      this.selectedHour = this.hours.find(h => h.id === Number(hour.id));
      this.display = 'minuteSelector';
      this.submitUpdate();
    },
    selectMinute(min: IScrollListItem) {
      console.log(min)
      this.selectedMinute = this.minutes.find(m => m.id === Number(min.id));
      this.submitUpdate();
      this.$emit('close');
    },
    styleConstructor(input: TimeItem) {
      return {
        transform: 'translate(' + input.position?.x + 'px,' + input.position?.y + 'px)',
      };
    },
    selectedClass(input: TimeItem) {
      const classes = [];
      if (this.selectedHour?.id === input.id && this.display === 'hourSelector') {
        classes.push('selected');
      }
      if (this.selectedMinute?.id === input.id && this.display === 'minuteSelector') {
        classes.push('selected');
      }
      if (this.closestItem?.item?.id === input.id) {
        classes.push('nearby');
      }

      return classes.join(' ');
    },
    submitUpdate() {
      this.showHourSelector = false;
      this.showMinuteSelector = false;
      this.$emit('update:modelValue', this.internal_status)
      this.$emit('change', this.internal_status)
    },
    getElementCenter(item: TimeItem) {
      if (!item.position) return {x: 0, y: 0};
      return {
        x: item.position.x,
        y: item.position.y,
      }
    },

    onmousemove(event: MouseEvent) {
      const x = event.clientX;
      const y = event.clientY;
      this.closestItem = {
        item: null,
        distance: Infinity,
      }
      if (this.display == 'hourSelector') {
        const hours = this.am_hours.concat( this.pm_hours);
        for (const hour of hours) {
          const containerLocation = (this.$refs['timeDisplay'] as HTMLElement).getBoundingClientRect()
          const elementX = containerLocation.x + hour.position!.x;
          const elementY = containerLocation.y + hour.position!.y;
          const distance = Math.sqrt((x - elementX) ** 2 + (y - elementY) ** 2);

          if (distance < this.closestItem.distance) {
            this.closestItem = {
              item: hour,
              distance,
            }
          }
        }
      }

      if (this.display == 'minuteSelector' || this.display == 'testSelector') {

        for (const min of this.minutes) {
          const containerLocation = (this.$refs['timeDisplay'] as HTMLElement).getBoundingClientRect()
          const elementX = containerLocation.x + min.position!.x;
          const elementY = containerLocation.y + min.position!.y;
          const distance = Math.sqrt((x - elementX) ** 2 + (y - elementY) ** 2);

          if (distance < this.closestItem.distance) {
            this.closestItem = {
              item: min,
              distance,
            }
          }
        }
      }
    },
    calculatePosition(value: TimeItem, index: number, array: TimeItem[]): TimeItem {
      let rot = -90;
      const angle = 360 / array.length;
      if (!this.center.x || !this.center.y) return value;
      console.log(index)
      rot = (rot + angle * index) ;
      console.log(rot)
      console.log(angle)
      const result = value;

      const radius = value.radius || 100;

      result.position = {
        x: this.center.x + Math.cos(rot * Math.PI / 180) * radius,
        y: this.center.y + Math.sin(rot * Math.PI / 180) * radius,
      };
      console.log(result.position)
      return result;
    }
  },
  computed: {
    minutes: function () {
      const minutes: TimeItem[] = Array.from({length: 60}, (_, i) => ({
        id: i,
        clockDisplay: String(i % 5 ? '.' : i),
        label: i.toString().padStart(2, '0'),
      }));
      return minutes.map(this.calculatePosition);
    },
    hours: function () {
      return this.am_hours.concat(this.pm_hours);
    },
    am_hours: function () {
      const hours = Array.from({length: 24}, (_, i) => ({
        id: i,
        label: i.toString().padStart(2, '0'),
      }));
      const filteredHours = hours.filter(hour => hour.id < 12);
      const added_radius = filteredHours.map(hour => ({...hour, radius: 70 }));
      return added_radius.map(this.calculatePosition)
    },
    pm_hours: function () {
      const hours = Array.from({length: 24}, (_, i) => ({
        id: i,
        label: i.toString().padStart(2, '0'),
      }));
      const filteredHours = hours.filter(hour => hour.id >= 12);
      const added_radius = filteredHours.map(hour => ({...hour, radius: 110 }));
      return added_radius.map(this.calculatePosition)
    },

    internal_status() {
      return {
        selectedHour: this.selectedHour? this.selectedHour : this.timeSelection.selectedHour,
        selectedMinute: this.selectedMinute? this.selectedMinute : this.timeSelection.selectedMinute,
      }
    },
    selectedPosition() {
      console.log(this.selectedMinute)
      if (this.display === 'hourSelector' && this.selectedHour) {
        return this.getElementCenter(this.selectedHour);
      }
      if (this.display === 'minuteSelector' && this.selectedMinute) {
        return this.getElementCenter(this.selectedMinute);
      }
      return {
        x: 0,
        y: 0,
      }
    },
    hoveredPosition() {
      if (!this.closestItem.item) return null;
      return this.getElementCenter(this.closestItem.item);
    },
  },
})
</script>
<style scoped lang="scss">
@import "CircleMixin";

.selectable {
  padding: 5px;
  transition: unset;


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
    .locator {
      margin: unset;
      padding: unset;
      border: unset;
      width: 0;
      height: 0;
      line-height: 0;

      .selectable {
        font-size: 1rem;
        cursor: pointer;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        line-height: 1.5;
        transition: border-color 0.5s ease;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        &:hover {
          background-color: transparent;
          outline: solid 1px var(--text-color);
        }

        &.nearby {
          background-color: transparent;
          outline: solid 1px var(--text-color);
        }


      }
    }

  }
}


</style>