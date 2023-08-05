# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

pymysql.install_as_MySQLdb()


from sqlalchemy import text


def mysql_session():
    engins = create_engine(
        "mysql://otoklx_myt01_rw:8V5uE34wL5wAMwMM@10.7.7.43:33333/db_content"
    )
    sessions = sessionmaker(bind=engins)
    return sessions()


if __name__ == "__main__":
    pass

    # s = mysql_session()
    # res = s.execute(text("update t_section_task set f_data = :r where f_id = 3593059"),{"r": }).fetchone()

    # f = open("E:/oto/docx/test.html",mode="a")
    # f.write(res.f_data)
