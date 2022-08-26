## aerich 命令

### 初始化

```shell
aerich init -t db.mysql.DB_ORM_CONFIG
```

### 初始化数据库
```shell
aerich init-db
```

### 生成迁移文件
```shell
aerich migrate
```


### 执行迁移
```shell
aerich upgrade
```


### 迁移失败

> 先 drop 再创建数据库
>
> 清空 migrations 目录
>
> 再执行 aerich init-db