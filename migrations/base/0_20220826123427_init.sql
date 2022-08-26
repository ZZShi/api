-- upgrade --
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "events" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "name" TEXT NOT NULL,
    "age" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "ut_details" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "epic" VARCHAR(64)   /* epic */,
    "feature" VARCHAR(64)   /* feature */,
    "story" VARCHAR(64)   /* story */,
    "func" VARCHAR(128)   /* 方法名称 */,
    "severity" VARCHAR(32)   /* 用例等级 */,
    "status" VARCHAR(32)   /* 状态 */,
    "start_time" TIMESTAMP   DEFAULT 0 /* 开始时间 */,
    "stop_time" TIMESTAMP   DEFAULT 0 /* 结束时间 */,
    "duration" REAL   /* 耗时 */,
    "parameters" TEXT   /* 参数 */,
    "failed_reason" TEXT   /* 失败原因 */,
    "developer" VARCHAR(48)   /* 开发同学邮箱 */,
    "test_developer" VARCHAR(48)   /* 测试同学邮箱 */,
    "order" INT   /* 历史报告 ID */,
    "case_url" VARCHAR(128)   /* 用例链接 */
) /* 测试报告详情数据 */;
CREATE TABLE IF NOT EXISTS "ut_histories" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "report_url" VARCHAR(128)   /* 报告链接 */,
    "report_name" VARCHAR(128)   /* 报告名称 */,
    "status" VARCHAR(1)   DEFAULT '0' /* 状态 */,
    "failed" INT   DEFAULT 0 /* 失败 */,
    "broken" INT   DEFAULT 0 /* 异常 */,
    "skipped" INT   DEFAULT 0 /* 跳过 */,
    "passed" INT   DEFAULT 0 /* 通过 */,
    "unknown" INT   DEFAULT 0 /* 未知 */,
    "total" INT   DEFAULT 0 /* 总数 */
) /* 测试报告历史数据 */;
CREATE TABLE IF NOT EXISTS "ut_overviews" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "epic" VARCHAR(64)   /* epic */,
    "feature" VARCHAR(64)   /* feature */,
    "story" VARCHAR(64)   /* story */,
    "failed" INT   /* 未通过 */,
    "broken" INT   /* 失败 */,
    "skipped" INT   /* 跳过 */,
    "passed" INT   /* 通过 */,
    "unknown" INT   /* 未知原因 */,
    "order" INT   /* 历史报告 ID */
) /* 测试报告概况数据 */;
CREATE TABLE IF NOT EXISTS "ut_tasks" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "task_name" VARCHAR(32)   /* 任务名称 */,
    "task_type" VARCHAR(1)   /* 任务类型 */,
    "crontab" VARCHAR(16)   DEFAULT '0 0 0 0 0 0 0' /* Corntab 表达式 */,
    "content" JSON   /* 选择的 case */,
    "case_path" JSON   /* 用例路径 */,
    "is_multi_progress" INT NOT NULL  DEFAULT 0 /* 是否多进程 */,
    "process_num" INT   /* 进程数 */,
    "group" VARCHAR(32)   /* 分组方式 */
) /* 自动化任务 */;
