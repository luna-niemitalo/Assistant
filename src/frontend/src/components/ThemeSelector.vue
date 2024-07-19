<template>
  <div class="theme-selector">
    <div>
      <span>Dark Mode</span>
      <font-awesome-icon
        :icon="darkMode ? 'toggle-on' : 'toggle-off'"
        @click="toggleDarkMode"
        class="dark-mode-toggle"
      />
    </div>
    <div>
      <label for="theme-select">Select Theme:</label>
      <select id="theme-select" v-model="selectedTheme" @change="applyTheme">
        <option
          v-for="(theme, index) in themes"
          :key="index"
          :value="theme.name"
        >
          {{ theme.displayName }}
        </option>
      </select>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";

interface Theme {
  name: string;
  displayName: string;
  userMessageBg: string;
  userMessageBg_dark: string;
  assistantMessageBg: string;
  assistantMessageBg_dark: string;
}

const themes: Theme[] = [
  {
    name: "purple",
    displayName: "Purple Theme",
    userMessageBg: "#f3e7ff",
    userMessageBg_dark: "#3a1c5a",
    assistantMessageBg: "#ffe7e7",
    assistantMessageBg_dark: "#1c3a5a",
  },
  {
    name: "green",
    displayName: "Green Theme",
    userMessageBg: "#b7e678",
    assistantMessageBg: "#e7f7e7",
    userMessageBg_dark: "#014421",
    assistantMessageBg_dark: "#3a5a1c",
  },
];

export default defineComponent({
  name: "ThemeSelector",
  data() {
    return {
      darkMode: false,
      selectedTheme: ref(themes[0].name),
      themes,
    };
  },
  beforeMount() {
    if (localStorage.darkMode) {
      this.darkMode = localStorage.darkMode === "true";
    }
    if (localStorage.selectedTheme) {
      this.selectedTheme = localStorage.selectedTheme;
    }
  },
  mounted() {
    this.applyTheme();
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      this.applyTheme();
    },
    applyTheme() {
      localStorage.darkMode = this.darkMode;
      localStorage.selectedTheme = this.selectedTheme;
      if (this.darkMode) {
        document.documentElement.setAttribute("data-theme", "dark");
      } else {
        document.documentElement.removeAttribute("data-theme");
      }
      const theme = themes.find((t) => t.name === this.selectedTheme);
      if (theme) {
        document.documentElement.style.setProperty(
          "--user-message-bg",
          this.darkMode ? theme.userMessageBg_dark : theme.userMessageBg
        );
        document.documentElement.style.setProperty(
          "--assistant-message-bg",
          this.darkMode
            ? theme.assistantMessageBg_dark
            : theme.assistantMessageBg
        );
      }
    },
  },
  watch: {
    selectedTheme: "applyTheme",
  },
});
</script>

<style>
.theme-selector {
  margin: 1rem;
  display: flex;
  justify-content: space-evenly;
}
:root {
  --background-color: #ffffff;
  --contrast-background-color: #f0f0f0;
  --text-color: #000000;
  --user-message-bg: #f3e7ff;
  --assistant-message-bg: #e7f7e7;
}

[data-theme="dark"] {
  --background-color: #000;
  --contrast-background-color: #151515;
  --text-color: #ddd;
  --user-message-bg: #3a1c5a;
  --assistant-message-bg: #3a5a1c;
}
#theme-select {
  margin-left: 0.5rem;
}
</style>
