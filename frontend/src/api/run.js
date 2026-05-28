import http from "./http";

export const runAlgorithmService = (moduleSlug, payload) => {
  const slug = String(moduleSlug || "").replaceAll("_", "-");
  return http.post("/api/algorithms/" + slug + "/run", payload);
};
