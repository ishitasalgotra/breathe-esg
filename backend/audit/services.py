from .models import AuditLog


def write_audit(*, tenant, entity_type, entity_id, action, before_value, after_value, changed_by):
    return AuditLog.objects.create(tenant=tenant, entity_type=entity_type, entity_id=str(entity_id), action=action, before_value=before_value, after_value=after_value, changed_by=changed_by)
