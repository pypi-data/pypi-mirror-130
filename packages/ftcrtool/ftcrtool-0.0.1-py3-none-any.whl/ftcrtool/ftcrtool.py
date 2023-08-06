#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import os
from subprocess import call, check_output
from tkinter import *
from tkinter import ttk
import getopt, sys
import re
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

#
# Created by Aucean.liang on 2019/1/11.
#

SCRIPT_PATH = os.getcwd()
RBT = "rbt"
GIT = "git"
DIFF_PATTERN = re.compile(r'\s*diff --git\s*a/([^\s]+)\s*b/[^\s]+')
INDEX_PATTERN = re.compile(r'\s*index\s*([0-9a-z]+)\.\.([0-9a-z]+).*')
SUBVERSION_PATTERN = re.compile(r'\s*\+Subproject\s*commit\s*([0-9a-z]+)\s*')
REVIEW_URL_PATTERN = re.compile(r'\s*http://reviewboard.oa.com[:0-9]*/r/([0-9]+)/diff/\s*')
# reviews.android

# 需求单ID
demandID = ""
# 区分SourceTree和命令行两种Post方式
isCommandPostStyle = True


def new_file_diff(file_path, version):
    with open(file_path) as f:
        lines = [("+" + line.replace("\n", "")).decode("utf-8") for line in f]

    head = '''diff --git a/{file_path} b/{file_path}
new file mode 100644
index 0000000000..{version}
--- /dev/null
+++ b/{file_path} 
@@ -0,0 +1,{line} @@'''.format(file_path=file_path, version=version, line=len(lines))
    return head.decode("utf-8").split("\n") + lines


def usage():
    print(
        '''
        postreview.py -s -r <review Id> {[<earlier commit Id>-]<commit Id>}|{<commit Id>,<commit Id>,...}
        -s 表示把staged文件提交review
        -r 表示要提交到一个已经publish的review里边来更新该review
        -p 表示一次提交多个记录到Review Board (Note:earlier commit Id要在前面)
        eg：postreview.py -p 83d452d,03d6025,6e69a6a
        <commit Id>可以是长Id也可以是短Id
        postreview.py <commit Id>:
          把<commit Id>对应的commit提交去review
          例如： postreview b400c4e
        postreview.py <earlier commit Id>-<commit Id>:
          把从<earlier commit Id>到<commit Id>所对应的范围内的(连续的)所有commit都提交去review
          例如：postreview.py b400c4e-91970bf
        postreview.py <commit Id>,<commit Id>,...
          把分立的多个commit提交到同一个review里边(这commitID的顺序需要注意下，最早的提交应该在最前)
          例如 postreview.py 83d452d,03d6025,6e69a6a
        ''')


def run_cmd(cmd="", cmd_list=[], exit_on_error=True, decode=True):
    """

    :rtype: object
    """
    result = None
    try:
        if not cmd_list:
            cmd_list = cmd.split()
        f = check_output(cmd_list)
        if decode:
            result = f.decode("utf-8").split("\n")
        else:
            return f
    except Exception as e:
        print (">>>error: ", e)
        if exit_on_error:
            exit(-1)
    return result


def get_published_diff(review_request):
    return run_cmd("/usr/local/bin/rbt patch --print " + review_request)


def remove_file(file_name):
    try:
        os.remove(file_name)
    except Exception as e:
        return


class Merge:
    def __init__(self):
        self.diff_seg_group = {}
        self.duplicate_diff = {}
        self.res_submodule = []

    def parse_diff(self, diff_file):
        result = {}
        file_path = ""
        index_start = ""
        index_end = ""
        content = []
        subVersion = ""
        for line in diff_file:
            m = DIFF_PATTERN.match(line)
            # the line is start with "diff --git"
            # it's a new file diff segment
            if m:
                if file_path:
                    if subVersion:
                        # 检查子模块
                        if file_path == "ftnn_res":
                            # 当前diff为ftnn_res子模块diff
                            self.res_submodule.append(subVersion)
                    else:
                        # 把结果存到map中
                        result[file_path] = {"start": index_start, "end": index_end, "content": content}

                # reset the field
                file_path = m.group(1)
                index_start = ""
                index_end = ""
                content = []
                subVersion = ""
            elif "+Subproject" in line:
                m = SUBVERSION_PATTERN.match(line)
                if m:
                    subVersion = m.group(1)
            else:
                m = INDEX_PATTERN.match(line)
                if m:
                    index_start = m.group(1)
                    index_end = m.group(2)
            content.append(line)

        if subVersion:
            # 检查子模块
            if file_path == "ftnn_res":
                # 当前diff为ftnn_res子模块diff
                self.res_submodule.append(subVersion)
        else:
            # 把结果存到map中
            result[file_path] = {"start": index_start, "end": index_end, "content": content}
        return result

    def add(self, diff):
        diff_seg = self.parse_diff(diff)
        # 分割完后这把它们合并到一起，并处理重复的diff
        for file_path in diff_seg:
            # 如果已经存在该文件的diff，那么证明该文件有多个版本的diff
            if file_path in self.diff_seg_group:
                # 把这更新的版本先暂存起来，应为后面可能会有更新的版本
                self.duplicate_diff[file_path] = diff_seg[file_path]
            else:
                self.diff_seg_group[file_path] = diff_seg[file_path]

    def get_merge_result(self):
        for diff_file in self.duplicate_diff:
            start_version = self.duplicate_diff[diff_file]["start"] #diff_seg_group
            end_version = self.duplicate_diff[diff_file]["end"]
            content = []
            if re.compile("^0+$").match(start_version):
                try:
                    content = new_file_diff(diff_file, end_version)
                except Exception as e:
                    print ("ignore " + diff_file + "start version: " + start_version + " end version: " + end_version)
                    print (e)
            else:
                merge_diff = run_cmd("git diff {start}..{end}".format(start=start_version, end=end_version))
                if "diff --git" in merge_diff[0]:
                    for line in merge_diff:
                        if "diff --git" in line:
                            content.append(
                                merge_diff[0].replace(start_version, diff_file).replace(end_version, diff_file))
                        elif "--- a/" in line:
                            content.append("--- a/" + diff_file)
                        elif "+++ b/" in line:
                            content.append("+++ b/" + diff_file)
                        else:
                            content.append(line)

            # 把多版本的diff merge后更新到diff_seg_group
            self.diff_seg_group[diff_file]["end"] = end_version
            self.diff_seg_group[diff_file]["content"] = content
        return self.diff_seg_group


