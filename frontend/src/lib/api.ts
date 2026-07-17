import createClient from "openapi-fetch";
import type { paths } from "@/gen/types";

export const api = createClient<paths>({ baseUrl: "/" });

export async function submitMovie(
  file: File,
  name: string,
  year: number,
  signal?: AbortSignal,
) {
  const formData = new FormData();
  formData.append("movie", file);
  // FastAPI's OpenAPI schema types UploadFile as string, so FormData
  // doesn't match the generated body type. Encapsulated here to keep
  // the cast isolated from component logic.
  return api.POST("/submit", {
    params: { query: { name, year } },
    body: formData as never,
    signal,
  });
}
