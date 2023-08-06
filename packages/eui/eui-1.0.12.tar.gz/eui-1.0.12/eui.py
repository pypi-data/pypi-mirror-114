"""
eui means easy UI. It is a fast and simple micro-framework for small browser-based applications.
Python and JS communicate through websocket protocol.
"""

import base64
import hashlib
import json
import logging
import os
import queue
import random
import socket
import struct
import threading
import time
from concurrent import futures

log = logging.getLogger('eui')
_SEND_QUEUE = queue.Queue()
PORT = None
HANDLERS = {}
_WORKERS = None
_MAX_RECEIVE_MESSAGE_SIZE = 1 * 1024 * 1024
_ws_connection = None
_TIMEOUT = None
_ttl = 30

_CONTENT_TYPE_DICT = {'.*': 'application/octet-stream', '.001': 'application/x-001', '.301': 'application/x-301',
                      '.323': 'text/h323', '.906': 'application/x-906', '.907': 'drawing/907',
                      '.a11': 'application/x-a11', '.acp': 'audio/x-mei-aac', '.ai': 'application/postscript',
                      '.aif': 'audio/aiff', '.aifc': 'audio/aiff', '.aiff': 'audio/aiff', '.anv': 'application/x-anv',
                      '.asa': 'text/asa', '.asf': 'video/x-ms-asf', '.asp': 'text/asp', '.asx': 'video/x-ms-asf',
                      '.au': 'audio/basic', '.avi': 'video/avi', '.awf': 'application/vnd.adobe.workflow',
                      '.biz': 'text/xml', '.bmp': 'application/x-bmp', '.bot': 'application/x-bot',
                      '.c4t': 'application/x-c4t', '.c90': 'application/x-c90', '.cal': 'application/x-cals',
                      '.cat': 'application/vnd.ms-pki.seccat', '.cdf': 'application/x-netcdf',
                      '.cdr': 'application/x-cdr', '.cel': 'application/x-cel', '.cer': 'application/x-x509-ca-cert',
                      '.cg4': 'application/x-g4', '.cgm': 'application/x-cgm', '.cit': 'application/x-cit',
                      '.class': 'java/*', '.cml': 'text/xml', '.cmp': 'application/x-cmp', '.cmx': 'application/x-cmx',
                      '.cot': 'application/x-cot', '.crl': 'application/pkix-crl', '.crt': 'application/x-x509-ca-cert',
                      '.csi': 'application/x-csi', '.css': 'text/css', '.cut': 'application/x-cut',
                      '.dbf': 'application/x-dbf', '.dbm': 'application/x-dbm', '.dbx': 'application/x-dbx',
                      '.dcd': 'text/xml', '.dcx': 'application/x-dcx', '.der': 'application/x-x509-ca-cert',
                      '.dgn': 'application/x-dgn', '.dib': 'application/x-dib', '.dll': 'application/x-msdownload',
                      '.doc': 'application/msword', '.dot': 'application/msword', '.drw': 'application/x-drw',
                      '.dtd': 'text/xml', '.dwf': 'application/x-dwf', '.dwg': 'application/x-dwg',
                      '.dxb': 'application/x-dxb', '.dxf': 'application/x-dxf', '.edn': 'application/vnd.adobe.edn',
                      '.emf': 'application/x-emf', '.eml': 'message/rfc822', '.ent': 'text/xml',
                      '.epi': 'application/x-epi', '.eps': 'application/postscript', '.etd': 'application/x-ebx',
                      '.exe': 'application/x-msdownload', '.fax': 'image/fax', '.fdf': 'application/vnd.fdf',
                      '.fif': 'application/fractals', '.fo': 'text/xml', '.frm': 'application/x-frm',
                      '.g4': 'application/x-g4', '.gbr': 'application/x-gbr', '.gcd': 'application/x-gcd',
                      '.gif': 'image/gif', '.gl2': 'application/x-gl2', '.gp4': 'application/x-gp4',
                      '.hgl': 'application/x-hgl', '.hmr': 'application/x-hmr', '.hpg': 'application/x-hpgl',
                      '.hpl': 'application/x-hpl', '.hqx': 'application/mac-binhex40', '.hrf': 'application/x-hrf',
                      '.hta': 'application/hta', '.htc': 'text/x-component', '.htm': 'text/html', '.html': 'text/html',
                      '.htt': 'text/webviewhtml', '.htx': 'text/html', '.icb': 'application/x-icb',
                      '.ico': 'application/x-ico', '.iff': 'application/x-iff', '.ig4': 'application/x-g4',
                      '.igs': 'application/x-igs', '.iii': 'application/x-iphone', '.img': 'application/x-img',
                      '.ins': 'application/x-internet-signup', '.isp': 'application/x-internet-signup',
                      '.IVF': 'video/x-ivf', '.java': 'java/*', '.jfif': 'image/jpeg', '.jpe': 'application/x-jpe',
                      '.jpeg': 'image/jpeg', '.jpg': 'application/x-jpg', '.js': 'application/x-javascript',
                      '.jsp': 'text/html', '.la1': 'audio/x-liquid-file', '.lar': 'application/x-laplayer-reg',
                      '.latex': 'application/x-latex', '.lavs': 'audio/x-liquid-secure', '.lbm': 'application/x-lbm',
                      '.lmsff': 'audio/x-la-lms', '.ls': 'application/x-javascript', '.ltr': 'application/x-ltr',
                      '.m1v': 'video/x-mpeg', '.m2v': 'video/x-mpeg', '.m3u': 'audio/mpegurl', '.m4e': 'video/mpeg4',
                      '.mac': 'application/x-mac', '.man': 'application/x-troff-man', '.math': 'text/xml',
                      '.mdb': 'application/x-mdb', '.mfp': 'application/x-shockwave-flash', '.mht': 'message/rfc822',
                      '.mhtml': 'message/rfc822', '.mi': 'application/x-mi', '.mid': 'audio/mid', '.midi': 'audio/mid',
                      '.mil': 'application/x-mil', '.mml': 'text/xml', '.mnd': 'audio/x-musicnet-download',
                      '.mns': 'audio/x-musicnet-stream', '.mocha': 'application/x-javascript',
                      '.movie': 'video/x-sgi-movie', '.mp1': 'audio/mp1', '.mp2': 'audio/mp2', '.mp2v': 'video/mpeg',
                      '.mp3': 'audio/mp3', '.mp4': 'video/mpeg4', '.mpa': 'video/x-mpg',
                      '.mpd': 'application/vnd.ms-project', '.mpe': 'video/x-mpeg', '.mpeg': 'video/mpg',
                      '.mpg': 'video/mpg', '.mpga': 'audio/rn-mpeg', '.mpp': 'application/vnd.ms-project',
                      '.mps': 'video/x-mpeg', '.mpt': 'application/vnd.ms-project', '.mpv': 'video/mpg',
                      '.mpv2': 'video/mpeg', '.mpw': 'application/vnd.ms-project', '.mpx': 'application/vnd.ms-project',
                      '.mtx': 'text/xml', '.mxp': 'application/x-mmxp', '.net': 'image/pnetvue',
                      '.nrf': 'application/x-nrf', '.nws': 'message/rfc822', '.odc': 'text/x-ms-odc',
                      '.out': 'application/x-out', '.p10': 'application/pkcs10', '.p12': 'application/x-pkcs12',
                      '.p7b': 'application/x-pkcs7-certificates', '.p7c': 'application/pkcs7-mime',
                      '.p7m': 'application/pkcs7-mime', '.p7r': 'application/x-pkcs7-certreqresp',
                      '.p7s': 'application/pkcs7-signature', '.pc5': 'application/x-pc5', '.pci': 'application/x-pci',
                      '.pcl': 'application/x-pcl', '.pcx': 'application/x-pcx', '.pdf': 'application/pdf',
                      '.pdx': 'application/vnd.adobe.pdx', '.pfx': 'application/x-pkcs12', '.pgl': 'application/x-pgl',
                      '.pic': 'application/x-pic', '.pko': 'application/vnd.ms-pki.pko', '.pl': 'application/x-perl',
                      '.plg': 'text/html', '.pls': 'audio/scpls', '.plt': 'application/x-plt',
                      '.png': 'application/x-png', '.pot': 'application/vnd.ms-powerpoint',
                      '.ppa': 'application/vnd.ms-powerpoint', '.ppm': 'application/x-ppm',
                      '.pps': 'application/vnd.ms-powerpoint', '.ppt': 'application/x-ppt', '.pr': 'application/x-pr',
                      '.prf': 'application/pics-rules', '.prn': 'application/x-prn', '.prt': 'application/x-prt',
                      '.ps': 'application/postscript', '.ptn': 'application/x-ptn',
                      '.pwz': 'application/vnd.ms-powerpoint', '.r3t': 'text/vnd.rn-realtext3d',
                      '.ra': 'audio/vnd.rn-realaudio', '.ram': 'audio/x-pn-realaudio', '.ras': 'application/x-ras',
                      '.rat': 'application/rat-file', '.rdf': 'text/xml', '.rec': 'application/vnd.rn-recording',
                      '.red': 'application/x-red', '.rgb': 'application/x-rgb',
                      '.rjs': 'application/vnd.rn-realsystem-rjs', '.rjt': 'application/vnd.rn-realsystem-rjt',
                      '.rlc': 'application/x-rlc', '.rle': 'application/x-rle', '.rm': 'application/vnd.rn-realmedia',
                      '.rmf': 'application/vnd.adobe.rmf', '.rmi': 'audio/mid',
                      '.rmj': 'application/vnd.rn-realsystem-rmj', '.rmm': 'audio/x-pn-realaudio',
                      '.rmp': 'application/vnd.rn-rn_music_package', '.rms': 'application/vnd.rn-realmedia-secure',
                      '.rmvb': 'application/vnd.rn-realmedia-vbr', '.rmx': 'application/vnd.rn-realsystem-rmx',
                      '.rnx': 'application/vnd.rn-realplayer', '.rp': 'image/vnd.rn-realpix',
                      '.rpm': 'audio/x-pn-realaudio-plugin', '.rsml': 'application/vnd.rn-rsml',
                      '.rt': 'text/vnd.rn-realtext', '.rtf': 'application/x-rtf', '.rv': 'video/vnd.rn-realvideo',
                      '.sam': 'application/x-sam', '.sat': 'application/x-sat', '.sdp': 'application/sdp',
                      '.sdw': 'application/x-sdw', '.sit': 'application/x-stuffit', '.slb': 'application/x-slb',
                      '.sld': 'application/x-sld', '.slk': 'drawing/x-slk', '.smi': 'application/smil',
                      '.smil': 'application/smil', '.smk': 'application/x-smk', '.snd': 'audio/basic',
                      '.sol': 'text/plain', '.sor': 'text/plain', '.spc': 'application/x-pkcs7-certificates',
                      '.spl': 'application/futuresplash', '.spp': 'text/xml', '.ssm': 'application/streamingmedia',
                      '.sst': 'application/vnd.ms-pki.certstore', '.stl': 'application/vnd.ms-pki.stl',
                      '.stm': 'text/html', '.sty': 'application/x-sty', '.svg': 'text/xml',
                      '.swf': 'application/x-shockwave-flash', '.tdf': 'application/x-tdf', '.tg4': 'application/x-tg4',
                      '.tga': 'application/x-tga', '.tif': 'application/x-tif', '.tiff': 'image/tiff',
                      '.tld': 'text/xml', '.top': 'drawing/x-top', '.torrent': 'application/x-bittorrent',
                      '.tsd': 'text/xml', '.txt': 'text/plain', '.uin': 'application/x-icq', '.uls': 'text/iuls',
                      '.vcf': 'text/x-vcard', '.vda': 'application/x-vda', '.vdx': 'application/vnd.visio',
                      '.vml': 'text/xml', '.vpg': 'application/x-vpeg005', '.vsd': 'application/x-vsd',
                      '.vss': 'application/vnd.visio', '.vst': 'application/x-vst', '.vsw': 'application/vnd.visio',
                      '.vsx': 'application/vnd.visio', '.vtx': 'application/vnd.visio', '.vxml': 'text/xml',
                      '.wav': 'audio/wav', '.wax': 'audio/x-ms-wax', '.wb1': 'application/x-wb1',
                      '.wb2': 'application/x-wb2', '.wb3': 'application/x-wb3', '.wbmp': 'image/vnd.wap.wbmp',
                      '.wiz': 'application/msword', '.wk3': 'application/x-wk3', '.wk4': 'application/x-wk4',
                      '.wkq': 'application/x-wkq', '.wks': 'application/x-wks', '.wm': 'video/x-ms-wm',
                      '.wma': 'audio/x-ms-wma', '.wmd': 'application/x-ms-wmd', '.wmf': 'application/x-wmf',
                      '.wml': 'text/vnd.wap.wml', '.wmv': 'video/x-ms-wmv', '.wmx': 'video/x-ms-wmx',
                      '.wmz': 'application/x-ms-wmz', '.wp6': 'application/x-wp6', '.wpd': 'application/x-wpd',
                      '.wpg': 'application/x-wpg', '.wpl': 'application/vnd.ms-wpl', '.wq1': 'application/x-wq1',
                      '.wr1': 'application/x-wr1', '.wri': 'application/x-wri', '.wrk': 'application/x-wrk',
                      '.ws': 'application/x-ws', '.ws2': 'application/x-ws', '.wsc': 'text/scriptlet',
                      '.wsdl': 'text/xml', '.wvx': 'video/x-ms-wvx', '.xdp': 'application/vnd.adobe.xdp',
                      '.xdr': 'text/xml', '.xfd': 'application/vnd.adobe.xfd', '.xfdf': 'application/vnd.adobe.xfdf',
                      '.xhtml': 'text/html', '.xls': 'application/x-xls', '.xlw': 'application/x-xlw',
                      '.xml': 'text/xml', '.xpl': 'audio/scpls', '.xq': 'text/xml', '.xql': 'text/xml',
                      '.xquery': 'text/xml', '.xsd': 'text/xml', '.xsl': 'text/xml', '.xslt': 'text/xml',
                      '.xwd': 'application/x-xwd', '.x_b': 'application/x-x_b', '.x_t': 'application/x-x_t'}

