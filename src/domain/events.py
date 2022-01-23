from dataclasses import dataclass


class Event:
    ...


@dataclass
class PipelineStarted(Event):
    pipeline_name: str

    def __post_init__(self):
        self.msg = f"Pipeline Started Processing - {self.pipeline_name}"


@dataclass
class PipelineFinish(Event):
    pipeline_name: str

    def __post_init__(self):
        self.msg = f"Pipeline Finished Processing - {self.pipeline_name}"
