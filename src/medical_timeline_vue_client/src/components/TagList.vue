<template>
  <div class="input-wrapper">
    <span class="input-label"> {{label}}: </span>
    <div class="tags">
      <BaseButton
          size="small"
          icon-size="small"
          :toggle="true"
          v-for="tag in tags"
          :key="tag.key"
          :label="tag.name"
          v-model="tag.selected"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import './base.css';
import {type ITag} from "@/components/Tag.vue";
import BaseButton from "@/components/BaseButton.vue";

export default defineComponent({
  name: 'TagList',
  components: {BaseButton},
  props: {
    tags: {
      type: Array as PropType<ITag[]>,
      required: true
    },
    label: {
      type: String,
      default: 'Tags'
    }
  },
  watch: {
    packedTags: function () {
      this.$emit('update:modelValue', this.packedTags);
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
  gap: 5px;
  flex-wrap: wrap;
  padding-top: 40px;
}

</style>