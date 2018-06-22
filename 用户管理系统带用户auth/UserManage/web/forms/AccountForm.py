#!/usr/bin/env python
#coding:utf-8

from django import forms

# LoginForm是随便定义的，但是必须继承forms.Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=10)
    # widget 是控件，意思是用什么展示
    password = forms.CharField(max_length=10,widget=forms.PasswordInput())
    # email = forms.EmailField(max_length=20)