def upload_diff(merged_diff, review_request, summary="", description="", depend_on=None, change_desc=""):
    diff_map = merged_diff.get_merge_result()
    tmp_diff_file = '/tmp/review.diff'
    with open(tmp_diff_file, 'w', encoding='utf-8') as f:
        for file_path, diff_content in diff_map.items():
            for line in diff_content["content"]:
                # byte = line.encode("utf-8") + "\n"
                f.write(line + "\n")

    cmd = ["/usr/local/bin/rbt", "post"]
    cmd.append("--diff-file={diff_file}".format(diff_file=tmp_diff_file))
    if depend_on:
        cmd.append("--depends-on={depend}".format(depend=depend_on))

    if summary:
        cmd.append("--summary={summary}".format(summary=summary))

    if description:
        cmd.append("--description={description}".format(description=description))

    if change_desc:
        cmd.append("--change-description={change_desc}".format(change_desc=change_desc))
    if review_request:
        cmd.append("-r")
        cmd.append("{review_id}".format(review_id=review_request))

    cmd.append("--markdown")
    rbt_output = run_cmd(cmd_list=cmd)

    review_id = 0
    for line in rbt_output:
        m = REVIEW_URL_PATTERN.match(line)
        if m:
            review_id = m.group(1)
        print (line)

    remove_file(tmp_diff_file)
    return review_id


def resolve_submodule(merge, review_request, subreview_request):
    depend_on = None
    if merge.res_submodule:
        print ("resolve submodule ")
        print (merge.res_submodule)
        current_dir = os.getcwd()
        os.chdir("./ftnn_res")
        res_commits = ",".join(merge.res_submodule)
        if review_request:
            if subreview_request:
                depend_on = post_committed(res_commits, subreview_request, None)
        else:
            depend_on = post_committed(res_commits, None, None)
        os.chdir(current_dir)
    return depend_on


def post_staged(review_request):
    merge = Merge()
    if review_request:
        merge.add(get_published_diff(review_request))

    stage_diff = run_cmd("git diff --ignore-submodules --cached")
    if not stage_diff[0]:
        print ("没有staged文件，请先把要post review 的文件stage再重新运行postreview.py -s")
        exit(2)
    merge.add(stage_diff)
    upload_diff(merge, review_request)


