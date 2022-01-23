from pipeline.base_pipeline import BasePipeline


class TripsAggregated(BasePipeline):
    def __init__(self, **kwargs) -> None:
        super(TripsAggregated, self).__init__(**kwargs)

    @property
    def pipeline(self):
        return []
