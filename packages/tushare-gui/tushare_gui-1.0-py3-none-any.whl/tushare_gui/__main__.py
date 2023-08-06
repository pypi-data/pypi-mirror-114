#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import tkinter
from tkinter import Frame, ttk
from tkinter.constants import DISABLED, INSERT, NO, NORMAL
from typing import Text
from pandastable.data import TableModel
import tushare
from pandastable import Table

try:
    #源码目录下运行
    from api_desc import desc_dict
    from api_list import api_list
except:
    #python3 -m运行
    from tushare_gui import api_desc, api_list
    desc_dict = api_desc.desc_dict
    api_list = api_list.api_list

from webbrowser import open as webopen
import configparser

#pandas table
pt=None
desc=None
curr_api=None
input_in=None
input_out=None
token = None
token_input = None
config = None
config_file = "config.ini"

def main():
    global pt
    global desc
    global input_in
    global input_out
    global token
    global token_input
    global config
    global api_list

    config_init()

    top = tkinter.Tk()
    top.title("tushare接口可视化工具")
    top.geometry("800x600")

    tree = ttk.Treeview(top, show='tree')
    populate_treeview(tree, None, api_list)
    tree.bind('<Double-Button-1>', show_desc)

    desc = tkinter.Text(top, height=20, padx=3, pady=3)
    desc.insert(INSERT, "说明：先输入token（token是调用接口必须的，已注册用户可登录tushare获取，如果还没注册，可以")
    desc.tag_configure('link',foreground='blue',underline=True)
    desc.insert('end','点击这里到tushare注册','link')
    desc.tag_bind('link','<Button-1>',lambda _:webopen('https://tushare.pro/register?reg=443506'))
    desc.insert(INSERT, "），再双击选择左侧的api接口，然后根据接口说明按需输入参数，最后点击调用按钮，问题反馈以及建议或者交流请加Q群：716696202，加群口令：tushare")
    desc.config(state=DISABLED)

    token_frame = tkinter.Frame(top)
    toekn_tip = tkinter.Label(token_frame, text="token：")
    token_input = tkinter.Entry(token_frame, width=70)
    toekn_tip.pack(side=tkinter.LEFT, padx=3, pady=3)
    token_input.pack(side=tkinter.LEFT, fill=tkinter.X, padx=3, pady=3)
    if token != None:
        token_input.insert(INSERT, token)

    f = tkinter.Frame(top)
    exec = tkinter.Button(f, text="调用", command=exec_api)
    export = tkinter.Button(f, text="导出", command=export_data)
    arg_example1 = tkinter.Label(f, text="参数举例（多个参数要用英文逗号分隔）：")
    arg_example2 = tkinter.Label(f, text="    输入参数（查询的过滤条件，str类型要加引号）：is_hs=\"H\",limit=3")
    arg_example3 = tkinter.Label(f, text="    输出参数（要显示哪些数据，不要加引号）：symbol,name")
    input_out = tkinter.Entry(f)
    label_out = tkinter.Label(f, text="输出参数：")
    input_in = tkinter.Entry(f)
    label_in = tkinter.Label(f, text="输入参数：")

    f2 = Frame(top)
    pt = Table(f2)
    pt.show()

    tree.pack(fill=tkinter.Y, side=tkinter.LEFT, padx=3, pady=3)
    token_frame.pack(fill=tkinter.X, side=tkinter.TOP, padx=3, pady=3)
    desc.pack(fill=tkinter.X, side=tkinter.TOP, padx=3, pady=3)
    arg_example1.pack(side=tkinter.TOP, anchor="w", padx=3, pady=3)
    arg_example2.pack(side=tkinter.TOP, anchor="w", padx=3, pady=3)
    arg_example3.pack(side=tkinter.TOP, anchor="w", padx=3, pady=3)
    label_in.pack(side=tkinter.LEFT, padx=3, pady=3)
    input_in.pack(side=tkinter.LEFT, padx=3, pady=3)
    label_out.pack(side=tkinter.LEFT, padx=3, pady=3)
    input_out.pack(side=tkinter.LEFT, padx=3, pady=3)
    exec.pack(side=tkinter.LEFT, padx=3, pady=3)
    export.pack(side=tkinter.LEFT, padx=3, pady=3)
    f.pack(fill=tkinter.X, side=tkinter.TOP, padx=3, pady=3)
    f2.pack(fill=tkinter.BOTH, side=tkinter.TOP, padx=3, pady=3)
    
    top.mainloop()

