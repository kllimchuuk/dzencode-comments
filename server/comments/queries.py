from __future__ import annotations

from django.db.models import QuerySet

from comments.models import Comment

ALLOWED_ORDERING = {
    "user_name",
    "-user_name",
    "email",
    "-email",
    "created_at",
    "-created_at",
}
DEFAULT_ORDERING = "-created_at"


def normalize_ordering(value: str | None) -> str:
    return value if value in ALLOWED_ORDERING else DEFAULT_ORDERING


def get_root_comments(*, ordering: str | None) -> QuerySet[Comment]:
    return (
        Comment.objects.roots()
        .select_related("attachment")
        .order_by(normalize_ordering(ordering))
    )


def get_comment_forest(roots: list[Comment]) -> list[Comment]:
    return [_build_subtree(root) for root in roots]


def _build_subtree(root: Comment) -> Comment:
    nodes = list(
        Comment.objects.descendants(root, include_self=True).select_related(
            "attachment"
        )
    )
    by_id = _index_nodes(nodes)
    _link_children(nodes, by_id)
    return by_id[root.pk]


def _index_nodes(nodes: list[Comment]) -> dict[int, Comment]:
    by_id: dict[int, Comment] = {}
    for node in nodes:
        node._children = []
        by_id[node.pk] = node
    return by_id


def _link_children(nodes: list[Comment], by_id: dict[int, Comment]) -> None:
    for node in nodes:
        parent = by_id.get(node.parent_id)
        if parent is not None:
            parent._children.append(node)
