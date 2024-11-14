<template>
  <div class="form">
    <h2>Add New Event</h2>
    <BaseTextInput label="Title" v-model="title"/>
    <BaseNumberInput label="Severity (1-10)" v-model.number="severity" :min="1" :max="10" :step="0.1"/>
    <BaseTextInput v-model="category" label="category" />
    <div>
      <label>Symptom:</label>
      <input v-model="symptom" type="checkbox" />
    </div>
    <div>
      <label>Category:</label>
      <input v-model="category" required />
    </div>
    <div>
      <label>Tags:</label>
      <div class="tags">
        <TagComponent v-for="tag in tags" :key="tag.key" :tag="tag" @click="handleTagUpdate(tag)"/>
      </div>
    </div>
    <div>
      <label>Notes:</label>
      <textarea v-model="notes"></textarea>
    </div>
    <button type="submit" @click="handleSubmit">Add Event</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import {addEvent, getTagsMapping} from '@/api/medicalTrackerApi';
import TagComponent, {type ITag} from '@/components/Tag.vue';
import FieldComponent from "@/components/FieldComponent.vue";
import BaseTextInput from "@/components/BaseTextInput.vue";
import BaseNumberInput from "@/components/BaseNumberInput.vue";

export interface dataTypings {
  title: string;
  severity: number;
  symptom: boolean;
  category: string;
  notes: string;
  tags: ITag[]; // populated in mounted hook from API call
}
export default defineComponent({
  name: 'AddEventForm',

  components: {BaseNumberInput, BaseTextInput, FieldComponent, TagComponent },
  data() {
    return {
      title: '',
      severity: 3,
      symptom: false,
      category: '',
      notes: '',
      tags: [] // populated in mounted hook from API call
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
  methods: {
    handleTagUpdate: function (tag: ITag) {
      tag.selected =!tag.selected;
    },
    handleSubmit: async function () {
      console.log("submit");
      try {
        //const response = await addEvent();
        //console.log('Event added successfully:', response);
      } catch (error) {
        console.error('Error adding event:', error);
      }

    }
  },
  computed: {
    selectedTags: function () {
      return this.tags.filter((tag: ITag) => tag.selected);
    },
    packedTags: function () {
      if (this.selectedTags.length === 0) return 0;
      return this.selectedTags.map(t => t.key).reduce((acc, tag) => {
        return acc | tag;
      })
    }
  }
});
</script>

<style scoped lang="scss">
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
}
</style>
