-- Supabase SQL Schema for AI Health Report Interpreter
-- Run this in your Supabase Dashboard -> SQL Editor

create table if not exists public.reports (
    id uuid primary key default gen_random_uuid(),
    user_id text not null,
    filename text not null,
    report_type text not null default 'general',
    language text not null default 'en',
    ocr_source text not null default 'Tesseract',
    analysis jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_reports_user_created
    on public.reports (user_id, created_at desc);

-- Enable Row Level Security (backend uses service_role key, which bypasses RLS,
-- while keeping direct anon/client access locked down by default)
alter table public.reports enable row level security;
