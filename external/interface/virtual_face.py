import abc


class VirtualFace(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def face_detect(self, url: str) -> bool:
        pass

    @abc.abstractmethod
    def user_add(self, image_base64: bytes, person_name: str, group_id: str = 'default', person_id: str = None) -> dict:
        pass

    @abc.abstractmethod
    def user_remove(self, user_id: str) -> dict:
        pass

    @abc.abstractmethod
    def user_search(self, image_base64: str, group_id: str = 'default') -> dict:
        pass