# eui.js code template
_JS_TEMPLATE = '''/**
* This file is automatically generated every time eui starts. Please do not modify it manually.
 */
window.eui = {};
eui.retryTimes = 10;

eui.init = function () {
   eui.ws = new WebSocket("ws://localhost:%s");
   eui.ws.onopen = function () {
      console.log('connect to eui server!');
      eui.retryTimes = 10;
   };

   eui.ws.onmessage = function (evt) {
      //heartbeat
      if (evt.data == 'pong') { return }
      try {
         var data = JSON.parse(evt.data);
         var handler = eval(data['handler']);
         if (typeof handler != 'function') {
            eui.onerror(data['handler'] + ' is not a valid function');
            return;
         }
         handler.apply(null, data['args']);
      } catch (e) {
         eui.onerror(e);
      }
   };

   eui.ws.onclose = function () {};

   eui.ws.onerror = function () {};

}

/**
* It is used to execute Python handler. 
* 
* @param {string} handler Python handler
* @param {...} ...args args for Python handler. If there are multiple args, separate them with commas.
*/
eui.py = function (handler, ...args) {
  if (eui.ws.readyState != 1) {
     setTimeout(eui.py, 100, handler, ...args);
  } else {
     eui.ws.send(JSON.stringify({ 'handler': handler, 'args': args }));
  }
};

/**
* Default error handler. It will be executed when an exception occurs and can be overridden if necessary.
* 
* @param {string} e error message
*/
eui.onerror = function (e) {
  alert(e);
  console.error(e);
};

/**
* exit app
* 
* @param {code} error code
*/
eui.exit = function (code) {
  eui.py('_exit', 0);
};

if ('WebSocket' in window) {
   eui.init();
   //send heartbeat
   setInterval(() => {
       eui.ws.send('ping');
    }, 6000);
    
    //check connection
    setInterval(() => {
       if (eui.retryTimes <= 0) {
          window.close();
       } else if (eui.ws && eui.ws.readyState > 1) {
          console.log('connection closed, retry init...');
          eui.retryTimes -= 1;
          eui.init();
       }
    }, 3000);
} else {
   alert("your browser don't support WebSocket");
}

'''


