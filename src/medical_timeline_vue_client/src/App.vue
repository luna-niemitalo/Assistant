<template>
  <div id="app">
    <AddEventForm />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AddEventForm from '@/components/AddEventForm.vue';

export default defineComponent({
  name: 'App',
  components: {
    AddEventForm,
  },
});
</script>
<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
