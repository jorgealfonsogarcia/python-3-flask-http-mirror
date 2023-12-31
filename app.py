# MIT License
# 
# COPYRIGHT (c) 2023 Jorge Garcia
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import datetime, timezone
from flask import Flask, request, jsonify
import tzlocal

app = Flask(__name__)

@app.after_request
def set_security_headers(response):
    """
    Sets security headers for the HTTP response.

    Args:
        response (flask.Response): The HTTP response object.

    Returns:
        flask.Response: The HTTP response object with security headers set.
    """
    csp_policy = (
        "default-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self';"
    )
    response.headers['Content-Security-Policy'] = csp_policy

    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers["Cache-Control"] = "max-age=0, must-revalidate, no-cache, no-store, private"

    return response


@app.route('/mirror', methods=['GET', 'POST', 'PUT', 'DELETE'])
def http_mirror():
    """
    Returns a JSON object containing information about the incoming HTTP request.

    Returns:
        A JSON object containing the following information:
        - datetime: The current date and time in ISO format.
        - method: The HTTP method used in the request.
        - url: The URL of the request.
        - headers: A dictionary containing the headers of the request.
        - args: A dictionary containing the query string parameters of the request.
        - form: A dictionary containing the form data of the request.
        - data: The raw data of the request.
        - cookies: A dictionary containing the cookies of the request.
        - files: A dictionary containing the files uploaded in the request.
        - json: The JSON data of the request.
        - referrer: The referrer of the request.
        - remote_addr: The IP address of the client making the request.
        - scheme: The URL scheme of the request.
        - user_agent: The user agent of the client making the request.
        - environ: A dictionary containing the environment variables of the request.
    """
    return jsonify({
        'datetime': datetime.now(tzlocal.get_localzone()).isoformat(),
        'method': request.method,
        'url': request.url,
        'headers': {k: v for k, v in request.headers.items() if k not in ['X-Forwarded-For']},
        'args': dict(request.args),
        'form': dict(request.form),
        'data': request.data.decode('utf-8'),
        'cookies': request.cookies,
        'files': dict(request.files),
        'json': request.json if request.content_type == 'application/json' else None,
        'referrer': request.referrer,
        'scheme': request.scheme,
        'user_agent': request.user_agent.string,
        'environ': {k: v for k, v in request.environ.items() if isinstance(v, (str, int, float, list, dict, bool)) \
                    and k not in ['REMOTE_ADDR', 'REMOTE_PORT', 'SERVER_SOFTWARE', 'HTTP_X_FORWARDED_FOR']}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
