import os, sys, zipfile
from PIL import Image
import tempfile, shutil

def process_zip(zip_path):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(temp_dir)

    # 画像ファイル名に接頭辞を付与
    for dir_path, _, file_names in os.walk(temp_dir):
        for file_name in file_names:
            if file_name.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg', '.webp')):
                old_path = os.path.join(dir_path, file_name)
                new_name = 'target_' + file_name
                new_path = os.path.join(dir_path, new_name)
                os.rename(old_path, new_path)

    # 画像変換
    for dir_path, _, file_names in os.walk(temp_dir):
        for file_name in file_names:
            if file_name.startswith('target_') and file_name.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg', '.webp')):
                image_path = os.path.join(dir_path, file_name)
                try:
                    image = Image.open(image_path).convert('RGB')
                    width, height = image.size
                    if height != 1080:
                        new_width = int(width * 1080 / height)
                        image = image.resize((new_width, 1080), Image.LANCZOS)
                    base_name = os.path.splitext(file_name)[0].replace('target_', '')
                    new_image_path = os.path.join(dir_path, base_name + '.jpg')
                    image.save(new_image_path, 'JPEG', quality=85)
                except Exception as e:
                    print("Error:", image_path, e)

    # target_で始まるファイルを削除
    for dir_path, _, file_names in os.walk(temp_dir):
        for file_name in file_names:
            if file_name.startswith('target_'):
                try:
                    os.remove(os.path.join(dir_path, file_name))
                except Exception as e:
                    print("Error removing:", file_name, e)

    # 元ファイル削除して再作成
    os.remove(zip_path)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for dir_path, _, file_names in os.walk(temp_dir):
            for file_name in file_names:
                full_path = os.path.join(dir_path, file_name)
                relative_path = os.path.relpath(full_path, temp_dir)
                zip_file.write(full_path, relative_path)
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python script.py <対象フォルダ>")
    else:
        for dir_path, _, file_names in os.walk(sys.argv[1]):
            for file_name in file_names:
                if file_name.lower().endswith('.zip'):
                    process_zip(os.path.join(dir_path, file_name))
