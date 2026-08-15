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
      <span class="comment-author">{{ comment.user_name }}</span>
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
  padding: 0.75rem;
  margin-bottom: 0.75rem;
  background: #fff;
  border: 1px solid #e2e4e8;
  border-radius: 6px;
}

.comment-head {
  display: flex;
  gap: 0.75rem;
  align-items: baseline;
  margin-bottom: 0.4rem;
  font-size: 0.85rem;
}

.comment-author {
  font-weight: 600;
}

.comment-email {
  color: #6b7280;
}

.comment-date {
  margin-left: auto;
  color: #9ca3af;
}

.comment-text {
  line-height: 1.5;
}

.comment-attachment {
  margin-top: 0.5rem;
}

.attachment-thumb {
  max-width: 240px;
  max-height: 180px;
  border: 1px solid #e2e4e8;
  border-radius: 4px;
  cursor: pointer;
}

.attachment-file {
  padding: 0;
  border: none;
  background: none;
  color: #2563eb;
  font: inherit;
  cursor: pointer;
}

.comment-actions {
  margin-top: 0.5rem;
}

.reply-btn {
  padding: 0;
  border: none;
  background: none;
  color: #2563eb;
  font: inherit;
  font-size: 0.85rem;
  cursor: pointer;
}

.comment-replies {
  margin-top: 0.75rem;
  margin-left: 1.25rem;
  padding-left: 0.75rem;
  border-left: 2px solid #e2e4e8;
}

.comment-replies .comment:last-child {
  margin-bottom: 0;
}
</style>
