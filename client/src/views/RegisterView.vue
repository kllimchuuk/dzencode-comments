<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();
const form = reactive({ username: "", email: "", password: "" });
const error = ref("");

async function submit() {
  error.value = "";
  try {
    await auth.register(form);
    router.push("/");
  } catch (err) {
    error.value = err.response?.data?.message ?? "Registration failed.";
  }
}
</script>

<template>
  <section class="auth">
    <h2>Register</h2>
    <form class="auth-form" @submit.prevent="submit">
      <input v-model.trim="form.username" placeholder="Username" />
      <input v-model.trim="form.email" type="email" placeholder="E-mail" />
      <input v-model="form.password" type="password" placeholder="Password" />
      <button type="submit">Register</button>
      <small v-if="error" class="error">{{ error }}</small>
    </form>
    <p>Have an account? <RouterLink to="/login">Login</RouterLink></p>
  </section>
</template>

<style scoped>
.auth {
  max-width: 320px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.auth-form input {
  padding: 0.45rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font: inherit;
}

.auth-form button {
  padding: 0.45rem;
  border: none;
  border-radius: 4px;
  background: #2563eb;
  color: #fff;
  font: inherit;
  cursor: pointer;
}

.error {
  color: #dc2626;
}
</style>
