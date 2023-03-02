from typing import Union

from pydantic import BaseModel


# result = {'code': 200, 'data': data, 'status': True, 'message': None}
class responseData(BaseModel):
    code: int = 1
    data: Union[dict, list, None]
    status: bool = True
    message: str = ""

    @classmethod
    def ok(cls, data):
        _a = cls()
        _a.code = 200
        _a.data = data
        _a.status = True
        _a.message = ""
        return _a

    @classmethod
    def fail(cls, message):
        _a = cls()
        _a.code = 555
        _a.data = None
        _a.status = False
        _a.message = message
        return _a


if __name__ == '__main__':
    a = responseData.ok("123")
    print(a)