def post_committed(commit_ids, review_request, subreview_request):
    merge = Merge()
    summary = ""
    tmpStr = ""
    change_desc = ""
    description = ""
    is_change = False
    continuously_commit = re.compile(r"\s*([^-,]+)-([^-,]+)\s*")
    m = continuously_commit.match(commit_ids)
    start_commit = ""
    end_commit = ""

    if m:
        start_commit = m.group(1) + "~"
        end_commit = m.group(2)
    else:
        start_commit = end_commit = commit_ids
        start_commit += "~"
    if "," in commit_ids:
        singleStr = ''
        tmpStr = ""
        for commit in reversed(commit_ids.split(",")):
            singleStr = run_cmd(r"git show -s --format=%B {commitId}".format(commitId=commit), decode=False)
            singleStr = singleStr.decode("utf-8").replace("\n", " ")  # python3 不会自动decode了 不需要encode  .encode("utf-8")
            tmpStr += (singleStr) + " "
    else:
        tmpStr = run_cmd(r"git show -s --format=%B {commitId}".format(commitId=end_commit), decode=False)
        tmpStr = tmpStr.decode("utf-8").replace("\n", " ") # python3 不会自动decode了 不需要encode  .encode("utf-8")

    if review_request:
        is_change = True
        if review_request == "00":
            regStr = re.search(r"reviewboard.oa.com/r/[0-9]+", tmpStr).group()
            review_request = re.search(r"[0-9]+", tmpStr).group()
        else:
            # regStr = re.search(r"reviewboard.oa.com/r/[0-9]+", tmpStr).group()
            review_request = re.search(r"[0-9]+", review_request).group()
        merge.add(get_published_diff(review_request))

    if "," in commit_ids:
        # commit id 以","分割，代表多个分立的commit
        # 把每个commit的diff取出
        if isCommandPostStyle:
            for commit in commit_ids.split(","):
                diff_item = run_cmd("git diff {commit_id}~ {commit_id}".format(commit_id=commit))
                # 由于是多个分立的commit，所以有可以包含对相同文件的修改
                merge.add(diff_item)
        else:
            for commit in reversed(commit_ids.split(",")):
                diff_item = run_cmd("git diff {commit_id}~ {commit_id}".format(commit_id=commit))
                # 由于是多个分立的commit，所以有可以包含对相同文件的修改
                merge.add(diff_item)
    else:

        diff_content = run_cmd(
            "git diff {start_commit_id} {end_commit_id}".format(start_commit_id=start_commit, end_commit_id=end_commit))
        merge.add(diff_content)

    if is_change:
        change_desc = tmpStr
    else:
        summary = tmpStr
        description = '''# 需求/Bug\n- 链接：\n- 简要描述：\n# 修改点\n1.\n# 影响点（改动对业务的影响，可选）\n1.'''

    if len(demandID) != 0:
        summary = "【" + demandID + "】  " + summary

    depend_on = resolve_submodule(merge, review_request, subreview_request)

    return upload_diff(merge, review_request, summary, description, depend_on, change_desc)


# 需求ID文本框
def textWindow():
    window = Tk()
    window.title("Post CodeReview")
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    ww = 300
    wh = 200
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    lable = Label(window, text='请输入需求单ID(选填)', width=30, height=2)
    lable.place(x=30, y=30)
    entry = Entry(window, highlightbackground='gray', fg='gray')
    entry.place(x=65, y=65)

    def getUrl():
        global varID
        varID = entry.get()
        window.quit()

    def closeWindow():
        window.quit()
        exit(0)

    ttk.Button(window, text="Post", style='black/white.TButton', command=getUrl).place(x=55, y=100)
    ttk.Button(window, text="Cancel", style='black/white.TButton', command=closeWindow).place(x=165, y=100)

    def OnFocusIn(event):
        if type(event.widget).__name__ == 'Tk':
            event.widget.attributes('-topmost', False)

    window.attributes('-topmost', True)
    window.focus_force()
    window.bind('<FocusIn>', OnFocusIn)
    window.mainloop()
    return varID


review_request = None
subreview_request = None
staged = False
# 确定是否要弹出需求ID文本框
hasDemandID = True

optlist, args = getopt.getopt(sys.argv[1:], "shr:b:p")
for opt in optlist:
    if opt[0] == "-r":
        if opt[1] == "00":
            # 定义窗口
            window = Tk()
            window.title("Update CodeReview")
            sw = window.winfo_screenwidth()
            sh = window.winfo_screenheight()
            ww = 300
            wh = 200
            x = (sw - ww) / 2
            y = (sh - wh) / 2
            window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
            lable = Label(window, text='请输入Update CodeReview链接', width=30, height=2)
            lable.place(x=30, y=30)

            entry = Entry(window, highlightbackground='gray', fg='gray')
            entry.place(x=65, y=65)


            def getUrl():
                global var
                var = entry.get()
                window.quit()

            def closeWindow():
                window.quit()
                exit(0)

            ttk.Button(window, text="Update", style='black/white.TButton', command=getUrl).place(x=55, y=100)
            ttk.Button(window, text="Cancel", style='black/white.TButton', command=closeWindow).place(x=165, y=100)

            def OnFocusIn(event):
                if type(event.widget).__name__ == 'Tk':
                    event.widget.attributes('-topmost', False)


            window.attributes('-topmost', True)
            window.focus_force()
            window.bind('<FocusIn>', OnFocusIn)
            window.mainloop()
            if var == "":
                exit(0)
            review_request = var
            hasDemandID = False
        # elif opt[1] == "01":
        #     isCommandPostStyle = True
        else:
            review_request = opt[1]
            hasDemandID = False
    elif opt[0] == "-s":
        staged = True
        hasDemandID = False
    elif opt[0] == "-h":
        usage()
        exit(0)
    elif opt[0] == "-b":
        subreview_request = opt[1]
        hasDemandID = False
    elif opt[0] == "-p":
        isCommandPostStyle = False

if staged:
    post_staged(review_request)
else:
    if args:
        if hasDemandID:
            demandID = textWindow()
        post_committed(",".join(args), review_request, subreview_request)
    else:
        print ("请指定commit id")
        usage()
        exit(-1)
