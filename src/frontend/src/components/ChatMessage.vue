<template>
  <div :class="commentClasses">
    <div class="comment">
      <div class="comment-header">
        <span class="comment-user">{{ name }}</span>
        <span class="comment-timestamp">{{ humanReadableTimestamp }}</span>
      </div>
      <div class="comment-text" v-if="!editing" v-html="getText"></div>
      <div v-if="editing" class="comment-edit">
        <input v-model="editText" class="edit-input" />
        <font-awesome-icon icon="check" class="icon-check" />
      </div>
      <div class="images">
        <ImageView
          v-for="image in model.images"
          :key="image.file_id"
          :image_stump="image"
        />
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
import ImageView from "./ImageView.vue";
import markdownit from "markdown-it";
import hljs from "highlight.js"; // https://highlightjs.org

const md = markdownit({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
        // eslint-disable-next-line no-empty
      } catch (__) {}
    }
    return ""; // Use external default escaping
  },
});

type ServerImage_stump = {
  file_id: string;
  detail: "auto" | "low" | "high";
};

export type Message = {
  id?: number;
  text: string;
  images?: CustomImage[];
  role: "user" | "assistant" | "system";
  timestamp?: number;
};

export type CustomImage = {
  data?: string;
  lastModified: number;
  name: string;
  webkitRelativePath: string;
  size: number;
  type: string;
};

export type ServerMessage = {
  id: number;
  text: string;
  images?: ServerImage_stump[];
  role: "user" | "assistant" | "system";
  timestamp: number;
};

type Data = {
  model: ServerMessage;
  editing: boolean;
  hashMatch: boolean;
  editText: string;
};

export default defineComponent({
  components: { FontAwesomeIcon, ImageView },
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
      console.log(this.model.text);
      const markdown = this.model.text;
      return md.render(markdown);
    },
    humanReadableTimestamp(): string {
      if (!this.model.timestamp) return "";
      if (this.message.timestamp?.toString().length === 10)
        return new Date(this.model.timestamp * 1000).toLocaleString();
      return new Date(this.model.timestamp).toLocaleString();
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
      type: Object as () => ServerMessage,
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
  background-color: var(--background-color);
}
.comment-container {
  display: flex;
  padding: 1rem;

  &.user-message {
    justify-content: flex-end;
    .comment {
      background-color: var(--user-message-bg);
    }
  }

  &.assistant-message {
    justify-content: flex-start;
    .comment {
      background-color: var(--assistant-message-bg);
    }
  }

  .comment {
    border: 1px solid var(--text-color);
    border-radius: 5px;
    padding: 1rem;
    max-width: 60%;
    position: relative;

    .images {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1rem;
      .image {
        max-width: 100px;
        max-height: 100px;
        object-fit: contain;
      }
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
