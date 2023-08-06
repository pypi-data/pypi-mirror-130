import json
import time
import requests
from b_c_components.Intercept_requests.selenium_network import info
from b_c_components.custom_module.custom_exception import Configuration_file_error


def login(environment, username, password, driver):
    """
    登陆，返回cookie
    """
    session = requests.session()
    login_data = {
        "UserName": f"{username}",
        "Password": f"{password}",
        "LoginType": "0",
        "Remember": "true",
        "IsShowValCode": "false",
        "ValCodeKey": ""}
    try:
        r = session.post(
            url='https://www.italent.' +
            environment +
            '/Account/Account/LogInITalent',
            data=login_data)
        if r.status_code == 200:
            if json.loads(r.text).get('Code') == 1:
                driver.get(driver.global_instance.get('element_str').italent_url + environment)
                driver.add_cookie(
                    {'name': 'Tita_PC', 'value': r.cookies.get('Tita_PC')})
                driver.get(driver.global_instance.get('element_str').italent_url + environment)
            else:
                raise
        else:
            raise
    except Exception as e:
        raise e


def login_interface(environment, username, password):
    """

    :param environment:
    :param username:
    :param password:
    """
    session = requests.session()
    login_data = {
        "UserName": f"{username}",
        "Password": f"{password}",
        "LoginType": "0",
        "Remember": "true",
        "IsShowValCode": "false",
        "ValCodeKey": ""}
    login_url = 'https://www.italent.link' if environment == 'test' else 'https://www.italent.cn'
    r = session.post(url=login_url + '/Account/Account/LogInITalent', data=login_data)
    if r.status_code == 200:
        return session
    else:
        return Configuration_file_error(msg=r.text)


def unfinished_transactions(driver, environment, transaction_type, transaction_name):
    """
    cloud待办的处理
    transaction_type 待办所属产品
    transaction_name 以绩效为例，transaction_name代表活动
    """
    cookie = ''
    cookie_list = driver.get_cookies()
    driver.global_cases_instance.update(BSGlobal={})
    time.sleep(0.5)
    driver.global_cases_instance.get('BSGlobal').update(
        tenantInfo=driver.execute_script('return BSGlobal.tenantInfo'))
    driver.global_cases_instance.get('BSGlobal').update(
        userInfo=driver.execute_script('return BSGlobal.userInfo'))
    ssn_Tita_PC = ''
    for i in cookie_list:
        if i.get('name') == 'Tita_PC':
            cookie = f'{i.get("name")}={i.get("value")}' + \
                f'; {"ssn_Tita_PC"}={i.get("value")}'
            ssn_Tita_PC = i.get("value")
            break
    headers = {
        'Cookie': cookie
    }
    tenantId = str(driver.global_cases_instance.get(
        'BSGlobal').get('tenantInfo').get('Id'))
    userId = str(driver.global_cases_instance.get(
        'BSGlobal').get('userInfo').get('userId'))
    # # environment = driver.global_instance.get('element_str').environment
    # environment = driver.element_str.environment
    session = requests.session()
    url = f'https://www.italent.{environment}/api/v3/{tenantId}/{userId}/todo/Get?app_id=-1&deadline=&blackTodoIds=&page_size=10&status=1&__t={round(time.time() * 1000)}'
    all_transactions = json.loads(
        session.get(
            url=url,
            headers=headers).text).get('data').get('todos')
    domain = 'cloud.italent.' + environment
    driver.add_cookie(
        {'domain': domain, 'name': 'ssn_Tita_PC', 'value': ssn_Tita_PC})
    for i in all_transactions:
        if transaction_type == i.get('appName'):
            if transaction_name != "" and transaction_name in i.get('content'):
                driver.get(url='https:' + i.get('objUrl'))
                break


def go_to_menu(driver, environment, menu_name):
    """
    进入菜单
    menu_name: 菜单名称，默认菜单传应用名称，非默认菜单传应用名称_菜单名称
    """
    driver.add_cookie({'domain': 'cloud.italent.cn',
                       'name': 'ssn_Tita_PC',
                       'value': driver.get_cookie('Tita_PC').get('value')})
    driver.add_cookie({'domain': 'cloud.italent.cn',
                       'name': 'Tita_PC',
                       'value': driver.get_cookie('Tita_PC').get('value')})
    menu_mapping = requests.get('http://8.141.50.128:80/static/json_data/menu_mapping.json').json()
    host_url = f'https://cloud.italent.{environment}/'
    driver.get(host_url + menu_mapping.get(menu_name))


