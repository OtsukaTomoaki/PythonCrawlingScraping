import logging
from typing import Tuple

import lxml.html
import readability


#readability-lxmlのDEBUG/INFOレベルのログを表示しないようにする
#Spider実行時にreadability-lxmlのログが大量に表示されて、ログが見づらくなるのを防ぐため
logging.getLogger('readability.readability').setLevel(logging.WARNING)

def get_content(html: str) -> Tuple[str, str]:
    document = readability.Document(html)
    content_html = document.summary()
    #htmlタグを除去して本文のテキストのみを取得する
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    return short_title, content_text