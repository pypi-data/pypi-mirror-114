import abc
import datetime
import json
import os
from collections import namedtuple
from ntpath import join
from pathlib import Path
from typing import (Any, Callable, Dict, Iterable, List, NamedTuple, Optional,
                    Sequence, Set)

from antannotator.utils import (JsonSerializableEncoder, JsonSerilaizable,
                                distinct_by, generate_random_filename)

#DOTO define serializable base class for AvailableOptions


class AnnotationSample(JsonSerilaizable):
    def __init__(self, sample_id: str, task_data: Any, hidden_info: Optional[Dict], visible_info: Optional[Dict], available_options: Dict[str, str]):
        self.sample_id = sample_id
        self.task_data = task_data
        self.hidden_info = hidden_info
        self.visible_info= visible_info
        self.available_options = available_options
        # key is option key, value is display name
    def to_serializable(self):
        return self.__dict__

class AnnotationEvent(JsonSerilaizable):
    def __init__(self, annotation_result, annotation_sample: AnnotationSample) -> None:
        self.annotation_result = annotation_result 
        self.annotation_sample = annotation_sample 
    
    def to_serializable(self):
        return self.__dict__

class AnnotationEventWrapper(JsonSerilaizable):
    def __init__(self, annotation_event: AnnotationEvent, event_time):
        self.annotation_event = annotation_event
        self.event_time =event_time

    def to_serializable(self):
        return self.__dict__

class EventStorage(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass
    
    @abc.abstractmethod
    def persist_event(self, annotation_event:AnnotationEvent):
        raise NotImplementedError('users must define "persist_event" to use this base class')

    @abc.abstractmethod
    def get_annotated_ids(self) -> List[str]:
        raise NotImplementedError('users must define "get_annotated_ids" to use this base class')

        

class FileEventStorage(EventStorage):
    def __init__(self, directory) -> None:
        self.directory = directory
        self.__session_file = None
        
    def __get_session_file(self):
        if self.__session_file is None:
            session_file = os.path.join(self.directory, f"{generate_random_filename()}.json")
            self.__session_file = session_file
            os.makedirs(self.directory, exist_ok=True)
            return session_file
        else:
            return self.__session_file

    def persist_event(self, annotation_event:AnnotationEvent):
        session_file = self.__get_session_file()
        
        now = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
        event_wrapper = AnnotationEventWrapper(annotation_event=annotation_event, event_time=now)
        json_line = json.dumps(event_wrapper, cls=JsonSerializableEncoder)
        with open(session_file, "a") as f:
            f.writelines([json_line, "\n"])


    def get_annotated_ids(self):
        if not os.path.exists(self.directory):
            return []
            
        def get_ids_from_file(file):
            with open(file) as f:
                lines = f.readlines()
                event_wrappers = [json.loads(line) for line in lines]

                return [event_wrapper["annotation_event"]["annotation_sample"]["sample_id"] for event_wrapper in event_wrappers]

        event_files = [os.path.join(self.directory, file) for file in os.listdir(self.directory)]
        
        return set([id for file in event_files for id in get_ids_from_file(file)])                

class AutoEventStorage:
    def get_event_storage(path):
        return FileEventStorage(path)


AppendSamplesStat = namedtuple("AppendSamplesStat", ["total_tasks_count", "appended_tasks_count"])

class AnnotationTaskStorage(metaclass=abc.ABCMeta):
    
    def __init__(self) -> None:
        pass

    def append_samples(self, samples: List[AnnotationSample]) -> AppendSamplesStat:
        existed_ids = self._get_existed_ids()
        
        #existed_ids = self.event_storage.get_annotated_ids()
        new_tasks = list(distinct_by([sample for sample in samples if sample.sample_id not in existed_ids], lambda x:x.sample_id))
        self._persist_batch(new_tasks)

        return AppendSamplesStat(total_tasks_count=len(samples), appended_tasks_count=len(new_tasks))

    @abc.abstractmethod
    def _get_existed_ids() -> List[str]:
        raise NotImplementedError('users must define "_get_existed_ids" to use this base class')

    @abc.abstractmethod
    def _persist_batch(self, samples: List[AnnotationSample]):
        raise NotImplementedError('users must define "_persist_batch" to use this base class')

    @abc.abstractmethod
    def get_samples(self) -> Iterable[AnnotationSample]:
        raise NotImplementedError('users must define "get_samples" to use this base class')


class FileAnnotationTaskStorage(AnnotationTaskStorage):
    def __init__(self, directory) -> None:
        super().__init__()
        self.directory = directory

    def _get_existed_ids(self) -> List[str]:
        if not os.path.exists(self.directory):
            return []

        def get_ids_from_file(file):
            with open(file) as f:
                lines = f.readlines()
                samples = [json.loads(line) for line in lines]

                return [sample["sample_id"] for sample in samples]

        batch_files = [os.path.join(self.directory, file) for file in os.listdir(self.directory)]
        
        return set([id for file in batch_files for id in get_ids_from_file(file)])                


    def _persist_batch(self, samples: List[AnnotationSample]):
        batch_file = os.path.join(self.directory, f"{generate_random_filename()}.json")
        os.makedirs(self.directory, exist_ok=True)

        with open(batch_file, "w") as f:
            for sample in samples:
                json_line = json.dumps(sample, cls=JsonSerializableEncoder)
                f.writelines([json_line, "\n"])

    def get_samples(self) -> Iterable[AnnotationSample]:
        batch_files = [os.path.join(self.directory, file) for file in os.listdir(self.directory)]
        for batch_file in batch_files:
            with open(batch_file) as f:
                lines = f.readlines()
                samples = [json.loads(line) for line in lines]
                for sample in samples:
                    yield AnnotationSample(**sample)



class AutoAnnotationTaskStorage:
    def get_task_storage(path):
        return FileAnnotationTaskStorage(directory=path)


