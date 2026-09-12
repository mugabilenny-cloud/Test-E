# Supabase integration snippets

## Python client

```python
from supabase import create_client
client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
rows = client.table('nodes').select('*').is_('parent_id', 'null').execute().data
```

## RPC for search

```python
rows = client.rpc('fn_search_tree', {
    'search_query': 'PHA 2101',
    'result_limit': 25,
}).execute().data
```

## RPC for device bookmarks

```python
client.rpc('fn_save_bookmark', {
    'p_device_token': device_token,
    'p_link_id': resource_id,
}).execute()
```

## SQL migration

Run `supabase/migrations/001_initial_schema.sql` in the Supabase SQL Editor. It creates the content tree, links, device-scoped bookmarks/history, ads, notifications, RPC interface, and RLS policies.

## Admin role

The dashboard checks `auth.users.app_metadata.role == 'admin'`. Set that metadata using a trusted administrative process. Do not put a service-role key into `.streamlit/secrets.toml` for the public/student application.
