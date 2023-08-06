from typing import List, Optional

from camel_model.camel_model import CamelModel

from domain.distribution.data_block import DataBlock


class DistributionData(CamelModel):
    subtitle: Optional[str]
    blocks: List[DataBlock] = []
