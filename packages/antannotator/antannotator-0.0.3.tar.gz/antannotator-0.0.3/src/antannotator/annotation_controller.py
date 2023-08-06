import asyncio
from typing import List

import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Box, Label, Layout, Output

from antannotator.persistence import (AnnotationEvent, AnnotationSample,
                                      AnnotationTaskStorage, AppendSamplesStat,
                                      AutoAnnotationTaskStorage,
                                      AutoEventStorage, EventStorage)
from antannotator.text_classification_wiget import \
    get_text_classification_wiget


class AnnotationController:
    def __init__(self, task_storage: AnnotationTaskStorage, event_storage: EventStorage) -> None:
        self.task_storage = task_storage
        self.event_storage = event_storage

    
    def append_samples(self, samples: List[AnnotationSample]) -> AppendSamplesStat: # TODO change type to Controller stat, wich include annotated samples count
        return self.task_storage.append_samples(samples)

    @staticmethod
    def create_auto(task_storage_path:str, event_storage_path:str):
        return AnnotationController(task_storage=AutoAnnotationTaskStorage.get_task_storage(task_storage_path), event_storage=AutoEventStorage.get_event_storage(event_storage_path))

    def do_annotaions(self, show_logs=False, show_comment=True):
        widget = Box([Label(value="Starting annotation ....")], layout=Layout(width='auto', height='auto'))
        log = Output()

        already_annotated_ids = self.event_storage.get_annotated_ids()

        loop = asyncio.get_running_loop()

        def create_event(annotation_result, sample):
            return AnnotationEvent(annotation_result=annotation_result, annotation_sample=sample)
        # create_event(None, None)

        def persist(event: AnnotationEvent):
            self.event_storage.persist_event(annotation_event=event)
        # persist(event=None)            

        async def work():
            for sample in self.task_storage.get_samples():
                if sample.sample_id not in already_annotated_ids:
                    log.append_stdout(f'Run annotation for sample_id={sample.sample_id} ' + '\n')
                    future = loop.create_future()
                    
                    def on_done(annotation_result):
                        future.set_result(annotation_result)
                    


                    widget.children = [get_text_classification_wiget(sample=sample, on_done=on_done, show_comment=show_comment)]

                    annotation_result = await future
                    
                    log.append_stdout(f'Done for sample_id={sample.sample_id} ' + '\n')
                    
                    log.append_stdout(f'Create event ' + '\n')
                    annotation_event = create_event(annotation_result=annotation_result, sample=sample) #{"test": annotation_result} #AnnotationEvent(annotation_result=annotation_result, annotate_sample=sample)
                    log.append_stdout(f'Start persist ' + '\n')
                    persist(event=annotation_event)
                    log.append_stdout(f'Event persisted ' + '\n')
            
            widget.children = [Label(value="All done")]


        loop.create_task(work())
        display(widget)
        if show_logs:
            display(log)
        

