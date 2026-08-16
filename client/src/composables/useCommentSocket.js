import { onMounted, onUnmounted } from "vue";
import { useCommentsStore } from "../stores/comments";

export function useCommentSocket() {
  const store = useCommentsStore();
  let socket = null;

  function connect() {
    const protocol = location.protocol === "https:" ? "wss:" : "ws:";
    socket = new WebSocket(`${protocol}//${location.host}/ws/comments/`);
    socket.onmessage = () => store.load();
  }

  onMounted(connect);
  onUnmounted(() => socket?.close());
}
