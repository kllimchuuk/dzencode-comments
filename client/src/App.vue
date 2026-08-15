<script setup>
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();
</script>

<template>
  <header class="app-header">
    <RouterLink to="/" class="brand">Comments</RouterLink>
    <nav class="auth-nav">
      <template v-if="auth.isAuthenticated">
        <span class="auth-user">{{ auth.username }}</span>
        <button type="button" @click="auth.logout">Logout</button>
      </template>
      <template v-else>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
      </template>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e4e8;
}

.brand {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  text-decoration: none;
}

.auth-nav {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  font-size: 0.9rem;
}

.auth-user {
  font-weight: 600;
}

.auth-nav button {
  padding: 0.3rem 0.7rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #fff;
  font: inherit;
  cursor: pointer;
}
</style>