def get_form_view(driver):
    """
    获取表单信息
    """
    fields_to_operate_on_list = []
    network_data = info(driver)
    network_data.reverse()
    datasource_data = []
    for data in network_data:
        url = data.get('request').get('url')
        if '/api/v2/data/datasource' in url:
            # 获取字段对应数据源
            datasource_data = json.loads(data.get('response_data').get('body'))
            break
    for data in network_data:
        # 解析formView接口，获取所有表单字段
        url = data.get('request').get('url')
        if '/api/v2/UI/FormView' in url:
            # 在这里获取所有需要操作的字段
            for sub in json.loads(
                    data.get('response_data').get('body')).get('sub_cmps'):
                for field in sub.get('sub_cmps'):
                    if field.get('cmp_data').get('showdisplaystate') == 'readonly' and field.get(
                            'cmp_data').get('required') is True:
                        dict_data = {}
                        for data_source in datasource_data:
                            if field.get('cmp_data').get(
                                    'datasourcename') == data_source.get('key'):
                                dict_data['dataSourceResults'] = data_source.get(
                                    'dataSourceResults')
                                break
                        dict_data.update({
                            'cmp_id': field.get('cmp_id'),
                            'cmp_label': field.get('cmp_label'),
                            'cmp_name': field.get('cmp_name'),
                            'cmp_type': field.get('cmp_type'),
                            'cmp_data': field.get('cmp_data')
                        })
                        fields_to_operate_on_list.append(dict_data)
    return fields_to_operate_on_list


def option_form(driver, fields_to_operate_on_list):
    """
    操作表单
    """
    for field in fields_to_operate_on_list:
        """
        表单填充
        """
        if field.get('cmp_type') == 'BC_TextBox':
            driver.find_element_by_xpath(
                f"""//*[@class="bc-form-item clearfix bc-form-item-middle"]/div[{str(
                    fields_to_operate_on_list.index(field)+1)}]/div[2]/input""").clear()
            driver.find_element_by_xpath(
                f"""//*[@class="bc-form-item clearfix bc-form-item-middle"]/div[{str(
                    fields_to_operate_on_list.index(field)+1)}]/div[2]/input""").send_keys(
                '自动化人才模型数据' + str(int(time.time())))


def add_or_edit_manipulate_fields(driver, button_xpath):
    """
    视图新增按钮
    """
    time.sleep(1)
    button_xpath = '//*[@id="indexPageViewName"]/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/span'
    driver.find_element_by_xpath(button_xpath).click()
    driver.switch_to_frame(0)
    option_form(driver, get_form_view(driver))
    driver.find_element_by_xpath('//*[@id="formSubmitButton"]').click()
    driver.switch_to_default_content()
    time.sleep(5)
    driver.refresh()


def copy_list_data(driver, list_index, button_xpath):
    """
    复制
    """
    button_xpath = ''
    time.sleep(2)
    element_str = f'//*[@class="table-item-check table-item-check-back-noMoving pc-sys-Checkbox-nomal-svg"]'
    element = driver.find_elements_by_xpath(element_str)[list_index + 2]
    driver.execute_script(f'arguments[0].scrollIntoView()', element)
    driver.execute_script(f'arguments[0].click()', element)
    driver.find_element_by_xpath(
        '//*[@id="indexPageViewName"]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/span').click()
    driver.switch_to_frame(0)
    option_form(driver, get_form_view(driver))
    driver.find_element_by_xpath('//*[@id="formSubmitButton"]').click()
    driver.switch_to_default_content()
    time.sleep(5)
    driver.refresh()


def delete_list_data(driver, list_index, button_xpath):
    """
    复制
    """
    button_xpath = ''
    time.sleep(2)
    element_str = f'//*[@class="table-item-check table-item-check-back-noMoving pc-sys-Checkbox-nomal-svg"]'
    element = driver.find_elements_by_xpath(element_str)[list_index + 1]
    driver.execute_script(f'arguments[0].scrollIntoView()', element)
    driver.execute_script(f'arguments[0].click()', element)
    driver.find_element_by_xpath(
        '//*[@id="indexPageViewName"]/div[2]/div/div/div[1]/div[3]/div[1]/div[3]/span').click()
    time.sleep(1)
    driver.find_elements_by_xpath(
        '//*[@class="us-footer clearfix"]/div/span')[0].click()
    time.sleep(5)
    driver.refresh()


def go_to_data_details(driver):
    """
    进入列表数据详情
    进入列表获取列表数据，解析id，通过url访问
    """
    # https://cloud.italent.cn/CustomModel/#/DetailPage?
    # metaObjName=CustomModel.CustomModel&listViewName=CustomModel.SingleObjectListView.ListOfModel&id=
    # metaObjName=CustomModel.CustomModel&listViewName=CustomModel.SingleObjectListView.ListOfModel&app=CustomModel
