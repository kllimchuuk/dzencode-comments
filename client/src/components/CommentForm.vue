<script setup>
import { reactive, ref, nextTick } from "vue";
import { createComment, previewComment } from "../api/comments";
import { useCommentsStore } from "../stores/comments";
import CaptchaField from "./CaptchaField.vue";

const props = defineProps({ parent: { type: Number, default: null } });
const emit = defineEmits(["created"]);

const store = useCommentsStore();

const USER_NAME_RE = /^[A-Za-z0-9]+$/;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"];
const MAX_TEXT_SIZE = 100 * 1024;

const form = reactive({
  user_name: "",
  email: "",
  home_page: "",
  text: "",
  captchaToken: "",
  captchaAnswer: "",
});

const errors = ref({});
const textarea = ref(null);
const previewHtml = ref(null);
const previewError = ref("");
const file = ref(null);
const fileError = ref("");
const submitError = ref("");
const captcha = ref(null);
const fileInput = ref(null);

function isValidUrl(value) {
  try {
    new URL(value);
    return true;
  } catch {
    return false;
  }
}

function isValidXhtml(text) {
  const doc = new DOMParser().parseFromString(
    `<div>${text}</div>`,
    "application/xml",
  );
  return !doc.querySelector("parsererror");
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
  else if (!isValidXhtml(form.text))
    found.text = "Invalid HTML: check that all tags are closed.";
  if (!form.captchaAnswer) found.captchaAnswer = "Captcha answer is required.";
  return found;
}

function wrap(tag) {
  const el = textarea.value;
  const start = el.selectionStart;
  const end = el.selectionEnd;
  const selected = form.text.slice(start, end);
  const open = tag === "a" ? '<a href="" title="">' : `<${tag}>`;
  const close = `</${tag}>`;
  form.text =
    form.text.slice(0, start) + open + selected + close + form.text.slice(end);
  nextTick(() => {
    el.focus();
    el.setSelectionRange(
      start + open.length,
      start + open.length + selected.length,
    );
  });
}

function isAllowedFile(selected) {
  if (IMAGE_TYPES.includes(selected.type)) return true;
  return (
    selected.name.toLowerCase().endsWith(".txt") &&
    selected.size <= MAX_TEXT_SIZE
  );
}

function onFile(event) {
  fileError.value = "";
  const selected = event.target.files[0];
  if (!selected) {
    file.value = null;
    return;
  }
  if (isAllowedFile(selected)) file.value = selected;
  else {
    file.value = null;
    fileError.value = "Only JPG/PNG/GIF images or a .txt file (<=100KB).";
  }
}

async function preview() {
  previewError.value = "";
  try {
    previewHtml.value = await previewComment(form.text);
  } catch {
    previewHtml.value = null;
    previewError.value = "Cannot preview — check that your HTML is valid.";
  }
}

function resetForm() {
  form.user_name = "";
  form.email = "";
  form.home_page = "";
  form.text = "";
  form.captchaAnswer = "";
  file.value = null;
  fileError.value = "";
  previewHtml.value = null;
  errors.value = {};
  if (fileInput.value) fileInput.value.value = "";
  captcha.value?.refresh();
}

async function handleSubmit() {
  errors.value = validate();
  if (Object.keys(errors.value).length) return;
  submitError.value = "";
  try {
    await createComment({
      user_name: form.user_name,
      email: form.email,
      home_page: form.home_page,
      text: form.text,
      captcha_token: form.captchaToken,
      captcha_answer: form.captchaAnswer,
      parent: props.parent,
      file: file.value,
    });
    resetForm();
    await store.load();
    emit("created");
  } catch (error) {
    submitError.value = error.response?.data?.message ?? "Failed to submit.";
    captcha.value?.refresh();
  }
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

    <div class="field">
      <span>Text</span>
      <div class="toolbar">
        <button type="button" @click="wrap('i')">[i]</button>
        <button type="button" @click="wrap('strong')">[strong]</button>
        <button type="button" @click="wrap('code')">[code]</button>
        <button type="button" @click="wrap('a')">[a]</button>
      </div>
      <textarea ref="textarea" v-model="form.text" rows="4"></textarea>
      <small v-if="errors.text" class="error">{{ errors.text }}</small>
    </div>

    <label class="field">
      <span>Attachment (image or .txt)</span>
      <input
        ref="fileInput"
        type="file"
        accept="image/jpeg,image/png,image/gif,.txt"
        @change="onFile"
      />
      <small v-if="fileError" class="error">{{ fileError }}</small>
    </label>

    <CaptchaField
      ref="captcha"
      v-model:token="form.captchaToken"
      v-model:answer="form.captchaAnswer"
    />
    <small v-if="errors.captchaAnswer" class="error">
      {{ errors.captchaAnswer }}
    </small>

    <div class="form-actions">
      <button type="button" class="preview-btn" @click="preview">
        Preview
      </button>
      <button type="submit" class="submit-btn">Add comment</button>
    </div>

    <div v-if="previewHtml" class="preview">
      <div class="preview-label">Preview</div>
      <div class="preview-body" v-html="previewHtml"></div>
    </div>
    <small v-if="previewError" class="error">{{ previewError }}</small>
    <small v-if="submitError" class="error">{{ submitError }}</small>
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

.toolbar {
  display: flex;
  gap: 0.35rem;
}

.toolbar button {
  padding: 0.15rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #f9fafb;
  font: inherit;
  cursor: pointer;
}

.error {
  color: #dc2626;
}

.form-actions {
  display: flex;
  gap: 0.6rem;
}

.preview-btn {
  padding: 0.45rem 1.1rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #fff;
  font: inherit;
  cursor: pointer;
}

.submit-btn {
  padding: 0.45rem 1.1rem;
  border: none;
  border-radius: 4px;
  background: #2563eb;
  color: #fff;
  font: inherit;
  cursor: pointer;
}

.preview {
  padding: 0.75rem;
  background: #f9fafb;
  border: 1px dashed #d1d5db;
  border-radius: 6px;
}

.preview-label {
  margin-bottom: 0.4rem;
  color: #6b7280;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.preview-body {
  line-height: 1.5;
}
</style>
