<template>
  <div :class="commentClasses">
    <div class="comment">
      <div class="comment-header">
        <span class="comment-user">{{ name }}</span>
        <span class="comment-timestamp">{{ humanReadableTimestamp }}</span>
      </div>
      <div class="comment-text" v-if="!editing" v-html="getText"></div>
      <div v-else class="comment-edit">
        <input v-model="editText" class="edit-input" />
        <font-awesome-icon icon="check" class="icon-check" />
      </div>
      <div class="comment-footer">
        <font-awesome-icon
          icon="edit"
          @click="editing = true"
          class="icon-edit"
        />
        <font-awesome-icon icon="thumbs-up" class="icon-like" />
        <font-awesome-icon icon="thumbs-down" class="icon-dislike" />
        <font-awesome-icon icon="trash" class="icon-delete" />
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import markdownit from "markdown-it";
import hljs from "highlight.js"; // https://highlightjs.org

const md = markdownit({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(str, { language: lang }).value;
    }

    return ""; // use external default escaping
  },
});

export type Message = {
  thread_id?: string;
  id: number;
  text: string;
  role: "user" | "assistant" | "system";
  timestamp?: number;
};
type Data = {
  model: Message;
  editing: boolean;
  hashMatch: boolean;
  editText: string;
};

export default defineComponent({
  components: { FontAwesomeIcon },
  data(): Data {
    return {
      model: this.message,
      editing: false,
      hashMatch: true,
      editText: "",
    };
  },
  computed: {
    getText(): string {
      const markdown = this.model.text;
      return md.render(markdown);
    },
    humanReadableTimestamp(): string {
      if (!this.model.timestamp) return "";
      return new Date(this.model.timestamp * 1000).toLocaleString();
    },
    commentClasses(): string[] {
      return [
        "comment-container",
        this.model.role === "user" ? "user-message" : "assistant-message",
        this.hashMatch ? "" : "hash-mismatch",
      ];
    },
    name(): string {
      return this.model.role === "user" ? "Luna" : "Assistant";
    },
  },
  props: {
    message: {
      type: Object as () => Message,
      required: true,
    },
  },
  mounted() {
    this.model = this.message;
  },
  watch: {
    message: function (newValue) {
      this.model = newValue;
    },
  },
});
</script>

<style scoped lang="scss">
.hash-mismatch {
  background-color: #ffcccc; /* Light red background for mismatch */
}
.comment-container {
  display: flex;
  padding: 1rem;

  &.user-message {
    justify-content: flex-end;
  }

  &.assistant-message {
    justify-content: flex-start;
  }

  .comment {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 1rem;
    max-width: 60%;
    position: relative;

    &.user-message .comment {
      background-color: #e1f5fe;
    }

    &.assistant-message .comment {
      background-color: #f1f8e9;
    }

    .comment-header {
      display: flex;
      justify-content: space-between;
      column-gap: 1rem;
      margin-bottom: 0.5rem;

      .comment-user {
        font-weight: bold;
      }

      .comment-timestamp {
        color: #999;
        font-size: 0.875rem;
      }
    }

    .comment-text {
      margin-bottom: 1rem;
    }

    .comment-edit {
      display: flex;
      align-items: center;

      .edit-input {
        flex-grow: 1;
        margin-right: 0.5rem;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 3px;
      }

      .icon-check {
        color: #4caf50;
        cursor: pointer;
      }
    }

    .comment-footer {
      display: flex;
      justify-content: flex-end;

      .icon-edit,
      .icon-like,
      .icon-dislike,
      .icon-delete {
        margin-left: 0.5rem;
        cursor: pointer;
        color: #999;

        &:hover {
          color: #333;
        }
      }
    }
  }
}
</style>
