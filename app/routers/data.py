from pathlib import Path
import json

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/data",
    tags=["Data"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(path: Path):
    if not path.exists():
        raise HTTPException(status_code=404, detail="Không tìm thấy dữ liệu")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/ppct/{khoi}")
def get_ppct(khoi: str):
    file = DATA_DIR / "ppct" / f"{khoi}.json"
    return load_json(file)


@router.get("/curriculum/{khoi}/{chuong}")
def get_curriculum(khoi: str, chuong: str):
    file = DATA_DIR / "curriculum" / khoi / f"{chuong}.json"
    return load_json(file)


@router.get("/mapping/{khoi}/{chuong}")
def get_mapping(khoi: str, chuong: str):
    file = DATA_DIR / "mapping" / khoi / f"{chuong}.json"
    return load_json(file)