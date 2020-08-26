import oss2,re

class AliOss:

    _accessKeyId = ''

    _accessKeySecret = ''

    _bucket = ''

    _endpint = ''



    _auth = None


    def __init__(self, accessKeyId, accessKeySecret, endpint, bucket):
        self._accessKeySecret = accessKeySecret
        self._accessKeyId = accessKeyId
        self._bucket = bucket
        self._endpint = endpint

    def _getAuth(self):
        if(not self._auth or self._auth is None):
            self._auth = oss2.Auth(self._accessKeyId, self._accessKeySecret)
        return self._auth

    def _getBucket(self, bucket, endpint):
        bucketObj = oss2.Bucket(self._getAuth(), endpint, bucket)
        return bucketObj

    def getFileList(self, prefix='', delimiter='', bucket='', endpint=''):
        if not bucket or bucket is None:
            bucket = self._bucket
        if not endpint or endpint is None:
            endpint = self._endpint
        listData = []
        for obj in oss2.ObjectIterator(self._getBucket(bucket, endpint), prefix, delimiter):
            if re.match('.*/$', obj.key) is None:
                item = {
                    'type': obj.type,
                    'size': obj.size,
                    'storage_class': obj.storage_class,
                    'last_modified': obj.last_modified,
                    'etag': obj.etag,
                    'object_name': obj.key,
                    'suffix': obj.key[obj.key.rfind('.')+1:],
                    'file_name': obj.key[obj.key.rfind('/')+1:obj.key.rfind('.')]
                }
                listData.append(item)
        return listData

    def download(self, objectName, localFilePath, bucket='', endpoint=''):
        if not bucket or bucket is None:
            bucket = self._bucket
        if not endpint or endpint is None:
            endpint = self._endpint
        bucketObj = self._getBucket(bucket, endpint)
        bucketObj.get_object_to_file(objectName, localFilePath)
        return self


    def setSymlink(self, symlink, objectName, bucket='', endpoint=''):
        if not bucket or bucket is None:
            bucket = self._bucket
        if not endpint or endpint is None:
            endpint = self._endpint
        bucketObj = self._getBucket(bucket, endpint)
        bucketObj.put_symlink(objectName, symlink)
        return self

    def getSymlinkObject(self, symlink, bucket='', endpoint=''):
        if not bucket or bucket is None:
            bucket = self._bucket
        if not endpint or endpint is None:
            endpint = self._endpint
        return self._getBucket(bucket, endpint).get_symlink(symlink)



