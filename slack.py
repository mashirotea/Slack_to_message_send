import os
import json
import sys
import urllib.request
import dataclasses
from dataclasses import field
from typing import List

#### Slack関連のクラス
class Slack():
    def __init__(self, attributes = None):
        if attributes is dataclasses.is_dataclass(attributes):
            self.attributes = attributes
        else:
            self.attributes = SlackInfo()

    def post(self):
        req = urllib.request.Request(
            self.attributes.url,
            data=json.dumps(self.attributes.data).encode('utf-8'),
            method='POST', 
            headers=self.attributes.headers
        )
        urllib.request.urlopen(req)

#### Slackにメッセージを送る上で必要なデータ軍
@dataclasses.dataclass
class SlackInfo:
    ## URL
    url: str = 'https://slack.com/api/chat.postMessage'
    
    ## HEADER
    content_type:       str = 'application/json; charset=UTF-8'
    headers:      List[str] = field(default_factory=list, compare=False)
    user_token:         str = "SLACK_BOT_USER_ACCESS_TOKEN"

    ## CONTENTS
    data:         List[str] = field(default_factory=list, compare=False)
    token:              str = "SLACK_BOT_VERIFY_TOKEN"
    channel:            str = "SLACK_CHANNEL"
    text:               str = ''
    response_type:      str = 'in_channel'
    replace_original:   str = 'true'
    
    ## MESSAGES
    attachments:  List[str] = field(default_factory=list, compare=False)
    message:            str = ''
    fallback:           str = ''
    callback_id:        str = ''
    color:              str = '#000000'
    attachment_type:    str = 'default'

    ## MESSAGES ACTIONS
    actions:      List[str] = field(default_factory=list, compare=False)
    
    # データを固める
    def make(self):
        self.headers = {
            'Content-Type': self.content_type,
            'Authorization': 'Bearer {0}'.format(self.user_token)
        }
        self.attachments.append({
            'text': self.message,
            'fallback': self.fallback,
            'callback_id': self.callback_id,
            'color': self.color,
            'attachment_type': self.attachment_type,
            'actions': self.actions
        })
        self.data = {
            'token': self.token,
            'channel': self.channel,
            'text': self.text,
            'response_type': self.response_type,
            'replace_original': self.replace_original,
            'attachments': self.attachments
        }

    # はい, いいえ のボタン作成
    def init_button_yes_no(self, name = 'name'):
        button_action = [{
            'type': 'button',
            'name': name,
            'text': 'はい',
            'value': 'true'
        },
        {
            'type': 'button',
            'name': name,
            'text': 'いいえ',
            'value': 'false'
        }]
        self.actions.extend(button_action)
    
    # 汎用的なボタン作成
    def init_button(self, name = 'name', text = 'text', value = ''):
        button_action = {
            'type': 'button',
            'name': name,
            'text': text,
            'value': value
        }
        self.actions.append(button_action)

    # 汎用的なセレクトボックス作成
    def init_select(self, name = 'name', text = 'text', option = []):
        select_action = {
            'type': 'select',
            'name': name,
            'text': text,
            'options': option
        }
        self.actions.append(select_action)