def _init_log(file, level):
    """
    init log config
    :param file: log file
    :param level: log level
    :return:
    """
    log.setLevel(level)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(pathname)s [line:%(lineno)d] %(message)s",
                                  '%Y-%m-%d %H:%M:%S')
    console_log_handler = logging.StreamHandler()
    console_log_handler.setFormatter(formatter)
    file_log_handler = logging.FileHandler(file, mode='w')
    file_log_handler.setFormatter(formatter)

    log.addHandler(console_log_handler)
    log.addHandler(file_log_handler)


def _get_headers(payload):
    """
    get headers from data
    :param payload: received connection message
    :return: headers
    """
    headers = {}
    if not payload:
        return headers
    header_str, body = str(payload, encoding="utf-8").split("\r\n\r\n", 1)
    header_list = header_str.split("\r\n")
    headers['method'], headers['uri'], headers['protocol'] = header_list[0].split(' ')
    for row in header_list[1:]:
        key, value = row.split(":", 1)
        headers[str(key).lower()] = value.strip()

    return headers


def _parse_payload(payload):
    """
    parse payload message

    :param payload: bytes message
    :return: parsed string message
    """
    if not payload:
        return ''
    payload_len = payload[1] & 127
    if payload_len == 126:
        mask = payload[4:8]
        decoded = payload[8:]

    elif payload_len == 127:
        mask = payload[10:14]
        decoded = payload[14:]
    else:
        mask = payload[2:6]
        decoded = payload[6:]

    byte_list = bytearray()
    for i, b in enumerate(decoded):
        chunk = b ^ mask[i % 4]
        byte_list.append(chunk)
    # connection close
    if byte_list == bytearray(b'\x03\xe9'):
        return ''

    return str(byte_list, encoding='utf-8')


