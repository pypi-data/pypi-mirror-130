from typing import List, Optional

from camel_model.camel_model import CamelModel

from domain.distribution.distribution_image import DistributionImage


class DataBlock(CamelModel):
    text: Optional[List[str]]
    image: Optional[DistributionImage]
    upper_text: Optional[bool]

