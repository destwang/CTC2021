# coding:utf-8


import sys
import Levenshtein
import json


src_path = sys.argv[1]
tgt_path = sys.argv[2]
sid_path = sys.argv[3]

with open(src_path) as f_src, open(tgt_path) as f_tgt, open(sid_path) as f_sid:
    lines_src = f_src.readlines()
    lines_tgt = f_tgt.readlines()
    lines_sid = f_sid.readlines()
    assert len(lines_src) == len(lines_tgt) == len(lines_sid)

    for i in range(len(lines_src)):
        src_line = lines_src[i].strip().replace(' ', '')
        tgt_line = lines_tgt[i].strip().replace(' ', '')
        sid = lines_sid[i].strip().split('\t')[0]
        edits = Levenshtein.opcodes(src_line, tgt_line)
        result = []
        for edit in edits:
            if "。" in tgt_line[edit[3]:edit[4]]: # rm 。
                continue
            if edit[0] == "insert":
                result.append((str(edit[1]), "缺失", "", tgt_line[edit[3]:edit[4]]))
            elif edit[0] == "replace":
                result.append((str(edit[1]), "别字", src_line[edit[1]:edit[2]], tgt_line[edit[3]:edit[4]]))
            elif edit[0] == "delete":
                result.append((str(edit[1]), "冗余", src_line[edit[1]:edit[2]], ""))

        out_line = ""
        for res in result:
            out_line +=  ', '.join(res) + ', '
        if out_line:
            print(sid + ', ' + out_line.strip())
        else:
            print(sid + ', -1')


