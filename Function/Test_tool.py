import read_info
import json



if __name__ == '__main__':
    #abc=r'/Users/youdrew/Documents/AMF/Test_file/amf-util-master/amf_TEST/Rec.709-Rec.709100nitsdim.amf'
    abc = r'/Users/youdrew/Documents/AMF/Test_file/论文测试文件/0306/Isabella_trial.amf'
    i,j,m,n=read_info.Printinfo(abc)
    print(json.dumps(i, sort_keys=False, indent=4))
    print(json.dumps(j, sort_keys=False, indent=4))
    print(json.dumps(m, sort_keys=False, indent=4))
    print(json.dumps(n, sort_keys=False, indent=4))
    #print(i,'\n',j,'\n',m,'\n',n)

