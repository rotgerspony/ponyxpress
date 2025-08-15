
# Add tenant_id to models and filter by current tenant where needed
def get_current_tenant():
    # TODO: use session or subdomain routing
    return "tenant1"

def filter_by_tenant(query, model):
    tenant_id = get_current_tenant()
    return query.filter_by(tenant_id=tenant_id)
