# Licensed to Tomaz Muraus under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# Tomaz muraus licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import urllib2
import chardet

from gevent import monkey
from gevent.pool import Pool

monkey.patch_socket()

BASE_URL = 'http://seznami.gov.si/DURS/Neplacniki_files/Html%s.html'
IMAGE_LINK = 'http://seznami.gov.si/DURS/Neplacniki_files/%s'

START_NUM = 0
END_NUM = 326
NUM_LEN = 4

CHUNK_SIZE = 1024 * 64

pool = Pool(30)


def read_page(url):
    response = urllib2.urlopen(url)
    content = response.read()
    encoding = chardet.detect(content)
    content = content.decode(encoding['encoding'])
    return content


def parse_image_links(content):
    content = content
    result = re.findall(r'<img\s+src=\'(.*\.jpg)\'\s+width="\d+"\s+/>',
                        content, re.IGNORECASE)

    if not result:
        return []

    links = [IMAGE_LINK % (name) for name in result]
    return links


def download_file(url, file_name):
    response = urllib2.urlopen(url)

    with open(file_name, 'w') as fp:
        data = response.read(CHUNK_SIZE)

        while data:
            fp.write(data)
            data = response.read(CHUNK_SIZE)


def process_page(i):
    num = str(i)
    padding = NUM_LEN - len(num)
    page_num = padding * '0' + num
    url = BASE_URL % (page_num)

    print 'Downloading images on page %s...' % (i + 1)

    content = read_page(url=url)
    image_links = parse_image_links(content=content)

    for index, url in enumerate(image_links):
        file_name = os.path.join('scraped/', 'page_%s-%s.jpg' % (page_num,
                                                                 index + 1))
        download_file(url, file_name=file_name)

    print 'Images on page %s downloaded' % (i + 1)


def main():
    for i in range(START_NUM, END_NUM):
        pool.spawn(process_page, i)

    pool.join()

main()
