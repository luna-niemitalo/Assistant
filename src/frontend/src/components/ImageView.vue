<template>
  <img
    class="image"
    v-if="image"
    :src="image.data"
    :alt="image.name"
    :key="image_stump.file_id"
  />
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { CustomImage } from "./ChatMessage.vue";

type ServerImage_stump = {
  file_id: string;
  detail: "auto" | "low" | "high";
};

type Data = {
  image?: CustomImage;
  url: string;
};

interface ServerImage {
  id: string;
  bytes: number;
  created_at: number;
  filename: string;
  object: string;
  purpose: string;
  status: string;
  status_details: null;
  data: string;
}

export default defineComponent({
  data(): Data {
    return {
      image: undefined,
      url: "http://127.0.0.1:5000/api",
    };
  },
  props: {
    image_stump: {
      type: Object as () => ServerImage_stump,
      required: true,
    },
  },
  mounted() {
    this.load_image(this.image_stump);
  },
  methods: {
    load_image: async function (image: ServerImage_stump) {
      try {
        const response = await fetch(
          this.url + "/open_ai_image?image_id=" + image.file_id
        );

        if (!response.ok) {
          console.error("Failed to load image");
          return;
        }
        const data: ServerImage = await response.json();
        console.log(data);
        this.image = {
          data: this.createBlobUrl(data),
          lastModified: data.created_at,
          name: data.filename,
          webkitRelativePath: "",
          size: data.bytes,
          type: data.purpose,
        };
      } catch (error) {
        console.error("Failed to load image: " + error);
        return;
      }
    },
    createBlobUrl(src: ServerImage) {
      const b64toBlob = (
        b64Data: string,
        contentType = "",
        sliceSize = 512
      ) => {
        const byteCharacters = atob(b64Data);
        const byteArrays = [];

        for (
          let offset = 0;
          offset < byteCharacters.length;
          offset += sliceSize
        ) {
          const slice = byteCharacters.slice(offset, offset + sliceSize);

          const byteNumbers = new Array(slice.length);
          for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
          }

          const byteArray = new Uint8Array(byteNumbers);
          byteArrays.push(byteArray);
        }

        return new Blob(byteArrays, { type: contentType });
      };
      const blob = b64toBlob(src.data, "image/png");
      console.log(src);
      if (!src) return;
      return URL.createObjectURL(blob);
    },
  },
});
</script>

<style scoped lang="scss"></style>
