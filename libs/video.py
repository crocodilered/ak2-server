import os
import re
import mimetypes
from flask import Response


class VideoHandler(object):

    MB = 1 << 20
    BUFF_SIZE = 10 * MB

    def __init__(self, file_path):
        self.file_path = file_path

    def get_response(self, start, end=None):
        file_size = os.path.getsize(self.file_path)

        # Determine (end, length)
        if end is None:
            end = start + VideoHandler.BUFF_SIZE - 1

        end = min(end, file_size - 1)
        end = min(end, start + VideoHandler.BUFF_SIZE - 1)

        length = end - start + 1

        # Read file
        with open(self.file_path, 'rb') as file:
            file.seek(start)
            file_content = file.read(length)

        assert len(file_content) == length

        response = Response(
            file_content,
            206,
            mimetype=mimetypes.guess_type(self.file_path)[0],
            direct_passthrough=True,
        )

        response.headers.add(f'Content-Range', 'bytes {start}-{end}/{file_size}')
        response.headers.add('Accept-Ranges', 'bytes')

        return response

    @staticmethod
    def get_range(request):
        if 'Range' in request.headers:
            m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', request.headers['Range'])
            if m:
                start = int(m.group('start'))
                end = int(m.group('end')) if m.group('end') else None
                return start, end

        return 0, None
