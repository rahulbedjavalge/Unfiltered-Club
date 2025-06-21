-- Unfiltered Club Database Setup
-- Run these commands in your Supabase SQL editor

-- Create posts table
CREATE TABLE IF NOT EXISTS posts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    content text NOT NULL,
    user_id uuid DEFAULT NULL,
    mood text NOT NULL CHECK (mood IN ('sad', 'angry', 'meh', 'lol', 'happy', 'confused')),
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create comments table
CREATE TABLE IF NOT EXISTS comments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    content text NOT NULL,
    user_id uuid DEFAULT NULL,
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create reactions table
CREATE TABLE IF NOT EXISTS reactions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    emoji text NOT NULL,
    user_id text NOT NULL DEFAULT 'anon',
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(post_id, user_id)
);

-- Create rooms table (for future private rooms feature)
CREATE TABLE IF NOT EXISTS rooms (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    description text,
    is_private boolean DEFAULT false,
    passcode text DEFAULT NULL,
    created_by uuid DEFAULT NULL,
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create user_profiles table (anonymous profiles)
CREATE TABLE IF NOT EXISTS user_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    anonymous_id text UNIQUE NOT NULL,
    total_posts integer DEFAULT 0,
    total_comments integer DEFAULT 0,
    total_reactions integer DEFAULT 0,
    favorite_mood text DEFAULT 'meh',
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    last_active timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS posts_created_at_idx ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS posts_mood_idx ON posts(mood);
CREATE INDEX IF NOT EXISTS comments_post_id_idx ON comments(post_id);
CREATE INDEX IF NOT EXISTS reactions_post_id_idx ON reactions(post_id);

-- Enable Row Level Security (RLS)
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE reactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Create policies for anonymous access
-- Posts: Allow all operations for everyone (since it's anonymous)
CREATE POLICY "Allow all access to posts" ON posts FOR ALL USING (true);

-- Comments: Allow all operations for everyone
CREATE POLICY "Allow all access to comments" ON comments FOR ALL USING (true);

-- Reactions: Allow all operations for everyone
CREATE POLICY "Allow all access to reactions" ON reactions FOR ALL USING (true);

-- Rooms: Allow read access to all, create/update for authenticated users
CREATE POLICY "Allow read access to rooms" ON rooms FOR SELECT USING (true);
CREATE POLICY "Allow insert access to rooms" ON rooms FOR INSERT WITH CHECK (true);

-- User profiles: Allow all access
CREATE POLICY "Allow all access to user_profiles" ON user_profiles FOR ALL USING (true);

-- Create functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_posts_updated_at BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_comments_updated_at BEFORE UPDATE ON comments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to get post stats
CREATE OR REPLACE FUNCTION get_post_stats(post_uuid uuid)
RETURNS json AS $$
DECLARE
    result json;
BEGIN
    SELECT json_build_object(
        'comments_count', (SELECT COUNT(*) FROM comments WHERE post_id = post_uuid),
        'reactions_count', (SELECT COUNT(*) FROM reactions WHERE post_id = post_uuid),
        'reactions', (SELECT json_agg(emoji) FROM reactions WHERE post_id = post_uuid)
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Insert some sample data (optional)
INSERT INTO posts (content, mood) VALUES 
    ('I eat cereal for dinner more often than actual meals and I''m not even sorry about it 🥣', 'meh'),
    ('Sometimes I pretend to understand what people are talking about in meetings when I have absolutely no clue', 'confused'),
    ('I still sleep with a stuffed animal and I''m 28 years old. Judge me, I dare you.', 'happy'),
    ('Why do I feel guilty for taking sick days when I''m literally sick? Capitalism has broken my brain.', 'angry'),
    ('I spent 3 hours organizing my digital photos today and it felt more productive than my actual job', 'lol');

-- Add some AI comments to the sample posts
INSERT INTO comments (post_id, content, user_id) 
SELECT 
    p.id,
    '🤖 AI (funny): Cereal for dinner is just breakfast for rebels. You''re living in 3023 while the rest of us are stuck in boring dinner traditions!',
    'ai_bot'
FROM posts p 
WHERE p.content LIKE '%cereal%' 
LIMIT 1;

INSERT INTO comments (post_id, content, user_id) 
SELECT 
    p.id,
    '🤖 AI (helpful): Meeting confusion is universal! Try the "strategic nodding and note-taking" technique - works 73% of the time, every time.',
    'ai_bot'
FROM posts p 
WHERE p.content LIKE '%meetings%' 
LIMIT 1;

-- Create a view for posts with stats
CREATE OR REPLACE VIEW posts_with_stats AS
SELECT 
    p.*,
    COALESCE(c.comment_count, 0) as comment_count,
    COALESCE(r.reaction_count, 0) as reaction_count,
    COALESCE(r.reactions, '[]'::json) as reactions
FROM posts p
LEFT JOIN (
    SELECT post_id, COUNT(*) as comment_count
    FROM comments
    GROUP BY post_id
) c ON p.id = c.post_id
LEFT JOIN (
    SELECT 
        post_id, 
        COUNT(*) as reaction_count,
        json_agg(emoji) as reactions
    FROM reactions
    GROUP BY post_id
) r ON p.id = r.post_id
ORDER BY p.created_at DESC;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;
