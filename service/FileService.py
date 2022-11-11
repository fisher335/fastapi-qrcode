import os
import time

from model.MinioFile import MinioFile
from utils.MinIOFileUtil import Bucket


async def get_localfile_list():
    filePath = os.getcwd() + "/static/file"
    # print(filePath)
    fileList = []
    for home, dirs, files in os.walk(filePath):
        for filename in files:
            result = {}
            fullname = os.path.join(home, filename)
            fileinfo = os.stat(fullname)
            result['name'] = filename
            result['size'] = hum_convert(fileinfo.st_size)
            result['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(fileinfo.st_ctime))
            result['url'] = fullname
            fileList.append(result)
    # print(fileList)
    return fileList


def hum_convert(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size


def getMinIOFileList(fileName=None):
    minio_obj = Bucket()
    fileTable = []
    fileList = minio_obj.bucket_list_files('upload', '/')
    for obj in fileList:
        file = MinioFile()
        file.fileID = obj.etag
        file.bucket = obj.bucket_name
        file.type = obj.content_type
        file.date = obj.last_modified
        file.name = obj.object_name
        file.size = hum_convert(obj.size)
        # file = {'bucket': , 'name': obj.object_name, 'date': obj.last_modified,
        #         'fileID': obj.etag, 'size': hum_convert(obj.size), 'type': obj.content_type}
        fileTable.append(file)
    return fileTable


def downloadFile(fileName: str):
    minio_obj = Bucket()

    url = minio_obj.presigned_get_file('upload', fileName)
    print(url)
    return url


if __name__ == "__main__":
    print(getMinIOFileList())
