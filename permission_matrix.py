
permissions = {
    'admin': ['view_all', 'edit_all'],
    'carrier': ['scan', 'view_own'],
    'substitute': ['view']
}

def check_permission(role, action):
    return action in permissions.get(role, [])