def config_init():
    global config
    global token
    global config_file
    if (os.path.exists(config_file)):
        config = configparser.ConfigParser()
        config.read(config_file)
    else:
        config = configparser.ConfigParser()
    if "tushare" not in config.sections():
        config.add_section("tushare")
    if "token" in config.options("tushare"):
        token = config.get("tushare", "token")

def exec_api():
    global pt
    global curr_api
    global input_out
    global input_in
    global token
    global token_input
    global config
    global config_file
    curr_token = token_input.get()
    if curr_token == "":
        tkinter.messagebox.showinfo("错误", "请输入token")
        return
    if curr_token != token:
        #保存配置
        config.set("tushare", "token", curr_token)
        with open(config_file, "w") as f:
            config.write(f)
    pro = tushare.pro_api(curr_token)
    new_fun='''
def query(pro):
    return pro.query("%s"%s%s)
'''%(curr_api, "" if input_in.get() == "" else ","+input_in.get(), "" if input_out.get() == "" else ", fields=\""+input_out.get()+"\"")
    print(new_fun)
    constant = globals().copy()
    try:
        exec(new_fun, constant)
        df = constant["query"](pro)
    except Exception as e:
        tkinter.messagebox.showinfo("错误", "参数格式错误（str类型记得要加引号）,或有必须的参数没填，或超时（请重试），或没权限（积分不足或需申请，看接口说明），具体信息为："+str(e))
        return
    pt.updateModel(TableModel(df))
    pt.redraw()

def export_data():
    global pt
    file_name = tkinter.filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("CSV", ".csv")])
    pt.saveAs(filename=file_name+".csv")

def show_desc(event):
    global desc
    global curr_api
    global desc_dict
    tree = event.widget
    sels = tree.selection()
    item = tree.item(sels[0])["text"]
    if item in desc_dict:
        desc.config(state=NORMAL)
        desc.delete(1.0, "end")
        desc.insert(INSERT, desc_dict[item]["desc"])
        desc.config(state=DISABLED)
        curr_api=desc_dict[item]["api"]

def populate_treeview(tree, parent, node):
    """
    Populate tree view by given json object.
    :param tree: treeview widget.
    :param parent: parent node of treeview.
    :param node: node should be a dict object.
    :return:
    """
    # 如果没有父节点，建立一个父节点
    if parent is None:
        parent = tree.insert('', 'end', text='tushare接口列表')
    # 由于node一定是dict，直接迭代
    for item in node:
        value = node.get(item)
        if isinstance(value, dict):
            cur = tree.insert(parent, 'end', text=str(item), values=(str(value).replace("'", '"'), type(value).__name__))
            populate_treeview(tree, cur, value)
        elif isinstance(value, list):
            cur = tree.insert(parent, 'end', text=item, values=(str(value).replace("'", '"'), type(value).__name__))
            for each in value:
                if isinstance(each, dict):
                    tmp = tree.insert(cur, 'end', text='{}')
                    populate_treeview(tree, tmp, each)
                else:
                    tree.insert(cur, 'end', text=str(each), values=(str(value).replace("'", '"'), type(value).__name__))
        elif isinstance(value, int) or isinstance(value, str) or isinstance(value, bool):
            # tmp = str(item) + ':' + str(value)
            tmp = str(item)
            tree.insert(parent, 'end', text=tmp, values=(str(value).replace("'", '"'), type(value).__name__))

if __name__ == '__main__':
    main()