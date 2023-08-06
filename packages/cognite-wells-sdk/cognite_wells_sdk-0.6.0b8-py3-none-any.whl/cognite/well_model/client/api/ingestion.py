import logging
from typing import List

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.models import (
    Source,
    SourceItems,
    Well,
    Wellbore,
    WellboreIngestion,
    WellboreIngestionItems,
    WellboreItems,
    WellIngestion,
    WellIngestionItems,
    WellItems,
)

logger = logging.getLogger("WellsAPI")


class IngestionAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)

    def ingest_wells(self, ingestions: List[WellIngestion]) -> List[Well]:
        path = self._get_path("/wells")
        json = WellIngestionItems(items=ingestions).json()
        response: Response = self.client.post(path, json)
        well_items: WellItems = WellItems.parse_obj(response.json())
        return well_items.items

    def ingest_wellbores(self, ingestions: List[WellboreIngestion]) -> List[Wellbore]:
        path = self._get_path("/wellbores")
        json = WellboreIngestionItems(items=ingestions).json()
        response: Response = self.client.post(path, json)
        wellbore_items: WellboreItems = WellboreItems.parse_obj(response.json())
        return wellbore_items.items

    def ingest_sources(self, sources: List[Source]) -> List[Source]:
        path = self._get_path("/sources")
        json = SourceItems(items=sources).json()
        response: Response = self.client.post(path, json)
        source_items: SourceItems = SourceItems.parse_obj(response.json())
        return source_items.items
