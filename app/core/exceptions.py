from fastapi import HTTPException, status

def get_object_or_404(obj, detail: str = "Object not found"):
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return obj