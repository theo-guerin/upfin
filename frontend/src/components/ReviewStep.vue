<script setup lang="ts">
import { LoaderCircleIcon } from "@lucide/vue";
import { Button } from "@ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@ui/card";

defineProps<{
  fileName: string;
  name: string;
  year: number;
  submitting: boolean;
}>();

const emit = defineEmits<{
  (e: "back"): void;
  (e: "submit"): void;
}>();
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-semibold">Review</h2>
      <Button variant="ghost" @click="emit('back')">Back</Button>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>{{ name }} ({{ year }})</CardTitle>
      </CardHeader>
      <CardContent>
        <p class="break-all text-sm text-muted-foreground">File: {{ fileName }}</p>
      </CardContent>
    </Card>

    <Button class="w-full" :disabled="submitting" @click="emit('submit')">
      <LoaderCircleIcon v-if="submitting" class="mr-2 size-4 animate-spin" />
      {{ submitting ? "Adding..." : "Add to library" }}
    </Button>
  </div>
</template>
