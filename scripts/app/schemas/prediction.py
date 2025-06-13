from pydantic import BaseModel, Field
from typing import Dict, Union

class DiagnosisRequest(BaseModel):
    image_path: str = Field(..., description="Sunucudaki ultrason görüntüsünün tam dosya yolu.")
    features: Dict[str, Union[str, float, int]] = Field(
        ..., description="Hasta bilgilerini içeren öznitelikler sözlüğü."
    )
