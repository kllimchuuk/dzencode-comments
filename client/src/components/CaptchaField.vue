<script setup>
import { ref, onMounted } from "vue";
import { fetchCaptcha } from "../api/captcha";

const token = defineModel("token");
const answer = defineModel("answer");
const image = ref("");

async function refresh() {
  const data = await fetchCaptcha();
  token.value = data.token;
  image.value = data.image;
  answer.value = "";
}

defineExpose({ refresh });

onMounted(refresh);
</script>

<template>
  <div class="captcha-field">
    <div class="captcha-row">
      <img :src="image" alt="captcha" class="captcha-image" />
      <button
        type="button"
        class="captcha-refresh"
        title="Refresh"
        @click="refresh"
      >
        ↻
      </button>
    </div>
    <input
      v-model="answer"
      type="text"
      class="captcha-input"
      placeholder="Enter the code above"
    />
  </div>
</template>

<style scoped>
.captcha-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.captcha-row {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.captcha-image {
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.captcha-refresh {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.2rem;
  height: 2.2rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font-size: 1.1rem;
  color: var(--text);
  cursor: pointer;
  transition: background 0.15s;
}

.captcha-refresh:hover {
  background: var(--bg);
}

.captcha-input {
  max-width: 240px;
  padding: 0.5rem 0.65rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font: inherit;
  color: var(--text);
  transition:
    border-color 0.15s,
    box-shadow 0.15s;
}

.captcha-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}
</style>
