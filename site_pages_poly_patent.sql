CREATE TABLE site_pages_poly_patent (
    id bigserial primary key,
    content text not null,  -- Added content column
    metadata jsonb not null default '{}'::jsonb,  -- Added metadata column
    embedding vector(1536),  -- OpenAI embeddings are 1536 dimensions
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);  -- Removed extra comma

CREATE OR REPLACE FUNCTION public.match_site_pages_poly_patent(
  filter JSONB,
  match_count INT,
  query_embedding VECTOR(1536)
)
RETURNS TABLE (
  id BIGINT,
  content TEXT,
  metadata JSONB,
  embedding VECTOR(1536),
  similarity FLOAT
)
LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY
  SELECT
    v.id,
    v.content,
    v.metadata,
    v.embedding,
    1 - (v.embedding <=> match_site_pages_poly_patent.query_embedding) AS similarity
  FROM "YOUR TABLE NAME" v
  WHERE v.metadata @> filter
  ORDER BY v.embedding <=> match_site_pages_poly_patent.query_embedding
  LIMIT match_count;
END;
$$
;

alter table site_pages_poly_patent enable row level security;

-- Create a policy that allows anyone to read
create policy "Allow ALL"
  on site_pages_poly_patent
  for ALL
  to public
  using (true);