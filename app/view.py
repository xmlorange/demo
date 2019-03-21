# -*- coding: utf-8 -*-

import zipfile as zf
from datetime import datetime
from io import BytesIO
from urllib.parse import quote

from flask import request, make_response
import pyexcel as pe

from app import app
from app.common import NEW_STORE_MAP
from app.data_ready import get_summary_of_absences, signed_detail
from app.email_util import sender_email

from app.mysql_util import ex


def run(store_id, store_name):
    signed_mobile = [i[0] for i in ex.qb("""select mobile_no from by_user """)]
    data = [["分馆", "手机号", "学员", "是否关注"]]

    buffer = BytesIO()
    # 手机号,学员,是否已关注
    for store_id, mobile, name in ex.bs(
            """select c.store_id,s.mobile,s.name from by_contract c 
left join by_contract_student cs on cs.contract_id=c.id
left join by_student s on cs.student_id=s.id
where c.is_deleted=False and c.store_id in ({}) and c.lesson_cnt > c.lesson_finished_count

group by s.mobile""".format(store_id)):
        is_signed = "否"
        if mobile and mobile in signed_mobile:
            is_signed = "是"

        data.append([store_name, mobile, name or name, is_signed])
    pe.Sheet(data).save_to_memory(file_type="xlsx", stream=buffer)
    return buffer


def export_data():
    buffer = BytesIO()

    with zf.ZipFile(buffer, "w") as z:
        for _id, _name in NEW_STORE_MAP.items():
            data = run(_id, _name)
            z.writestr("{}.xlsx".format(_name), data.getvalue())

    return buffer


def week_data(buffer):
    with open("f.xlsx", "wb") as f:
        f.write(buffer.getvalue())


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        filename = quote("{}青浦星宝关注汇总.zip".format(datetime.now().strftime("%Y-%m-%d_%H_%M_%S")))
        response = make_response(export_data().getvalue())
        response.headers['Content-Type'] = "application/zip"
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response


@app.route("/week_schedule", methods=["GET"])
def schedule():
    buffer = BytesIO()

    mobiles = [i[0] for i in ex.qb("""select mobile_no from by_user""")]

    first_table = [["分馆", "日期", "合同号", "手机号", "学员", "顾问", "是否关注"]]

    for line in ex.bs("""select se.name,c.create_time,c.contract_no,c.mobile,group_concat(distinct s.name),group_concat(distinct s.mobile),sf.name from by_contract c
left join by_contract_student cs on c.id = cs.contract_id 
left join by_student s on cs.student_id = s.id
left join staff_prod.by_staff sf on c.owner_id=sf.id
left join staff_prod.by_store se on c.store_id=se.id
where c.is_deleted=false and c.renew_from_contract_id is null and cs.is_deleted=false
and c.store_id in (140,141,29) and c.create_time >='2019-01-12' and c.create_time < curdate()
group by c.id
;"""):
        is_signed = "未关注"
        if line[3] in mobiles or any([i in mobiles for i in line[5].split(",")]):
            is_signed = "已关注"

        first_table.append(
            [line[0], line[1], line[2], line[3], line[4], line[6], is_signed]
        )

    sec_table = [["分馆", "合同号", "合同签订时间", "未排课天数", "科目", "教师"]]

    for line in ex.bs("""select s.name,c.contract_no,c.create_time,datediff(curdate(),date_format(c.create_time,'%Y-%m-%d')) + 1,
group_concat(distinct st.name), group_concat(distinct t.name)
 from by_contract c
inner join staff_prod.by_store s on c.store_id=s.id
inner join by_contract_course_allocation ca on ca.contract_id = c.id
inner join by_subject st on ca.subject_id = st.id
left join staff_prod.by_staff t on ca.teacher_id = t.id
where c.is_deleted=false and c.renew_from_contract_id is null and c.lesson_arraged_count = 0 and c.create_time >='2019-01-12'
and c.store_id in (29,141,140)
group by c.id order by 1,3"""):
        sec_table.append(list(line))

    pe.Book({"昨日关注数据": first_table,
             "未排课数据": sec_table,
             "缺勤提醒": get_summary_of_absences()}).save_to_memory("xlsx", buffer)

    # _time = datetime.now() - timedelta(days=1)
    # _date = _time.strftime("%Y-%m-%d")
    # sender_email(subject="学员端日报",
    #              files={quote("{}.xlsx".format(_date)): buffer.getvalue()})
    # return "Success"
    week_data(buffer)
    return "Success"


@app.route("/public", methods=["GET"])
def public_info():
    public_data = [["合同号", "城市", "分馆", "学员姓名", "金额", "创建时间", "公益课类型"]]
    for i in ex.bs("""select c.contract_no,g.name,s.name,bs.name,c.total_tuition,c.create_time,cha.name from by_contract c
left join by_lesson_package cha on c.lesson_package_id=cha.id
left join by_contract_student cs on c.id=cs.contract_id
left join by_student bs on cs.student_id=bs.id
left join staff_prod.by_store s on c.store_id=s.id
left join staff_prod.by_geo g on s.city_code=g.code
where c.contract_category = 3 and c.is_deleted=false 
    and c.create_time>=date_add(curdate(),interval -7 day) and c.create_time < curdate() 
    # and c.create_time >'2018-12-01'
order by 2,3,6"""):
        public_data.append(list(i))

    tran_data = [["合同号", "城市", "分馆", "学员姓名", "总金额", "转化时间", "课程", "公益课合同号"]]

    for i in ex.bs("""select c.contract_no,g.name,s.name,group_concat(distinct st.name),c.actual_amt,c.create_time,group_concat(distinct sj.name),ct.contract_no from by_contract c
left join by_contract ct on c.transfer_public_contract_id = ct.id
left join by_contract_student cs on cs.contract_id=c.id
left join by_contract_course_allocation bcca on bcca.contract_id=c.id
left join by_student st on cs.student_id=st.id
left join by_subject sj on bcca.subject_id=sj.id
left join staff_prod.by_store s on c.store_id=s.id
left join staff_prod.by_geo g on s.city_code=g.code
where c.is_deleted=False and ct.is_deleted=False  
    and c.create_time>=date_add(curdate(),interval -7 day) and c.create_time < curdate()
group by c.id;
"""):
        tran_data.append(list(i))

    pe.Book({"公益课签订数据": public_data,
             "公益课转化数据": tran_data}).save_as("公益课.xlsx")
    return "Success"


@app.route("/week_report", methods=["GET"])
def week_report():
    signed_detail()
    return "Success"
