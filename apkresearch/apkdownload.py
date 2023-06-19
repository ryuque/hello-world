# -*- coding: utf-8 -*-

import csv

from re import A
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
import os
from androguard.misc import AnalyzeAPK
import zipfile
import shutil

def delete_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def extract_xapk(xapk_file_path, output_directory):
    with zipfile.ZipFile(xapk_file_path, 'r') as xapk_zip:
        for member in xapk_zip.namelist():
            if member.lower().endswith('.apk'):
                # APKファイルを抽出
                xapk_zip.extract(member, output_directory)
            elif member.lower().endswith('.obb'):
                # OBBファイルを抽出
                xapk_zip.extract(member, output_directory)

def check_elements(elements):
    if not elements:  # Check if permissions is empty
        return 0
    elif len(elements) == 1:  # Check if permissions has only one element
        return 1
    else:
        return 2

def delete_file(file_path):
    # Check if file exists before trying to delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"The file {file_path} has been deleted successfully.")
    else:
        print("The file does not exist.")

def find_apk_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".apk") or file.endswith(".xapk"):
                return file

def find_apkmain_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".apk") and not file.startswith("config."):
                yield os.path.join(root, file)

def extract_apis_and_permissions(apk_path):
    a, d, dx = AnalyzeAPK(apk_path)
    permissions = a.get_permissions()

    return permissions

def is_download_finished(download_folder):
    for filename in os.listdir(download_folder):
        if filename.endswith('.crdownload'):  # Chromeはダウンロード中のファイルにこの拡張子を付けます
            return False

    return True

def download_apk(keyword):
    try:
    
        # ChromeのWebDriverオブジェクトを作成します
        driver = webdriver.Chrome('/mnt/c/chromedriver_win32/chromedriver.exe')

        # APKPureのウェブサイトを開きます
        driver.get('https://m.apkpure.com/jp/search?q='+keyword)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'first-info')))
        # ダウンロードリンクをクリックします
        element = driver.find_element(By.CLASS_NAME, "first-info")
        link = element.get_attribute('href')

        driver.get(link+'/download')
    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'download-start-btn')))
        # ダウンロードリンクをクリックします
        element = driver.find_element(By.CLASS_NAME, "download-start-btn")

        link = element.get_attribute('href')
        print(link)
        driver.get(link)
        time.sleep(10)
    
        #driver.find_element(By.CLASS_NAME, "download-start-btn").click()
        # ダウンロードフォルダを指定します
        download_folder = '/mnt/c/users/ryutaro/downloads'

        # ダウンロードが完了するまで待ちます
        while not is_download_finished(download_folder):
            time.sleep(1)

        print('Download finished.')
    

    except Exception as e:
        print("An error occurred: ", e)

    finally:
        # ブラウザを閉じます
    
        print("Compleat download")

def delete_obb_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".obb"):
                file_path = os.path.join(root, file)
                delete_file(file_path)

def research(keyword):

    print(f"Searching for APP: {keyword}")
    download_apk(keyword)

    directory = "/mnt/c/users/ryutaro/downloads"  # ここに探索するディレクトリのパスを入力してください
    file_name = find_apk_files(directory)

    if file_name is None:
        print(f"No APK file found for: {keyword}")
        return  0,0,0           # APKファイルが見つからない場合、次のキーワードに進みます

    print(f"Extracting permissions for: {file_name}")
    file_path = os.path.join("/mnt/c/users/ryutaro/downloads", file_name)

    if file_name.endswith('.xapk'):
        extract_xapk(file_path, directory)
        delete_obb_files(directory)
        for file_name in find_apkmain_files(directory):

            if file_name is None:
                print(f"No APK file found in the extracted XAPK for: {keyword}")
                return 0,0,0
            file_path = os.path.join(directory, file_name)
            permissions = []
            permissions.extend(extract_apis_and_permissions(file_path))

    else:
        permissions = extract_apis_and_permissions(file_path)
    
    delete_all_files(directory)
    return 1, permissions, file_name


if __name__ == "__main__":

    with open("output_result.csv", 'w', newline='', encoding='utf-8_sig') as f:
        writer = csv.DictWriter(f, fieldnames=['App Name', 'App ID', 'Genre', 'Installs','APK_file_name'])
        writer.writeheader()

    try:
        # CSVファイルからキーワードを取得
        with open('output.csv', 'r', encoding='utf-8_sig') as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダー行をスキップ
            for row in reader:  # 2行目以降を読み取ります

                suc, permissions, file_name = research(row[0])

                if suc is 1:
                    with open("output_result.csv", 'a', newline='', encoding='utf-8_sig') as f:
                        writer = csv.writer(f)
                        num = check_elements(permissions)
                        if num is 0:
                            writer.writerow(row+[file_name])
                        elif num is 1:
                            writer.writerow(row+[file_name]+[permissions])
                        else:
                            writer.writerow(row+[file_name]+permissions)

                # ここで行ごとの処理を行います

    except FileNotFoundError:
        print("CSV file not found.")
        exit(1)
    except IndexError:
        print("Error occurred while reading CSV file.")
        exit(1)

    
    print("Task Complete")












