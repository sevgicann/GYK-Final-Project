-- Create necessary PostgreSQL extensions
-- This script runs when the database is first initialized

-- Enable UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pg_stat_statements for query monitoring
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Enable unaccent for text search
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Enable btree_gin for better indexing
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Enable btree_gist for better indexing
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- Create custom functions for better performance
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Set timezone
SET timezone = 'UTC';

-- Set default transaction isolation level
SET default_transaction_isolation = 'read committed';