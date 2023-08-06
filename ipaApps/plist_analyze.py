# -*- coding: Shift_JIS -*-
import plistlib
import json

def read_plist_file(plist_file_path):
    try:
        with open(plist_file_path, 'rb') as fp:
            plist_data = plistlib.load(fp)
        return plist_data
    except FileNotFoundError:
        print("�w�肵���t�@�C����������܂���B")
    except plistlib.InvalidFileException:
        print("������plist�t�@�C���ł��B")

if __name__ == "__main__":
    plist_file_path = "E:\ipafiles\Apps\extracted_ipa\Payload\YouTube.app\Info.plist"  # ���ۂ�plist�t�@�C���̃p�X�ɒu�������Ă�������
    plist_data = read_plist_file(plist_file_path)
    if plist_data:
        formatted_data = json.dumps(plist_data, indent=4)
        print(formatted_data)
