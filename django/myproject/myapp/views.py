from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.tasks import run_job
from celery.result import AsyncResult
from django.core.cache import cache

@api_view(["POST"])
def run_sequence_and_search(request):
    nucleotide_id = request.data.get("id", "30271926")
    pattern = request.data.get("pattern", "GGCAT")
    result = run_job(nucleotide_id, pattern)
    
    return Response({
        "task_id": result.id,  # this is the group or chord ID
        "message": "Chained tasks started. You can poll the result using the task_id."
    })

@api_view(["GET"])
def get_task_result(request, task_id):
    task_result = AsyncResult(task_id)

    # Safely handle result serialization
    result_data = None
    if task_result.successful():
        result_data = task_result.result
    elif task_result.failed():
        result_data = str(task_result.result)  # Convert error to string
    elif task_result.status == "PENDING":
        result_data = None

    return Response({
        "task_id": task_id,
        "status": task_result.status,
        "is_ready": task_result.ready(),
        "result": result_data,
    })