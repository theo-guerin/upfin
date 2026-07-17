<script setup lang="ts">
import { useColorMode } from "@vueuse/core";
import { ref } from "vue";
import { client } from "./lib/api";

useColorMode({
  initialValue: "dark",
});

const value = ref("");

client
  .GET("/search_movie", {
    params: { query: { filename: "The Matrix (1999).mkv" } },
  })
  .then(({ data }) => {
    value.value = JSON.stringify(data, null, 2);
  });
</script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit
    <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a>
    to read the documentation
    {{ value }}
  </p>
</template>
