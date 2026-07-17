<script setup lang="ts">
import { ref } from "vue";
import { UploadIcon } from "@lucide/vue";

const emit = defineEmits<{
  (e: "file-selected", file: File): void;
}>();

const dragOver = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const validationError = ref("");

const MAX_SIZE = 20 * 1024 * 1024 * 1024; // 20 GB

function isValidVideo(file: File): boolean {
  if (!file.type.startsWith("video/")) {
    validationError.value = "Please select a video file.";
    return false;
  }
  if (file.size > MAX_SIZE) {
    validationError.value = "File is too large. Maximum size is 20 GB.";
    return false;
  }
  validationError.value = "";
  return true;
}

function handleFile(file: File) {
  if (isValidVideo(file)) {
    emit("file-selected", file);
  }
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) handleFile(file);
}

function onDrop(event: DragEvent) {
  dragOver.value = false;
  const file = event.dataTransfer?.files?.[0];
  if (file) handleFile(file);
}
</script>

<template>
  <div
    class="flex cursor-pointer flex-col items-center gap-4 rounded-lg border-2 border-dashed p-12 transition-colors"
    :class="dragOver ? 'border-primary bg-primary/5' : 'border-border'"
    tabindex="0"
    role="button"
    @click="fileInput?.click()"
    @keydown.enter="fileInput?.click()"
    @keydown.space.prevent="fileInput?.click()"
    @dragover.prevent="dragOver = true"
    @dragleave="dragOver = false"
    @drop.prevent="onDrop"
  >
    <UploadIcon class="size-8 text-muted-foreground" />
    <p class="text-sm text-muted-foreground">
      Drop a movie file here, or click to browse
    </p>
    <input
      ref="fileInput"
      type="file"
      accept="video/*"
      class="hidden"
      @change="onFileChange"
    >
  </div>
  <p
    v-if="validationError"
    class="mt-3 text-center text-sm text-destructive"
  >
    {{ validationError }}
  </p>
</template>
