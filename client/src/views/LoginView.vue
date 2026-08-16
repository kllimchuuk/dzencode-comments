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
    <div class="auth-card">
      <h2>Login</h2>
      <form class="auth-form" @submit.prevent="submit">
        <input v-model.trim="form.username" placeholder="Username" />
        <input v-model="form.password" type="password" placeholder="Password" />
        <button type="submit">Login</button>
        <small v-if="error" class="auth-error">{{ error }}</small>
      </form>
      <p class="auth-alt">
        No account? <RouterLink to="/register">Register</RouterLink>
      </p>
    </div>
  </section>
</template>
