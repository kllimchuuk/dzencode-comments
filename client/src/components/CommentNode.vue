<script setup>
defineProps({ comment: { type: Object, required: true } });

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
</style>
