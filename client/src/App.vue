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
        <button type="button" class="btn-ghost" @click="auth.logout">
          Logout
        </button>
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
  position: sticky;
  top: var(--space-2);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
  padding: var(--space-3) var(--space-4);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.brand {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
}

.brand:hover {
  text-decoration: none;
}

.auth-nav {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  font-size: 0.9rem;
}

.auth-user {
  font-weight: 600;
}

.btn-ghost {
  padding: 0.35rem 0.8rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font: inherit;
  color: var(--text);
  cursor: pointer;
  transition: background 0.15s;
}

.btn-ghost:hover {
  background: var(--bg);
}
</style>
