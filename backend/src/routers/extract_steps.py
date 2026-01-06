from fastapi import APIRouter

router = APIRouter()


@router.post("/extract-steps/")
def extract_steps_from_applehealthcare():
    return {"message": "Extracted steps from Apple Healthcare data."}