def _init_js(static_dir):
    """
    generate js file

    :param static_dir: dir for eui.js
    :return:
    """
    os.makedirs(static_dir, exist_ok=True)
    path = (static_dir if static_dir.endswith('/') else static_dir + '/') + 'eui.js'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_JS_TEMPLATE % PORT)
    log.debug('init js path: %s', path)


def _task(handler, args):
    """
    task is a handler wrapper to execute handler with Exception handling
    :param handler: target handler
    :param args: handler args
    :return:
    """
    try:
        if args:
            handler(*args)
        else:
            handler()
    except Exception as e:
        raise_ui_error(str(e), e)


def _startup_receive_message_worker():
    """
    startup a worker to receive message

    """

    def run():
        global _ttl
        while True:
            try:
                payload = _ws_connection.recv(_MAX_RECEIVE_MESSAGE_SIZE)
                parsed_payload = _parse_payload(payload)
                # connection close
                if not parsed_payload:
                    time.sleep(0.1)
                    continue
                log.debug('payload: %s', parsed_payload)
                # heart beat, reset ttl
                if parsed_payload == 'ping':
                    _ttl = _TIMEOUT
                    _send_message(b'pong')
                    continue
                # parse json data
                data = json.loads(parsed_payload)
                handler_name = data.get('handler', '')
                if handler_name not in HANDLERS:
                    raise_ui_error(
                        "handler '%s' not found, please check Python handlers config" % handler_name)
                    continue
                handler = HANDLERS[handler_name]
                args = data.get('args', None)
                _WORKERS.submit(_task, handler, args)
            except ConnectionAbortedError:
                log.warning('connection aborted')
                time.sleep(1)
            except Exception as e:
                log.warning('receive message error', exc_info=e)

    # send message worker is a daemon thread
    send_thread = threading.Thread(target=run)
    send_thread.setDaemon(True)
    send_thread.start()


