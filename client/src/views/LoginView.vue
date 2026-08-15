<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();
const form = reactive({ username: "", password: "" });
const error = ref("");

async function submit() {
  error.value = "";
  try {
    await auth.login(form);
    router.push("/");
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Login failed.";
  }
}
</script>

<template>
  <section class="auth">
    <h2>Login</h2>
    <form class="auth-form" @submit.prevent="submit">
      <input v-model.trim="form.username" placeholder="Username" />
      <input v-model="form.password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
      <small v-if="error" class="error">{{ error }}</small>
    </form>
    <p>No account? <RouterLink to="/register">Register</RouterLink></p>
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
