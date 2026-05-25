from fastapi import APIRouter, Response

from app.services.evidence_import import EVIDENCE_IMPORT_TEMPLATE_FILENAME, build_evidence_import_template_csv


router = APIRouter()


@router.get("/import/template.csv")
def download_evidence_import_template_csv() -> Response:
    csv_text = build_evidence_import_template_csv()
    return Response(
        content=csv_text.encode("utf-8"),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{EVIDENCE_IMPORT_TEMPLATE_FILENAME}"',
        },
    )
