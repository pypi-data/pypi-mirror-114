from coinlib.feature.CoinlibFeature import CoinlibFeature
from abc import abstractmethod

from coinlib.feature.FeatureDTO import FeatureData, ProcessResponse


class CoinlibFeatureProcessor(CoinlibFeature):


    async def start_run_process(self):
        return await self.run_process()

    @abstractmethod
    async def run_process(self) -> ProcessResponse:
        pass

