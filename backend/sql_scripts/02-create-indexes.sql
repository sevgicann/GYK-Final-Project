-- Create additional indexes for better performance
-- This script runs after tables are created

-- Note: This script will be executed after Flask-Migrate creates the tables
-- The indexes will be created by Flask-Migrate, but we can add additional ones here

-- Create partial indexes for active records
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_active ON users (id) WHERE is_active = true;
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_active ON products (id) WHERE is_active = true;
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_environments_active ON environments (id) WHERE is_active = true;

-- Create composite indexes for common queries
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_recommendations_user_status ON recommendations (user_id, status);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_recommendations_type_created ON recommendations (recommendation_type, created_at DESC);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_model_results_user_type ON model_results (user_id, model_type);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_activity_logs_user_created ON user_activity_logs (user_id, created_at DESC);

-- Create indexes for JSON fields (PostgreSQL 9.4+)
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_model_results_predictions_gin ON model_results USING GIN (predictions);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_recommendations_input_gin ON recommendations USING GIN (input_parameters);

-- Create indexes for text search
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_name_trgm ON products USING GIN (name gin_trgm_ops);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_description_trgm ON products USING GIN (description gin_trgm_ops);

-- Create indexes for date ranges
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_model_results_created_date ON model_results (created_at DESC);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_activity_logs_created_date ON user_activity_logs (created_at DESC);

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Terramind database indexes prepared successfully';
END $$;
