import argparse
import os
import re
import warnings

from Cryptodome.Cipher import AES
import humanfriendly
import m3u8
from progress.bar import Bar
import requests


__author__ = "Xavier-Lam"
__description__ = "Rips purchased video off r18.com"
__title__ = "r18ripper"
__version__ = "0.1.1"


DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 OPR/74.0.3911.107"
# referrer https://www.r18.com/player?cid=mide00070


class R18M3U8Client(m3u8.DefaultHTTPClient):
    def __init__(self, session):
        self.session = session

    def download(self, uri, timeout=None, headers={}, verify_ssl=True):
        resp = self.session.get(uri, timeout=timeout, headers=headers)
        return resp.text, resp.url


class R18Ripper:
    def __init__(self, session):
        self.session = session
        self.client = R18M3U8Client(session)

    def get_versions(self, uri):
        return self.m3u8_load(uri).playlists

    def get_segments(self, uri, bandwidth=None):
        m3u8_obj = self.m3u8_load(uri)
        if m3u8_obj.is_variant:
            versions = m3u8_obj.playlists
            if bandwidth:
                versions = [v for v in versions
                            if v.stream_info.bandwidth == bandwidth]
                if not versions:
                    availables = [v.stream_info.bandwidth
                                  for v in m3u8_obj.playlists]
                    raise ValueError("couldn't find target bandwidth,"
                                     "available choices are: "
                                      + ",".join(map(str, availables)))
            m3u8_obj = self.m3u8_load(versions[-1].absolute_uri)
        else:
            if bandwidth:
                warnings.warn("bandwidth argument has been ignored")
        return m3u8_obj.segments

    def get_stream(self, segments):
        for seg in segments:
            yield self.get_data(seg)

    def get_data(self, seg):
        resp = self.session.get(seg.absolute_uri)
        if seg.key:
            not hasattr(seg.key, "data") and self._load_key(seg.key)
            cipher = getattr(seg.key, "cipher", None)
            if not cipher:
                iv = self._create_init_iv(seg)
                cipher = AES.new(seg.key.data, AES.MODE_CBC, iv)
            return cipher.decrypt(resp.content)
        else:
            return resp.content

    def _load_key(self, key):
        resp = self.session.get(key.absolute_uri)
        key.data = resp.content
        if key.iv:
            key.cipher = AES.new(key.data, AES.MODE_CBC, key.iv)
        return key

    def _create_init_iv(self, seg):
        match = re.search(r"_(\d+)\.ts$", seg.uri)
        idx = int(match.group(1))
        return idx.to_bytes(16, "big")

    def m3u8_load(self, uri, headers={}):
        return m3u8.load(uri, http_client=self.client, headers={})


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("uri", help="m3u8 stream address")
    parser.add_argument("-b", "--bandwidth", required=False,
                        help="choose the bandwidth of the stream")
    parser.add_argument("-o", "--output-file", required=True)
    parser.add_argument("--proxy", required=False,
                        help="using a proxy to get stream")
    parser.add_argument("-r", "--raw", action="store_true",
                        help="save raw ts files to disk")
    parser.add_argument("-s", "--slice",
                        help="")
    parser.add_argument("--trusted-proxy", action="store_true",
                        help="ignore server certification errors when using a proxy")
    parser.add_argument("-u", "--user-agent", default=DEFAULT_USER_AGENT,
                        help="customize user-agent string")
    return parser


def create_session(session=None, *, user_agent=DEFAULT_USER_AGENT,
                   proxies=None, trusted_proxy=False):
    session = session or requests.Session()
    headers = {"User-Agent": user_agent}
    session.headers.update(headers)
    if proxies:
        session.proxies.update(proxies)
        if trusted_proxy:
            session.verify = False
    return session


def main():
    parser = get_parser()
    args = parser.parse_args()

    options = dict(
        user_agent=args.user_agent
    )
    if args.proxy:
        options["proxies"] = {"http": args.proxy, "https": args.proxy}
    if args.trusted_proxy:
        options["trusted_proxy"] = True

    bandwidth = None
    if args.bandwidth:
        bandwidth = humanfriendly.parse_size(args.bandwidth)

    slice = args.slice
    start, end = 0, -1
    if slice:
        seg_start, seg_end = slice.split(":", maxsplit=2)
        if seg_start:
            start = int(seg_start)
        if seg_end:
            end = int(seg_end)

    session = create_session(**options)
    ripper = R18Ripper(session)
    segments = ripper.get_segments(args.uri, bandwidth)[start: end]
    progress_bar = Bar(max=len(segments))

    if args.raw:
        os.path.exists(args.output_file) or os.mkdir(args.output_file)
        i = start
        for seg in segments:
            filename = "{0:06d}.ts".format(i)
            i += 1
            with open(os.path.join(args.output_file, filename), "wb") as f:
                content = ripper.get_data(seg)
                f.write(content)
                progress_bar.next()
    else:
        with open(args.output_file, "wb") as f:
            for content in ripper.get_stream(segments):
                f.write(content)
                progress_bar.next()

    progress_bar.finish()


if "__main__" == __name__:
    main()
