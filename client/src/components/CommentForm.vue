<script setup>
import { reactive } from "vue";
import CaptchaField from "./CaptchaField.vue";

const form = reactive({
  captchaToken: "",
  captchaAnswer: "",
});
</script>

<template>
  <form class="comment-form">
    <CaptchaField
      v-model:token="form.captchaToken"
      v-model:answer="form.captchaAnswer"
    />
  </form>
</template>

<style scoped>
.comment-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  margin-bottom: 1.25rem;
  background: #fff;
  border: 1px solid #e2e4e8;
  border-radius: 6px;
}
</style>
