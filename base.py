"""base methods and classes
"""
class BaseHandler():
    def __init__(self):
        self._status_code: int = 0
        self.error = ''

    def status(self):
        if self._status_code == 0:
            return 'READY'
        elif self._status_code == 1:
            return 'ALIVE'
        else:
            return 'ERROR'

    def _exception_handle(self, msg='', exception=None, is_fatal=True, re_raise=False):
        ex_msg = f'ERROR. {msg} {exception}'
        self.error = ex_msg

        if is_fatal:
            self._status_code = 2
            self.exit()

        if re_raise and exception:
            raise RuntimeError(ex_msg) from exception
