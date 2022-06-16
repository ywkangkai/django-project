def handel_header_params(datas):
    header_list = []
    if datas is not None:
        for key, value in datas.items():
            header_list.append({
                "key": key,
                "value": value
            })

    return header_list


def handle_globalVar_parameterized(datas):
    result_list = []
    if datas is not None:
        for one_var_dict in datas:
            key = list(one_var_dict)[0]
            value = one_var_dict.get(key)
            if isinstance(value, int):
                param_type = "int"
            elif isinstance(value, float):
                param_type = "float"
            elif isinstance(value, bool):
                param_type = "boolean"
            else:
                param_type = "string"
            result_list.append({
                "key": key,
                "value": value,
                "param_type": param_type
            })
    return result_list

def handle_validate(datas):
    """
    将[{'check': 'status_code', 'expect':200, 'comparator': 'equals'}]
    转化为 [{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}],
    :param datas: 待转换的参数列表
    :return:
    """
    result_list = []
    if datas is not None:
        for one_validate_dict in datas:
            key = one_validate_dict.get("check")
            value = one_validate_dict.get("expect")
            comparator = one_validate_dict.get("comparator")
            if isinstance(value, int):
                param_type = "int"
            elif isinstance(value, float):
                param_type = "float"
            elif isinstance(value, bool):
                param_type = "boolean"
            else:
                param_type = "string"
            result_list.append({
                "key": key,
                "value": value,
                "comparator": comparator,
                "param_type": param_type
            })

    return result_list


def handle_from_data(datas):
    """
    将 {'username': 'keyou', 'age': 18, 'gender': True}
    [{key: 'username', value: 'keyou', param_type: 'string'}, {key: 'age', value: 18, param_type: 'int'}]
    :param datas: 待转换的参数列表
    :return:
    """
    result_list = []
    if datas is not None:
        for key, value in datas.items():
            if isinstance(value, int):
                param_type = "int"
            elif isinstance(value, float):
                param_type = "float"
            elif isinstance(value, bool):
                param_type = "boolean"
            else:
                param_type = "string"
            result_list.append({
                "key": key,
                "value": value,
                "param_type": param_type
            })
    return result_list


def handle_extract(datas):
    """
    将 [{'token': 'content.token'}]
    转化为 [{key: 'token', value: 'content.token'}]
    :param datas: 待转换的参数列表
    :return:
    """
    result_list = []
    if datas is not None:
        for one_dict in datas:
            key = list(one_dict)[0]
            value = one_dict.get(key)
            # 如果参数化的值为列表, 则转化为字符串形式
            if isinstance(value, list):
                value = str(value)
            result_list.append({
                "key": key,
                "value": value
            })

    return result_list


def handle_setup_teardown(datas):
    """
    处理第五种类型的数据转化
    将 ['${setup_hook_prepare_kwargs($request)}', '${setup_hook_httpntlmauth($request)}']
    转化为 [{key: '${setup_hook_prepare_kwargs($request)}'}, {key: '${setup_hook_httpntlmauth($request)}'}]
    :param datas:
    :return:
    """
    result_list = []
    if datas is not None:
        for item in datas:
            result_list.append({
                "key": item
            })

    return result_list