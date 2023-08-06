from pydantic import (
    BaseModel,
    HttpUrl, root_validator
)

from typing import Optional, List

from ..generics import Image


class OfflinePreRunEventData_MetaField(BaseModel):
    webhooks: Optional[HttpUrl]


class OfflinePreRunEventData(BaseModel):
    request_id: str
    meta: Optional[OfflinePreRunEventData_MetaField]
    images: Optional[List[Image]]
    imagesfile: Optional[str]
    model_name: str
    model_id: str
    labels_source: Optional[str]

    @root_validator
    def check_images_or_imagefile_has_data(cls, values):
        if not values.get('images') and not values.get('imagesfile'):
            raise ValueError(
                "At least one of 'images' and 'imagesfile' must be set."
            )

        return values
