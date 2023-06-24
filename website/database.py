import uuid
from abc import abstractmethod, ABC
from pathlib import Path

from website.file_utils import *
from website.models import Thought

_LOCAL_REPO_PATH = "/Users/dannyyang/workspace/flask-demo/thought-repo-local"
_DELETED_LOCAL_REPO_PATH = "/Users/dannyyang/workspace/flask-demo/thought-repo-local/deleted"
_LOCAL_HEADER_END_MARKER = "_END"


class _ThoughtDb(ABC):

    @abstractmethod
    def bootstrap(self):
        pass

    @abstractmethod
    def get(self, thought_id: str):
        pass

    @abstractmethod
    def create(self, thought_data: str):
        pass

    @abstractmethod
    def update(self, thought_id: str, thought_data: str):
        pass

    @abstractmethod
    def delete(self, thought_id: str):
        pass


class LocalThoughtDb(_ThoughtDb):

    def write_header_metadata(self, fp):
        now = now_epoch()
        header_metadata = [f"{now}\n",  # create datetime
                           f"{now}\n",  # last modified datetime
                           f"{_LOCAL_HEADER_END_MARKER}\n"]
        fp.writelines(header_metadata)


    def get_local_thought_files(self):
        return [f for f in os.listdir(_LOCAL_REPO_PATH) if f.startswith(THOUGHT_ID_PREFIX)]


    def bootstrap(self):
        # make the path if it doesn't exist
        Path(_LOCAL_REPO_PATH).mkdir(parents=True, exist_ok=True)

    def get(self, thought_id):
        files = self.get_local_thought_files()
        for f in files:
            t_id = get_thought_id_from_f_name(f)
            if t_id == thought_id:
                return f
        raise Exception(f"Did not find thoughtId: {thought_id}")

    def get_all(self, sort_function, reverse) -> list[Thought]:
        files = self.get_local_thought_files()
        result = []
        for f in files:
            f_path = f"{_LOCAL_REPO_PATH}/{f}"
            with open(f_path, 'r') as f_in:
                t_id = get_thought_id_from_abs_path(abs_path=f_path)

                file_ctime = int(f_in.readline().strip())
                file_mtime = int(f_in.readline().strip())
                end_marker = f_in.readline().strip()

                if end_marker != _LOCAL_HEADER_END_MARKER:
                    raise Exception(
                        f"Expected header to end after 2 lines. Instead found {end_marker} Corrupted file: {f_path}")

                result.append(
                    Thought(
                        tid=t_id,
                        text=f_in.read(),
                        createDate=epoch_to_str(file_ctime),
                        createTimeEpochMs=file_ctime,
                        lastModifiedDate=epoch_to_str(file_mtime),
                        lastModifiedEpochMs=file_mtime
                    )
                )

        result = sorted(result, key=sort_function, reverse=reverse)
        return result

    def create(self, thought_data: str) -> str:
        thought_id = uuid.uuid4()
        with open(f"{_LOCAL_REPO_PATH}/{THOUGHT_ID_PREFIX}{thought_id}.txt", 'w') as fp:
            self.write_header_metadata(fp)
            fp.write(thought_data)
        return str(thought_id)

    def delete(self, thought_id) -> bool:
        files = self.get_local_thought_files()

        for f in files:
            t_id = get_thought_id_from_f_name(f)
            if t_id == thought_id:
                print(f"[DELETE] Found thought {thought_id}, will delete.")

                old_path = f"{_LOCAL_REPO_PATH}/{f}"
                new_path = f"{_LOCAL_REPO_PATH}/{DELETED_PREFIX}{f}"
                os.rename(old_path, new_path)
                return True
        return False

    def update(self, thought_id: str, thought_data: str):
        # files = self.get_local_thought_files()
        # for f in files:
        #     t_id = get_thought_id_from_f_name(f)
        #     if t_id == thought_id:
        #         print(f"[DELETE] Found thought {thought_id}, will delete.")
        #
        #         old_path = f"{_LOCAL_REPO_PATH}/{f}"
        #         new_path = f"{_LOCAL_REPO_PATH}/{DELETED_PREFIX}{f}"
        #         os.rename(old_path, new_path)
        #         return True
        # return False
        # TODO: implement
        pass

