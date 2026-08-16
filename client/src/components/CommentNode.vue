<script setup>
import { ref } from "vue";
import Lightbox from "./Lightbox.vue";
import CommentForm from "./CommentForm.vue";

defineProps({ comment: { type: Object, required: true } });

const showLightbox = ref(false);
const showReply = ref(false);

function formatDate(iso) {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(iso));
}
</script>

<template>
  <article class="comment">
    <header class="comment-head">
      <a
        v-if="comment.home_page"
        :href="comment.home_page"
        target="_blank"
        rel="noopener noreferrer"
        class="comment-author"
      >
        {{ comment.user_name }}
      </a>
      <span v-else class="comment-author">{{ comment.user_name }}</span>
      <span class="comment-email">{{ comment.email }}</span>
      <time class="comment-date">{{ formatDate(comment.created_at) }}</time>
    </header>
    <div class="comment-text" v-html="comment.text"></div>
    <div v-if="comment.attachment" class="comment-attachment">
      <img
        v-if="comment.attachment.kind === 'image'"
        :src="comment.attachment.url"
        alt=""
        class="attachment-thumb"
        @click="showLightbox = true"
      />
      <button
        v-else
        type="button"
        class="attachment-file"
        @click="showLightbox = true"
      >
        📎 View text file
      </button>
      <Lightbox
        :attachment="comment.attachment"
        :open="showLightbox"
        @close="showLightbox = false"
      />
    </div>
    <div class="comment-actions">
      <button type="button" class="reply-btn" @click="showReply = !showReply">
        {{ showReply ? "Cancel" : "Reply" }}
      </button>
    </div>
    <CommentForm
      v-if="showReply"
      :parent="comment.id"
      @created="showReply = false"
    />
    <div v-if="comment.replies?.length" class="comment-replies">
      <CommentNode
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
      />
    </div>
  </article>
</template>

<style scoped>
.comment {
  padding: var(--space-4);
  margin-bottom: var(--space-3);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.comment-head {
  display: flex;
  gap: var(--space-2);
  align-items: baseline;
  margin-bottom: var(--space-2);
  font-size: 0.85rem;
}

.comment-author {
  font-weight: 600;
  color: var(--text);
}

a.comment-author:hover {
  color: var(--accent);
  text-decoration: none;
}

.comment-email {
  color: var(--muted);
}

.comment-date {
  margin-left: auto;
  color: var(--muted);
  font-size: 0.8rem;
}

.comment-text {
  line-height: 1.55;
  overflow-wrap: anywhere;
}

.comment-attachment {
  margin-top: var(--space-3);
}

.attachment-thumb {
  max-width: 220px;
  max-height: 160px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: transform 0.15s;
}

.attachment-thumb:hover {
  transform: scale(1.02);
}

.attachment-file {
  padding: 0;
  border: none;
  background: none;
  font: inherit;
  color: var(--accent);
  cursor: pointer;
}

.comment-actions {
  margin-top: var(--space-2);
}

.reply-btn {
  padding: 0;
  border: none;
  background: none;
  font: inherit;
  font-size: 0.85rem;
  color: var(--accent);
  cursor: pointer;
}

.reply-btn:hover {
  text-decoration: underline;
}

.comment-replies {
  margin-top: var(--space-3);
  margin-left: var(--space-4);
  padding-left: var(--space-4);
  border-left: 2px solid var(--border);
}

.comment-replies .comment:last-child {
  margin-bottom: 0;
}
</style>
