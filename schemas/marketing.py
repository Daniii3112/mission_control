from typing import List
from typing_extensions import TypedDict


class MarketingAngle(TypedDict):
    option_id: str
    hook: str
    main_message: str
    target_channels: List[str]
    campaign_concept: str
    communication_risk: str
