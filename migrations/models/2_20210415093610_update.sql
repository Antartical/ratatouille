-- upgrade --
CREATE UNIQUE INDEX "uid_user__index__a410b4" ON "user" ("_index_id");
-- downgrade --
DROP INDEX "idx_user__index__a410b4";
