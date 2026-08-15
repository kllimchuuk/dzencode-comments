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
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  padding: 1.25rem;
  overflow: auto;
  background: #fff;
  border-radius: 6px;
  transition: transform 0.2s ease;
}

.lightbox-image {
  display: block;
  max-width: 100%;
  max-height: 85vh;
}

.lightbox-text {
  max-width: 80vw;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.lightbox-close {
  position: absolute;
  top: 0.25rem;
  right: 0.5rem;
  border: none;
  background: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
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
  transform: scale(0.9);
}
</style>
