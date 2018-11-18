import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conferenceplatform.settings") 

import django
django.setup()
from django.db import IntegrityError
from conference.models import Subject

ALL_SUBJECTS = ['基础科学', '工程科技I辑', '工程科技II辑', '农业科技', '医药卫生科技', 
'哲学与人文科学', '社会科学I辑', '社会科学II辑', '信息科技', '经济与管理科学', '工业技术',
'医药卫生', '经济', '农业科学', '文化科学', '教育', '体育', '交通运输', '天文学', '地球科学',
'数理科学与化学', '环境科学', '安全科学', '政治', '法律', '航空', '航天', '生物科学', '社会科学总论', 
'历史', '地理', '自然科学总论', '语言', '文字', '哲学', '宗教', '艺术', '文学', '军事', '马克思主义',
'列宁主义', '毛泽东思想', '邓小平理论']

def import_into_db():
    for s in ALL_SUBJECTS:
        try:
            Subject.objects.create(name=s)
        except IntegrityError:
            pass

if __name__ == '__main__':
    import_into_db()