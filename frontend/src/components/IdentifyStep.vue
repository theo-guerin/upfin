<script setup lang="ts">
import { ref } from "vue";
import { LoaderCircleIcon } from "@lucide/vue";
import { Button } from "@ui/button";
import { Card } from "@ui/card";
import { Input } from "@ui/input";
import type { MovieSearchResult, MovieSelection } from "@/types";

defineProps<{
  results: MovieSearchResult[];
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: "movie-picked", movie: MovieSelection): void;
  (e: "back"): void;
}>();

const manual = ref(false);
const manualName = ref("");
const manualYear = ref("");
const manualError = ref("");

function pick(result: MovieSearchResult) {
  emit("movie-picked", {
    name: result.Name,
    year: result.ProductionYear,
  });
}

function onSubmitManual() {
  manualError.value = "";

  if (!manualName.value) {
    manualError.value = "Please enter a movie title.";
    return;
  }

  const year = Number.parseInt(manualYear.value, 10);
  if (Number.isNaN(year) || year < 1888 || year > 2100) {
    manualError.value = "Please enter a valid year.";
    return;
  }

  emit("movie-picked", { name: manualName.value, year });
}

function onCardKeydown(event: KeyboardEvent, result: MovieSearchResult) {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    pick(result);
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-semibold">Identify your movie</h2>
      <Button variant="ghost" @click="emit('back')">Back</Button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-12">
      <LoaderCircleIcon class="size-6 animate-spin text-muted-foreground" />
    </div>

    <template v-else-if="results.length > 0 && !manual">
      <p class="text-sm text-muted-foreground">
        {{ results.length }} match{{ results.length > 1 ? "es" : "" }} found.
        Pick the correct one:
      </p>

      <div class="space-y-2">
        <Card
          v-for="result in results"
          :key="`${result.Name}-${result.ProductionYear}`"
          class="cursor-pointer overflow-hidden py-0 transition-colors hover:bg-accent"
          tabindex="0"
          role="button"
          @click="pick(result)"
          @keydown="onCardKeydown($event, result)"
        >
          <div class="flex">
            <img
              v-if="result.ImageUrl"
              :src="result.ImageUrl"
              class="h-32 w-20 shrink-0 object-cover"
              loading="lazy"
            >
            <div class="flex min-w-0 flex-1 py-4">
              <div class="min-w-0 px-4">
                <p class="truncate text-sm font-medium">{{ result.Name }}</p>
                <p class="text-xs text-muted-foreground">
                  {{ result.ProductionYear }}
                </p>
                <p
                  v-if="result.Overview"
                  class="mt-1 line-clamp-3 text-xs text-muted-foreground"
                >
                  {{ result.Overview }}
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <Button variant="link" class="px-0" @click="manual = true">
        Not in the list? Enter manually
      </Button>
    </template>

    <div v-else class="space-y-3">
      <Button
        v-if="results.length > 0"
        variant="link"
        class="px-0"
        @click="manual = false; manualError = ''"
      >
        Back to results
      </Button>
      <p class="text-sm text-muted-foreground">
        Enter the movie details manually:
      </p>
      <Input v-model="manualName" placeholder="Movie title" />
      <Input v-model="manualYear" type="number" placeholder="Year" />
      <p v-if="manualError" class="text-sm text-destructive">{{ manualError }}</p>
      <Button :disabled="!manualName || !manualYear" @click="onSubmitManual">
        Continue
      </Button>
    </div>
  </div>
</template>
