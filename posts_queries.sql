-- name: get-posts
SELECT * FROM posts ORDER BY id DESC LIMIT :limit OFFSET :offset;
