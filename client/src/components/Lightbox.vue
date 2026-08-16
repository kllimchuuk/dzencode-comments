<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  attachment: { type: Object, required: true },
  open: { type: Boolean, required: true },
});
const emit = defineEmits(["close"]);

const textContent = ref("");

watch(
  () => props.open,
  async (isOpen) => {
    if (isOpen && props.attachment.kind === "text") {
      const response = await fetch(props.attachment.url);
      textContent.value = await response.text();
    }
  },
);
</script>

<template>
  <Transition name="lightbox">
    <div v-if="open" class="lightbox-overlay" @click.self="emit('close')">
      <div class="lightbox-content">
        <button type="button" class="lightbox-close" @click="emit('close')">
          ×
        </button>
        <img
          v-if="attachment.kind === 'image'"
          :src="attachment.url"
          alt=""
          class="lightbox-image"
        />
        <pre v-else class="lightbox-text">{{ textContent }}</pre>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  background: rgba(17, 24, 39, 0.75);
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  padding: var(--space-6);
  overflow: auto;
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
}

.lightbox-image {
  display: block;
  max-width: 100%;
  max-height: 85vh;
  border-radius: 4px;
}

.lightbox-text {
  max-width: 80vw;
  margin: 0;
  font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  font-size: 0.85rem;
  white-space: pre-wrap;
  word-break: break-word;
}

.lightbox-close {
  position: absolute;
  top: var(--space-1);
  right: var(--space-2);
  border: none;
  background: none;
  font-size: 1.5rem;
  line-height: 1;
  color: var(--muted);
  cursor: pointer;
}

.lightbox-close:hover {
  color: var(--text);
}

.lightbox-enter-active,
.lightbox-leave-active {
  transition: opacity 0.2s ease;
}

.lightbox-enter-from,
.lightbox-leave-to {
  opacity: 0;
}

.lightbox-enter-from .lightbox-content,
.lightbox-leave-to .lightbox-content {
  transform: scale(0.92);
}
</style>
