<script setup>
const props = defineProps({ ordering: { type: String, required: true } });
const emit = defineEmits(["change"]);

const columns = [
  { field: "user_name", label: "User Name" },
  { field: "email", label: "E-mail" },
  { field: "created_at", label: "Date" },
];

function sortBy(field) {
  const asc = props.ordering === field;
  emit("change", asc ? `-${field}` : field);
}

function isActive(field) {
  return props.ordering === field || props.ordering === `-${field}`;
}

function indicator(field) {
  if (props.ordering === field) return "▲";
  if (props.ordering === `-${field}`) return "▼";
  return "";
}
</script>

<template>
  <div class="sort-bar">
    <span class="sort-label">Sort by</span>
    <button
      v-for="col in columns"
      :key="col.field"
      type="button"
      class="sort-col"
      :class="{ active: isActive(col.field) }"
      @click="sortBy(col.field)"
    >
      {{ col.label }}<span class="sort-arrow">{{ indicator(col.field) }}</span>
    </button>
  </div>
</template>

<style scoped>
.sort-bar {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  margin-bottom: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.sort-label {
  margin-right: var(--space-1);
  color: var(--muted);
  font-size: 0.8rem;
}

.sort-col {
  display: inline-flex;
  gap: 0.25rem;
  align-items: center;
  padding: 0.2rem 0.5rem;
  border: none;
  border-radius: 6px;
  background: none;
  font: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--muted);
  cursor: pointer;
  transition: color 0.15s;
}

.sort-col:hover {
  color: var(--text);
}

.sort-col.active {
  color: var(--accent);
}

.sort-arrow {
  font-size: 0.7rem;
}
</style>
