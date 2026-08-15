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
    <input v-model="answer" type="text" placeholder="Enter the code above" />
  </div>
</template>

<style scoped>
.captcha-field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.captcha-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.captcha-image {
  border: 1px solid #e2e4e8;
  border-radius: 4px;
}

.captcha-refresh {
  padding: 0.25rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #fff;
  font-size: 1rem;
  cursor: pointer;
}
</style>
