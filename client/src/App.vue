<template>
  <header class="app-header">
    <RouterLink to="/" class="brand">Comments</RouterLink>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
.app-header {
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
</style>
