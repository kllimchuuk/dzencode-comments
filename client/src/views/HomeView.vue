<script setup>
import { onMounted } from "vue";
import { useCommentsStore } from "../stores/comments";
import CommentForm from "../components/CommentForm.vue";
import SortHeader from "../components/SortHeader.vue";
import CommentNode from "../components/CommentNode.vue";
import Pagination from "../components/Pagination.vue";

const store = useCommentsStore();

onMounted(() => store.load());
</script>

<template>
  <section>
    <CommentForm />
    <SortHeader :ordering="store.ordering" @change="store.setOrdering" />
    <p v-if="store.loading">Loading…</p>
    <p v-else-if="!store.roots.length">No comments yet.</p>
    <div v-else class="comment-list">
      <CommentNode v-for="root in store.roots" :key="root.id" :comment="root" />
    </div>
    <Pagination
      :page="store.page"
      :total-pages="store.totalPages"
      @change="store.setPage"
    />
  </section>
</template>
