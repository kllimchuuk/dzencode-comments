<script setup>
import { reactive, ref } from "vue";
import CaptchaField from "./CaptchaField.vue";

const USER_NAME_RE = /^[A-Za-z0-9]+$/;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const form = reactive({
  user_name: "",
  email: "",
  home_page: "",
  text: "",
  captchaToken: "",
  captchaAnswer: "",
});

const errors = ref({});

function isValidUrl(value) {
  try {
    new URL(value);
    return true;
  } catch {
    return false;
  }
}

function validate() {
  const found = {};
  if (!form.user_name) found.user_name = "User name is required.";
  else if (!USER_NAME_RE.test(form.user_name))
    found.user_name = "Only Latin letters and digits are allowed.";
  if (!form.email) found.email = "E-mail is required.";
  else if (!EMAIL_RE.test(form.email)) found.email = "Enter a valid e-mail.";
  if (form.home_page && !isValidUrl(form.home_page))
    found.home_page = "Enter a valid URL.";
  if (!form.text.trim()) found.text = "Text is required.";
  if (!form.captchaAnswer) found.captchaAnswer = "Captcha answer is required.";
  return found;
}

function handleSubmit() {
  errors.value = validate();
}
</script>

<template>
  <form class="comment-form" novalidate @submit.prevent="handleSubmit">
    <label class="field">
      <span>User Name</span>
      <input v-model.trim="form.user_name" type="text" />
      <small v-if="errors.user_name" class="error">{{
        errors.user_name
      }}</small>
    </label>

    <label class="field">
      <span>E-mail</span>
      <input v-model.trim="form.email" type="email" />
      <small v-if="errors.email" class="error">{{ errors.email }}</small>
    </label>

    <label class="field">
      <span>Home page</span>
      <input v-model.trim="form.home_page" type="url" />
      <small v-if="errors.home_page" class="error">{{
        errors.home_page
      }}</small>
    </label>

    <label class="field">
      <span>Text</span>
      <textarea v-model="form.text" rows="4"></textarea>
      <small v-if="errors.text" class="error">{{ errors.text }}</small>
    </label>

    <CaptchaField
      v-model:token="form.captchaToken"
      v-model:answer="form.captchaAnswer"
    />
    <small v-if="errors.captchaAnswer" class="error">
      {{ errors.captchaAnswer }}
    </small>

    <button type="submit" class="submit-btn">Add comment</button>
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

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.85rem;
}

.field input,
.field textarea {
  padding: 0.4rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font: inherit;
}

.error {
  color: #dc2626;
}

.submit-btn {
  align-self: flex-start;
  padding: 0.45rem 1.1rem;
  border: none;
  border-radius: 4px;
  background: #2563eb;
  color: #fff;
  font: inherit;
  cursor: pointer;
}
</style>
