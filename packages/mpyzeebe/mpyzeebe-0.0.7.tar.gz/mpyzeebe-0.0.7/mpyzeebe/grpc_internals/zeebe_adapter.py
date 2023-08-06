from mpyzeebe.grpc_internals.zeebe_job_adapter import ZeebeJobAdapter
from mpyzeebe.grpc_internals.zeebe_message_adapter import ZeebeMessageAdapter
from mpyzeebe.grpc_internals.zeebe_workflow_adapter import ZeebeWorkflowAdapter


# Mixin class
class ZeebeAdapter(ZeebeWorkflowAdapter, ZeebeJobAdapter, ZeebeMessageAdapter):
    pass
