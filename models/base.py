from tortoise import Model,fields
#时间戳混入类
class TimestampMixin(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    class Meta:
        abstract = True
#角色表
class Role(TimestampMixin):
    role_name = fields.CharField(max_length=15, description="角色名称")
    user: fields.ManyToManyRelation["Users"] = \
        fields.ManyToManyField("base.Users", related_name="role", on_delete=fields.CASCADE)
    access: fields.ManyToManyRelation["Access"] = \
        fields.ManyToManyField("base.Access", related_name="role", on_delete=fields.CASCADE)
    role_status = fields.BooleanField(default=False, description="True:启用 False:禁用")
    role_desc = fields.CharField(null=True, max_length=255, description='角色描述')

    class Meta:
        table_description = "角色表"
        table = "role"
#用户表
class  Users(TimestampMixin):
    role: fields.ManyToManyRelation[Role]
    id = fields.IntField(pk=True,description="用户id")
    name = fields.CharField(null=True,max_length=20,description="用户名")
    typee = fields.BooleanField(default=False,description="用户类型 True:管理员 False:普通用户")
    passwd = fields.CharField(null=True,max_length=255,description="密码")
    nickname = fields.CharField(default='nait用户',max_length=255,description="昵称")
    user_status = fields.IntField(default=1, description='0未激活 1正常 2禁用')
    header_img = fields.CharField(null=True, max_length=255, description='头像')
    email = fields.CharField(null=True,max_length=255,description="邮箱")
    phone = fields.CharField(null=True,max_length=255,description="电话")
    create_time = fields.DatetimeField(auto_now_add=True,description="创建时间")
    update_time = fields.DatetimeField(auto_now=True,description="更新时间")
    class Meta:
        table = "users"
        table_description = "用户表"
#权限表
class Access(TimestampMixin):
    role: fields.ManyToManyRelation[Role]
    access_name = fields.CharField(max_length=15, description="权限名称")
    parent_id = fields.IntField(default=0, description='父id')
    scopes = fields.CharField(unique=True, max_length=255, description='权限范围标识')
    access_desc = fields.CharField(null=True, max_length=255, description='权限描述')
    menu_icon = fields.CharField(null=True, max_length=255, description='菜单图标')
    is_check = fields.BooleanField(default=False, description='是否验证权限 True为验证 False不验证')
    is_menu = fields.BooleanField(default=False, description='是否为菜单 True菜单 False不是菜单')

    class Meta:
        table_description = "权限表"
        table = "access"

class SystemParams(TimestampMixin):
    params_name = fields.CharField(unique=True, max_length=255, description="参数名")
    params = fields.JSONField(description="参数")

    class Meta:
        table_description = "系统参数表"
        table = "system_params"