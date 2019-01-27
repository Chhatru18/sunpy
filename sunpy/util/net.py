"""
This module provides general net utility functions.
"""
import os
import re
import sys
import shutil
from unicodedata import normalize
from email.parser import FeedParser
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

from sunpy.util import replacement_filename

__all__ = ['slugify', 'get_content_disposition', 'get_filename',
           'get_system_filename', 'get_system_filename_slugify',
           'download_file', 'download_fileobj', 'check_download_file',
           'url_exists']

# Characters not allowed in slugified version.
_punct_re = re.compile(r'[:\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'_', encoding="ascii"):
    """
    Slugify given unicode text.
    """
    text = normalize('NFKD', text)

    period = '.'

    name_and_extension = text.rsplit(period, 1)
    name = name_and_extension[0]

    name = str(delim).join(
        filter(None, (word for word in _punct_re.split(name.lower()))))

    if len(name_and_extension) == 2:
        extension = name_and_extension[1]
        return str(period).join([name, extension])
    else:
        return name


def get_content_disposition(content_disposition):
    """
    Get content disposition filename from given header.

    Do not include "Content-Disposition:". Returns a unicode string!
    """
    parser = FeedParser()
    parser.feed('Content-Disposition: ' + content_disposition)
    name = parser.close().get_filename()
    if not isinstance(name, str):
        name = name.decode('latin1', 'ignore')
    return name


def get_filename(sock, url):
    """
    Get filename from given urllib2.urlopen object and URL.

    First, tries Content-Disposition, if unavailable, extracts name from URL.
    """
    name = None
    # NOTE: This gives bytes on 2 and unicode on 3.
    # How does 3.x know the encoding?
    cd = sock.headers.get('Content-Disposition', None)
    if cd is not None:
        try:
            name = get_content_disposition(cd)
        except IndexError:
            pass

    if not name:
        parsed = urlparse(url)
        name = parsed.path.rstrip('/').rsplit('/', 1)[-1]
    return str(name)


def get_system_filename(sock, url, default="file"):
    """
    Get filename from given urllib2.urlopen object and URL.

    First, attempts to extract Content-Disposition, second, extract from URL, eventually fall back
    to default. Returns bytestring in file system encoding.
    """
    name = get_filename(sock, url)
    if not name:
        name = str(default)
    return name.encode(sys.getfilesystemencoding(), 'ignore')


def get_system_filename_slugify(sock, url, default="file"):
    """
    Get filename from given urllib2.urlopen object and URL.

    First, attempts to extract Content-Disposition, second, extract from URL, eventually fall back
    to default. Returns bytestring in file system encoding, normalized so it shouldn't violate
    operating system restrictions.
    """
    return slugify(get_system_filename(sock, url, default))


def download_file(url, directory, default="file", overwrite=False):
    """
    Download file from url into directory.

    Try to get filename from Content-Disposition header, otherwise get from path of url. Fall back
    to default if both fail. Only overwrite existing files when overwrite is True.
    """
    opn = urlopen(url)
    try:
        path = download_fileobj(opn, directory, url, default, overwrite)
    finally:
        opn.close()
    return path


def download_fileobj(opn, directory, url='', default="file", overwrite=False):
    """
    Download file from url into directory.

    Try to get filename from Content-Disposition header, otherwise get from path of url if given.
    Fall back to default if both fail. Only overwrite existing files when overwrite is True.
    """
    filename = get_system_filename(opn, url, default)
    path = os.path.join(directory, filename.decode('utf-8'))
    if not overwrite and os.path.exists(path):
        path = replacement_filename(path)
    with open(path, 'wb') as fd:
        shutil.copyfileobj(opn, fd)
    return path


def check_download_file(filename, remotepath, download_dir, remotename=None,
                        replace=False):
    """
    Downloads a file from remotepath to localpath if it isn't there.

    This function checks whether a file with name filename exists in the
    location, localpath, on the user's local machine.  If it doesn't,
    it downloads the file from remotepath.

    Parameters
    ----------
    filename : `str`
        Name of file.
    remotepath : `str`
        URL of the remote location from which filename can be downloaded.
    download_dir : `str`
        The files directory.
    remotename : `str`, optional
        filename under which the file is stored remotely.
        Default is same as filename.
    replace : `bool`, optional
        If True, file will be downloaded whether or not file already exists
        locally.

    Examples
    --------
    >>> from sunpy.util.net import check_download_file
    >>> remotepath = "http://www.download_repository.com/downloads/"
    >>> check_download_file("filename.txt", remotepath, download_dir='.')   # doctest: +SKIP
    """
    # Check if file already exists locally.  If not, try downloading it.
    if replace or not os.path.isfile(os.path.join(download_dir, filename)):
        # set local and remote file names be the same unless specified
        # by user.
        if not isinstance(remotename, str):
            remotename = filename

        download_file(urljoin(remotepath, remotename),
                      download_dir, default=filename, overwrite=replace)


def url_exists(url, timeout=2):
    """
    Checks whether a url is online.

    Parameters
    ----------
    url: `str`
        A string containing a URL

    Returns
    -------
    value: `bool`
        If the url exists, it is `True`.
        If not, it is `False`.

    Examples
    --------
    >>> from sunpy.util.net import url_exists
    >>> url_exists('http://www.google.com')  #doctest: +REMOTE_DATA
    True
    >>> url_exists('http://aslkfjasdlfkjwerf.com')  #doctest: +REMOTE_DATA
    False
    """
    try:
        urlopen(url, timeout=timeout)
    except HTTPError:
        return False
    except URLError:
        return False
    else:
        return True


def is_online():
    """
    Checks whether an internet connection is available.

    Returns
    -------
    value: `bool`
        If online, it is `True`.
        If not, it is `False`.

    Examples
    --------
    >>> from sunpy.util.net import is_online
    >>> is_online()  #doctest: +REMOTE_DATA
    True
    """
    return url_exists('http://www.google.com')
