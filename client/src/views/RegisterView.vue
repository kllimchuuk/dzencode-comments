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
    <div class="auth-card">
      <h2>Register</h2>
      <form class="auth-form" @submit.prevent="submit">
        <input v-model.trim="form.username" placeholder="Username" />
        <input v-model.trim="form.email" type="email" placeholder="E-mail" />
        <input v-model="form.password" type="password" placeholder="Password" />
        <button type="submit">Register</button>
        <small v-if="error" class="auth-error">{{ error }}</small>
      </form>
      <p class="auth-alt">
        Have an account? <RouterLink to="/login">Login</RouterLink>
      </p>
    </div>
  </section>
</template>
