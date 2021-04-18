-- upgrade --
ALTER TABLE "user" ADD "_index_id" VARCHAR(255);
CREATE UNIQUE INDEX "uid_user_uuid_863a0b" ON "user" ("uuid");
-- downgrade --
ALTER TABLE "user" DROP COLUMN "_index_id";
DROP INDEX "idx_user_uuid_863a0b";
