# coding: utf-8

from django import forms


class FeiShuOptionsForm(forms.Form):
    webhook_url = forms.CharField(
        max_length=255,
        help_text='飞书机器人webhook地址'
    )
