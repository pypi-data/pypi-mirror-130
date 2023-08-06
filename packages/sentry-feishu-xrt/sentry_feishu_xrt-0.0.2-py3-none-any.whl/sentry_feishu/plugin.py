# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_feishu
from .forms import FeiShuOptionsForm

# DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class FeiShuPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to FeiShu.
    """
    author = 'ruitao.xiong'
    # author_url = 'https://github.com/anshengme/sentry-dingding'
    version = sentry_feishu.VERSION
    description = 'Send error counts to FeiShu.'
    # resource_links = [
    #     ('Source', 'https://github.com/anshengme/sentry-dingding'),
    #     ('Bug Tracker', 'https://github.com/anshengme/sentry-dingding/issues'),
    #     ('README', 'https://github.com/anshengme/sentry-dingding/blob/master/README.md'),
    # ]

    slug = 'FeiShu'
    title = 'FeiShu'
    conf_key = slug
    conf_title = title
    project_conf_form = FeiShuOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('webhook_url', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        webhook_url = self.get_option('webhook_url', group.project)

        title = u"{}项目发生报错".format(event.project.slug)
        event_url = u"{}events/{}/".format(group.get_absolute_url(), event.event_id)

        t = "group: \n"
        for i in dir(group): 
            t = t + "{key}: {value} \n".format(
                key = i,
                value = group[i]
            )

        t = t + "event: \n"

        for j in dir(event): 
            t = t + "{key}: {value} \n".format(
                key = j,
                value = event[j]
            )

        data = {
            "title": title,
            "text": t
        }
        requests.post(
            url=webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