def _send_message(message_bytes):
    """send message to ui"""
    try:
        token = b"\x81"
        length = len(message_bytes)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)

        msg = token + message_bytes
        _ws_connection.sendall(msg)
    except ConnectionAbortedError:
        pass
    except Exception as e:
        log.error('send message error: %s', str(e), exc_info=e)


def _startup_send_message_worker():
    """
    startup a worker to send message

    """

    def run():
        while True:
            try:
                data = _SEND_QUEUE.get().encode('utf-8')
                _send_message(data)
            except Exception as e:
                log.error('eui send message error: %s', str(e), exc_info=e)

    # send message worker is a daemon thread
    send_thread = threading.Thread(target=run)
    send_thread.setDaemon(True)
    send_thread.start()


def _startup_callback(fn):
    """
    startup callback function, when eui startup, fn will be execute
    :param fn: callback function
    :return:
    """
    if not fn:
        return
    callback_thread = threading.Thread(target=fn)
    callback_thread.setDaemon(True)
    callback_thread.start()


def _startup_timeout_checker():
    """
    startup a worker to check timeout event
    """
    if not _TIMEOUT:
        return

    def run():
        global _ttl
        while True:
            if _ttl <= 0:
                log.info('wait for connection timeout, eui will exit!')
                _exit(-1)
            _ttl -= 1
            time.sleep(1)

    t = threading.Thread(target=run)
    t.setDaemon(True)
    t.start()


