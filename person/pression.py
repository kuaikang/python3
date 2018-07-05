list = [
    {
        'path': '/login',
    },
    {
        'path': '/error',
    },
    {
        'path': '/404',
        'children': [
            {
                'path': 'index',
            }
        ]
    },
    {
        'path': '/401',
    },
    {
        'path': '/',
        'name': '首页',
    },
    {
        'path': '/standardBank',
        'name': '标准题库',
        'children': [
            {
                'path': 'standard',
                'name': '标准题库'
            },
            {
                'path': 'addNewQuestion/:summaryKey/:chapterId/:chapterName',
                'name': '新建题目'
            },
            {
                'path': 'addNewQuestion/:questionId/:summaryKey/:type/:flag/:summaryCode/:grade',
                'name': '编辑题目'
            }
        ]
    },
    {
        'path': '/KnowledgePoint',
        'name': '知识点管理',
        'children': [
            {
                'path': 'Knowledge',
                'name': '知识点管理'
            }
        ]
    },
    {
        'path': '/checkManagement',
        'name': '审核管理',
        'children': [
            {
                'path': '/firstCheck',
                'name': '初审',
                'children': [
                    {
                        'path': 'list'
                    },
                    {
                        'path': 'questionCheck/:summaryKey/:summaryCode/:tabNumber/:grade?/:material?/:book?/:unit?/:chapterId?/:reasonType?',
                        'name': '题目审核'
                    },
                    {
                        'path': 'questionDetail/:id/:summaryKey/:summaryCode/:type/:checkType/:tabNumber?/:grade?/:material?/:book?/:unit?/:chapterId?/:reasonType?',
                        'name': '题目详情'
                    }
                ]
            },
            {
                'path': '/secondCheck',
                'name': '复审',
                'children': [
                    {
                        'path': 'list',
                    },
                    {
                        'path': 'questionDetail/:id/:summaryKey/:summaryCode/:type/:checkType/:tabNumber',
                        'name': '复审题目详情'
                    }
                ]
            },

        ]
    },
    {
        'path': '/auditStatistics',
        'name': '统计报表',
        'children': [
            {
                'path': 'auditStatistics',
                'name': '审核统计'
            },

        ]
    },
    {
        'path': '/userManage',
        'name': '用户管理',
        'children': [
            {
                'path': 'userList',
                'name': '用户管理'
            },
            {
                'path': 'addUser',
                'name': '添加用户'
            },
            {
                'path': 'editUser/:userId?',
                'name': '修改用户'
            }
        ]
    },
    {
        'path': '/roleManage',
        'name': '权限管理',
        'children': [
            {
                'path': 'roleList',
                'name': '权限管理'
            }
        ]
    },
    {
        'path': '/updatePwd',
        'name': '修改密码',
    }
]

insert = "insert into t_sys_menu('id','menu_name','url','parent_id') " \
         "values('{id}','{path}','{menu_name}','{parent_id}')"
dict = {}
num = 1
for item in list:
    print(insert.format(id=num, path=item.get('path'), menu_name=item.get('name'), parent_id=''))
    dict['id'] = num
    num += 1
    child = item.get('children')
    if child:
        for c in child:
            print(insert.format(id=num, path=c.get('path'), menu_name=c.get('name'), parent_id=''))
            dict['id'] = num
            num += 1
            child = item.get('children')
            if child:
                for c in child:
                    print(insert.format(id=num, path=c.get('path'), menu_name=c.get('name'), parent_id=dict['id']))
                    num += 1
