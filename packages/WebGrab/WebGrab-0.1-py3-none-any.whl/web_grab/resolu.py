''' 按照规则解析文本内存，按照格式返回数据'''
from lxml import etree
''' 以下为 Json 解析'''


def ResoluJsons(jsonObj, rules):
    '''rules示例 [{"tag": 'IP',"rule": "origin","rules": []}]'''
    tmp = []
    for rule in rules:
        tmp.append(ResoluJson(jsonObj, rule))
    return tmp, None


def ResoluJson(jsonObj, rule):
    '''递归解析 JSON 数据'''
    if ("rules" in rule.keys()) and len(rule["rules"]):
        tmp_result = {rule["tag"]: []}
        jsonObjChilds = _jsonKey(jsonObj, rule["rule"])
        if isinstance(jsonObjChilds, (frozenset, list, set, tuple,)):
            for jsonChild in jsonObjChilds:
                chidResult = {}
                for r in rule["rules"]:
                    childTmp = ResoluJson(jsonChild, r)
                    chidResult.update(childTmp)
                tmp_result[rule["tag"]].append(chidResult)
        return tmp_result
    else:
        return {rule["tag"]: _jsonKey(jsonObj, rule["rule"])}


def _jsonKey(jsonObj, keys):
    '''根据Map 键的层级获取指定 json 节点'''
    tmp = jsonObj
    try:
        for key in keys.split("."):
            tmp = tmp[key]
        return tmp
    except:
        return "对象中不存在{0}元素键".format(keys)


''' 以下为 HTML 解析使用 xpath语法进行解析'''


def ResoluHtmls(htmlObj, rules):
    '''rules示例 [{"tag": 'IP',"rule": "origin","rules": []}]'''
    selector = etree.HTML(htmlObj)
    tmp = []
    for rule in rules:
        tmp.append(ResoluHtml(selector, rule))
    return tmp, None


def ResoluHtml(htmlObj, rule):
    '''递归解析 html 数据'''
    htmlObjChilds = _htmlKey(htmlObj, rule["rule"])
    if ("rules" in rule.keys()) and len(rule["rules"]):
        tmp_result = {rule["tag"]: []}
  
        for htmlChild in htmlObjChilds:
            chidResult = {}
            for r in rule["rules"]:
                childTmp = ResoluHtml(htmlChild, r)
                chidResult.update(childTmp)
                tmp_result[rule["tag"]].append(chidResult)
        return tmp_result
    else:
        if len(htmlObjChilds) == 1:
            return {rule["tag"]: htmlObjChilds[0]}
        else:
            result = {rule["tag"]: []}
            for htmlChild in htmlObjChilds:
                result[rule["tag"]].append( htmlChild)
            return result


def _htmlKey(htmlObj, rule):
    '''根据Map 键的层级获取指定 json 节点'''
    try:
        htmlElements = htmlObj.xpath(rule)
        tmp = []
        for elem in htmlElements:
            tmp.append(elem)
        return tmp
    except:
        return "对象中不存在{0}元素键".format(rule)

