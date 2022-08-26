-- upgrade --
ALTER TABLE "events" ADD "x" TEXT NOT NULL;
-- downgrade --
ALTER TABLE "events" DROP COLUMN "x";
