import logging

from utils import string_color
from utils import xtime


class JsonPrettyFormatter:
    NO_PRINT = ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                'thread', 'threadName', 'processName', 'process']

    def format_default(self, record: logging.LogRecord) -> str:
        header = f'【{record.levelname}】{xtime.from_timestamp_to_strtime(record.created)}\n' \
                 f'rid: {record.__dict__["request_id"]}\n'
        for i in record.__dict__:
            if i not in self.NO_PRINT:
                header += f'{i}: {string_color(record.__dict__[i], "white")}\n'
        return header

    def format_info(self, record: logging.LogRecord) -> str:
        if record.__dict__['koto'] == 'request_send':
            return f'【发送请求】{xtime.from_timestamp_to_strtime(record.created)}\n' \
                   f'rid: {record.__dict__["request_id"]}\n' \
                   f'uri: {record.__dict__["uri"]}\n' \
                   f'{record.__dict__["method"]}: {string_color(record.__dict__["request"], "green")}'
        if record.__dict__['koto'] == 'request_receive':
            return f'【发送请求返回】{xtime.from_timestamp_to_strtime(record.created)}\n' \
                   f'rid: {record.__dict__["request_id"]}\n' \
                   f'duration: {record.__dict__["duration"]}s\n' \
                   f'uri: {record.__dict__["uri"]}\n' \
                   f'{string_color(record.__dict__["response"], "blue")}'

        if record.__dict__['koto'] == 'response_accept':
            return f'【接受请求】{xtime.from_timestamp_to_strtime(record.created)}\n' \
                   f'rid: {record.__dict__["request_id"]}\n' \
                   f'uri: {record.__dict__["uri"]}\n' \
                   f'authorization: {string_color(record.__dict__["authorization"], "green")}\n' \
                   f'remote_ip: {string_color(record.__dict__["remote_ip"], "green")}\n' \
                   f'internal_token: {string_color(record.__dict__["internal_token"], "green")}\n' \
                   f'{record.__dict__["method"]}: {string_color(record.msg, "green")}'
        if record.__dict__['koto'] == 'response_return':
            return f'【接受请求返回】{xtime.from_timestamp_to_strtime(record.created)}\n' \
                   f'rid: {record.__dict__["request_id"]}\n' \
                   f'duration: {record.__dict__["duration"]}s\n' \
                   f'uri: {record.__dict__["uri"]}\n' \
                   f'{string_color(record.__dict__["response"], "pink")}'
        return self.format_default(record)

    @staticmethod
    def format_warn(record: logging.LogRecord) -> str:
        return f'【警告】{xtime.from_timestamp_to_strtime(record.created)}\n' \
               f'rid: {record.__dict__["request_id"]}\n' \
               f'duration: {record.__dict__["duration"]}s\n' \
               f'uri: {record.__dict__["uri"]}\n' \
               f'{string_color(record.__dict__["response"], "yellow")}'

    @staticmethod
    def format_error(record: logging.LogRecord) -> str:
        return f'【错误】{xtime.from_timestamp_to_strtime(record.created)}\n' \
               f'rid: {record.__dict__["request_id"]}\n' \
               f'duration: {record.__dict__["duration"]}s\n' \
               f'uri: {record.__dict__["uri"]}\n' \
               f'-----EXCEPT BEGIN-----\n' \
               f'{string_color(record.__dict__["response"], "red")}' \
               f'-----EXCEPT END-----\n'

    def format(self, record: logging.LogRecord) -> str:
        if record.levelname == 'ERROR':
            return self.format_error(record)
        if record.levelname == 'WARNING':
            return self.format_warn(record)
        if record.levelname == 'INFO':
            return self.format_info(record)
        return self.format_default(record)
