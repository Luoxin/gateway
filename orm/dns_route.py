import utils
from orm import *
from orm import base


class GatewayDns(base):
    __tablename__ = "gateway_dns"

    id = Column(Integer, primary_key=True)
    created_at = Column(Integer, server_default=str(utils.now()))
    updated_at = Column(
        Integer, server_default=str(int(utils.now())), onupdate=str(int(utils.now()))
    )

    domain = Column(String, index=True, comment="域名")

    crawl_url = Column(String(500), unique=True, comment="订阅地址/抓取源地址")

    crawl_type = Column(Integer, index=True, comment="抓取类型")
    rule = Column(JSON, comment="抓取规则")
    is_closed = Column(Boolean, comment="是否禁用")
    next_at = Column(Integer, comment="下一次的测速时间")
    interval = Column(Integer, comment="间隔")
    note = Column(Text, comment="备注信息")

    __table_args__ = {"comment": "域名映射表"}  # 添加索引和表注释
