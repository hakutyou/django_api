import abc


class VirtualFace(metaclass=abc.ABCMeta):
    def face_detect(self, url: str) -> bool:
        """
        人脸检测
        """
        return True

    @abc.abstractmethod
    def user_add(self, image_base64: bytes, person_name: str, group_id: str = 'default', person_id: str = None) -> dict:
        """
        人脸库添加人脸
        """
        pass

    @abc.abstractmethod
    def user_remove(self, user_id: str) -> dict:
        """
        人脸库删除人脸
        """
        pass

    @abc.abstractmethod
    def user_search(self, image_base64: str, group_id: str = 'default') -> dict:
        """
        从人脸库查找人脸
        """
        pass

    def user_list(self) -> list:
        """
        列出人脸库所有人
        """
        return []

    def face_verify(self, url: str):
        """
        在线活体检测
        """
        return None

    def face_compare(self, url_1: str, url_2: str):
        """
        人脸对比
        """
        return None
