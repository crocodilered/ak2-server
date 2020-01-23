import os
import re
import mimetypes
from flask import Flask, Response, request


MB = 1 << 20
BUFF_SIZE = 10 * MB

app = Flask(__name__)


def partial_response(path, start, end=None):
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)

    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)

    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    return response


def get_range(req):
    if 'Range' in req.headers:
        m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', req.headers['Range'])
        if m:
            start = int(m.group('start'))
            end = int(m.group('end')) if m.group('end') else None
            return start, end

    return 0, None


@app.route('/s.mp4')
def stream():
    file_path = 'video.mp4'
    start, end = get_range(request)
    return partial_response(file_path, start, end)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
