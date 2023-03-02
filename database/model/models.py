#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tortoise import fields, models


class baseModel:
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


# 用户的基础属性，对应用户表
class Users(models.Model,baseModel):
    login_name = fields.CharField(max_length=20, unique=False)
    name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=False)
    address = fields.CharField(max_length=128, null=True)
    type = fields.CharField(max_length=50, null=True)
    phone = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=128, null=True)

    class Meta:
        table = "users"
        ordering = ["modified_at"]
        unique_together = (["login_name"])


# 路由设备的基础属性
class Device(models.Model,baseModel):
    dev_id = fields.CharField(max_length=50, null=True)
    host = fields.CharField(max_length=50, null=True)
    type = fields.CharField(max_length=150, null=True)
    status = fields.CharField(max_length=150, null=True)
    id_delete = fields.CharField(max_length=10, null=True)
    description = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "device"
        ordering = ["modified_at"]

class MinioFile(models.Model,baseModel):
    bucket=fields.CharField(max_length=150, null=True)
    fileID= fields.CharField(max_length=150, null=True)
    name=fields.CharField(max_length=150, null=True)
    size= fields.CharField(max_length=150, null=True)
    date= fields.CharField(max_length=150, null=True)
    type=fields.CharField(max_length=150, null=True)
    description = fields.JSONField(description='测试')
    class Meta:
        table = "minio"