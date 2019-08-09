from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class TencentCoSService:
    def __init__(self, region, secret_id, secret_key, default_bucket, token=None):
        self.bucket = default_bucket
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
        self.client = CosS3Client(config)

    def list(self, path, bucket=None):
        if not bucket:
            bucket = self.bucket
        return self.client.list_objects(Bucket=bucket, Prefix=path[1:],
                                        Delimiter='/', MaxKeys=10)

    def file(self, path, bucket=None):
        if not bucket:
            bucket = self.bucket
        return self.client.get_object(Bucket=bucket, Key=path)
