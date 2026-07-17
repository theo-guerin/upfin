<script setup lang="ts">
import { ref } from "vue";
import { useColorMode } from "@vueuse/core";
import { Button } from "@ui/button";
import { api, submitMovie } from "@/lib/api";
import type { MovieSearchResult, MovieSelection } from "@/types";
import IdentifyStep from "@/components/IdentifyStep.vue";
import ReviewStep from "@/components/ReviewStep.vue";
import UploadStep from "@/components/UploadStep.vue";

useColorMode({ initialValue: "dark" });

const step = ref<"upload" | "identify" | "review" | "done">("upload");
const file = ref<File | null>(null);
const results = ref<MovieSearchResult[]>([]);
const selected = ref<MovieSelection | null>(null);
const loading = ref(false);
const submitting = ref(false);
const error = ref("");
let searchAbort: AbortController | null = null;
let submitAbort: AbortController | null = null;
let searchId = 0;
let submitId = 0;

function goToUpload() {
  searchAbort?.abort();
  submitAbort?.abort();
  searchId++;
  submitId++;
  loading.value = false;
  submitting.value = false;
  file.value = null;
  step.value = "upload";
}

async function onFileSelected(f: File) {
  searchAbort?.abort();

  const id = ++searchId;
  file.value = f;
  step.value = "identify";
  loading.value = true;
  results.value = [];
  error.value = "";

  searchAbort = new AbortController();

  try {
    const { data, error: err } = await api.GET("/search_movie", {
      params: { query: { filename: f.name } },
      signal: AbortSignal.any([searchAbort.signal, AbortSignal.timeout(30_000)]),
    });
    results.value = data ?? [];

    if (err) {
      error.value = "Search failed — enter movie details manually below.";
    }
  } catch (e) {
    if (e instanceof DOMException && e.name === "AbortError") return;
    error.value = "Search failed — enter movie details manually below.";
    results.value = [];
  } finally {
    if (id === searchId) loading.value = false;
  }
}

function onMoviePicked(movie: MovieSelection) {
  selected.value = movie;
  error.value = "";
  step.value = "review";
}

async function onSubmit() {
  if (!file.value || !selected.value) return;
  submitAbort?.abort();

  const id = ++submitId;
  submitting.value = true;
  error.value = "";

  submitAbort = new AbortController();

  try {
    const { error: err } = await submitMovie(
      file.value,
      selected.value.name,
      selected.value.year,
      AbortSignal.any([submitAbort.signal, AbortSignal.timeout(120_000)]),
    );

    if (err) {
      error.value = "Upload failed. Please try again.";
      return;
    }

    step.value = "done";
  } catch (e) {
    if (e instanceof DOMException && e.name === "AbortError") return;
    error.value = "Upload failed. Please try again.";
  } finally {
    if (id === submitId) submitting.value = false;
  }
}

function reset() {
  searchAbort?.abort();
  submitAbort?.abort();
  searchId++;
  submitId++;
  step.value = "upload";
  file.value = null;
  results.value = [];
  selected.value = null;
  error.value = "";
  submitting.value = false;
}
</script>

<template>
  <main class="mx-auto max-w-lg px-4 py-16">
    <h1 class="mb-8 text-center text-2xl font-bold">Movie Uploader</h1>

    <p
      v-if="error"
      class="mb-6 rounded-lg bg-destructive/10 p-3 text-sm text-destructive"
    >
      {{ error }}
    </p>

    <UploadStep
      v-if="step === 'upload'"
      @file-selected="onFileSelected"
    />

    <IdentifyStep
      v-else-if="step === 'identify'"
      :results="results"
      :loading="loading"
      @movie-picked="onMoviePicked"
      @back="goToUpload"
    />

    <ReviewStep
      v-else-if="step === 'review'"
      :file-name="file?.name ?? ''"
      :name="selected?.name ?? ''"
      :year="selected?.year ?? 0"
      :submitting="submitting"
      @back="step = 'identify'"
      @submit="onSubmit"
    />

    <div v-else class="space-y-4 text-center">
      <p class="text-lg font-semibold text-green-600 dark:text-green-400">
        Done!
      </p>
      <p class="text-sm text-muted-foreground">
        {{ selected?.name }} ({{ selected?.year }}) has been added.
      </p>
      <Button @click="reset">Upload another</Button>
    </div>
  </main>
</template>