def raise_ui_error(error_message, error=None):
    """
    send error message to js
    :param error_message: error message
    :param error: error object
    :return:
    """
    log.error(error_message, exc_info=error)
    js('eui.onerror', error_message)


def js(handler, *args):
    """
    call js function

    :param handler: js function
    :param args: js function args
    :return:
    """
    _SEND_QUEUE.put(json.dumps({'handler': handler, 'args': args}, ensure_ascii=True))


def _dispatch_connection(connection):
    """
    dispatch connection to websocket or HTTP handler
    :param connection: connection
    :return:
    """
    payload = connection.recv(_MAX_RECEIVE_MESSAGE_SIZE)
    headers = _get_headers(payload)
    if not headers:
        connection.sendall(b"HTTP/1.1 200 OK")
        connection.close()
        return

    # websocket connection
    global _ws_connection
    if headers.get('upgrade', '').lower() == 'websocket':
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade: websocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: %s\r\n" \
                       "WebSocket-Location: ws://%s\r\n\r\n"

        value = ''
        if headers.get('sec-websocket-key'):
            value = headers['sec-websocket-key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response = response_tpl % (ac.decode('utf-8'), headers.get("host"))
        connection.sendall(bytes(response, encoding="utf-8"))

        # if workers have not been initialized, initialize workers
        if _ws_connection is None:
            _ws_connection = connection
            # startup workers
            _startup_receive_message_worker()
            _startup_send_message_worker()
        else:  # have been initialized
            _ws_connection.close()
            _ws_connection = connection

    else:  # HTTP connection
        path = '.' + headers.get('uri', '')
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'rb') as f:
                data = f.read()
                response = "HTTP/1.1 200 OK\r\n" \
                           "Content-Type: %s\r\n" \
                           "Content-Length: %s\r\n\r\n" % (
                    _CONTENT_TYPE_DICT.get(os.path.splitext(path)[1], '.*'), len(data))
                connection.sendall(bytes(response, encoding='utf-8') + data)
        else:
            log.error("can't read file '%s'", path)
            connection.sendall(b"HTTP/1.1 404 Not Found")
        connection.close()


def start(host="0.0.0.0", port=None, handlers=None, static_dir='./static', startup_callback=None, max_workers=10,
          timeout=None, log_file='eui.log', log_level='DEBUG'):
    """
    start eui

    :param host: host
    :param port: port, if port is None, port will be a random int value
    :param handlers: python function for js call
    :param static_dir: dir for output eui.js
    :param startup_callback: the function after eui startup to run
    :param max_workers: max workers to execute handlers
    :param timeout: max seconds to wait for heartbeat
    :param log_file: log file path
    :param log_level: log level, 'CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
    :return:
    """

    global PORT, HANDLERS, _WORKERS, _TIMEOUT

    # init log
    _init_log(log_file, log_level)

    # init port
    if port is None:
        port = random.randint(5000, 60000)
    PORT = port

    # init handlers
    if handlers:
        HANDLERS = handlers
    HANDLERS['_exit'] = _exit

    # init js file
    _init_js(static_dir)

    # init workers
    _WORKERS = futures.ThreadPoolExecutor(max_workers=max_workers)

    # init timeout
    _TIMEOUT = timeout

    # init socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, PORT))
    sock.listen(6)

    # startup callback function
    _startup_callback(startup_callback)
    # startup timeout checker
    _startup_timeout_checker()
    print('******************** eui start up at port %s ********************' % PORT)

    # accept connection
    while True:
        try:
            connection, addr = sock.accept()
            _WORKERS.submit(_dispatch_connection, connection)
        except Exception as e:
            log.error('connect error', exc_info=e)


def _exit(code=0):
    """
    exit process
    :param code: error code
    :return:
    """
    _send_message(json.dumps({'handler': 'window.close'}).encode('utf-8'))
    os._exit(code)
