<template>
  <div class="form">
    <h2>Add New Event</h2>
    <BaseTextInput label="Title" v-model="title"/>
    <BaseNumberInput label="Severity" v-model.number="severity" :min="1" :max="10" :step="0.1" :value="severity"/>
    <BaseTextInput v-model="category" label="category" />

    <RadioField v-model="timeType" :options="['at', 'around', 'between']" label="Timing type"/>


    <DatePicker v-show="timeType == 'at'" v-model="date" label="Timestamp" />
    <RadioField v-show="timeType == 'around'" v-model="around" :options="['morning', 'noon', 'evening', 'night']" label="Around"/>
    <DatePicker v-show="timeType == 'between'" v-model="date" label="Start" />
    <DatePicker v-show="timeType == 'between'" v-model="date" label="End" />

    <TagList :tags="tags" v-model="pickedTags"/>
    <BaseButton v-model="symptom" :toggle="true" label="Symptom" size="small" icon-size="medium" />
    <BaseTextArea v-model="notes" label="Notes" />

    <BaseButton
        label="Add Event"
        type="submit"
        :disabled="!title || submittedSuccessfully !== undefined"
        :success="submittedSuccessfully"
        size="small"
        icon-size="medium"
        @customClick="handleSubmit"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import {addEvent, type EventData, getTagsMapping} from '@/api/medicalTrackerApi';
import {type ITag} from '@/components/Tag.vue';
import BaseTextInput from "@/components/BaseTextInput.vue";
import BaseNumberInput from "@/components/BaseNumberInput.vue";
import BaseTextArea from "@/components/BaseTextArea.vue";
import BaseButton from "@/components/BaseButton.vue";
import TagList from "@/components/TagList.vue";
import RadioField from "@/components/RadioField.vue";
import DatePicker from "@/components/DatePicker.vue";

export interface dataTypings {
  title: string;
  severity: number;
  symptom: boolean;
  category: string;
  notes: string;
  tags: ITag[]; // populated in mounted hook from API call
  pickedTags: 0;
  submittedSuccessfully?: boolean;
  date: Date;
  start?: Date;
  end?: Date;
  around?: 'morning' | 'noon' | 'evening' | 'night';
  timeType?: 'at' | 'around' | 'between';
}
export default defineComponent({
  name: 'AddEventForm',

  components: {DatePicker, RadioField, TagList, BaseButton, BaseTextArea, BaseNumberInput, BaseTextInput },
  data() {
    return {
      title: '',
      severity: 3,
      symptom: false,
      category: '',
      notes: '',
      tags: [],
      pickedTags: 0,
      submittedSuccessfully: undefined,
      date: new Date(),
      start: undefined,
      end: undefined,
      timeType: undefined,
    } as dataTypings;
  },
  mounted: function () {
    const tags = getTagsMapping();
    tags.then((result: {[key: string]: string}) => {
      console.log("Tags fetched from API: ", result);
      console.log(Object.keys(result));
      const keys = Object.keys(result);
      keys.forEach((tag: string) => {
        this.tags.push({name: result[tag], key: Number(tag), selected: false  });
      })

      console.log(this.tags);
    })
  },
  computed: {
    eventData: function (): EventData {
      return {
        user_id: 1,
        event_type: 'at',
        title: this.title,
        severity: this.severity,
        symptom: this.symptom,
        category: this.category,
        notes: this.notes,
        tags: this.pickedTags,
        timestamp: new Date().getTime(),
      }
    }
  },
  methods: {
    handleSubmit: async function () {
      if (this.submittedSuccessfully !== undefined) return;
      console.log("submit");
      try {
        const response = await addEvent(this.eventData);
        console.log('Event added successfully:', response);
        this.submittedSuccessfully = true;
      } catch (error) {
        console.error('Error adding event:', error);
        this.submittedSuccessfully = false;
      }

    }
  },

});
</script>

<style scoped lang="scss">
.form {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  flex-grow: 1;
  gap: 20px;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
}


input {
  align-self: baseline;
  height: 4rem;
  padding-top: 25px;
  background-color: var(--background-color);
  color: var(--text-color);
}
</style>
