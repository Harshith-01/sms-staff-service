-- Staff service bootstrap SQL
-- Staff domain uses shared tables in common schema. This file is intentionally lightweight.

BEGIN;

-- No-op marker to keep migration runners happy.
SELECT 1;

COMMIT;
