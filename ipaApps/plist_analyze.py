# -*- coding: Shift_JIS -*-
import plistlib
import json

def read_plist_file(plist_file_path):
    try:
        with open(plist_file_path, 'rb') as fp:
            plist_data = plistlib.load(fp)
        return plist_data
    except FileNotFoundError:
        print("指定したファイルが見つかりません。")
    except plistlib.InvalidFileException:
        print("無効なplistファイルです。")

if __name__ == "__main__":
    plist_file_path = "E:\ipafiles\Apps\extracted_ipa\Payload\YouTube.app\Info.plist"  # 実際のplistファイルのパスに置き換えてください
    plist_data = read_plist_file(plist_file_path)
    if plist_data:
        formatted_data = json.dumps(plist_data, indent=4)
        print(formatted_data)
