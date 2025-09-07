import os, sys, zipfile
from PIL import Image
import tempfile, shutil
import rarfile

def process_archive(archive_path):
    temp_dir = tempfile.mkdtemp()
    ext = os.path.splitext(archive_path)[1].lower()
    # 展開
    if ext == ".zip":
        with zipfile.ZipFile(archive_path, 'r') as arc:
            arc.extractall(temp_dir)
    elif ext == ".rar":
        with rarfile.RarFile(archive_path, 'r') as arc:
            arc.extractall(temp_dir)
    else:
        print(f"未対応のファイル: {archive_path}")
        shutil.rmtree(temp_dir)
        return

    # 対象画像ファイルリスト表示
    image_files = []
    for dir_path, _, file_names in os.walk(temp_dir):
        for file_name in file_names:
            if file_name.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg', '.webp')):
                image_files.append(os.path.join(dir_path, file_name))

    # 画像ファイル名に接頭辞を付与
    for image_path in image_files:
        dir_path, file_name = os.path.split(image_path)
        new_name = 'target_' + file_name
        new_path = os.path.join(dir_path, new_name)
        os.rename(image_path, new_path)

    # 画像変換
    target_files = []
    for dir_path, _, file_names in os.walk(temp_dir):
        for file_name in file_names:
            if file_name.startswith('target_') and file_name.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg', '.webp')):
                target_files.append(os.path.join(dir_path, file_name))
    for image_path in target_files:
        try:
            image = Image.open(image_path).convert('RGB')
            width, height = image.size
            if height != 1080:
                new_width = int(width * 1080 / height)
                image = image.resize((new_width, 1080), Image.LANCZOS)
            base_name = os.path.splitext(os.path.basename(image_path))[0].replace('target_', '')
            new_image_path = os.path.join(os.path.dirname(image_path), base_name + '.jpg')
            image.save(new_image_path, 'JPEG', quality=85)
        except Exception as e:
            print("Error:", image_path, e)

    # target_で始まるファイルを削除
    for image_path in target_files:
        try:
            os.remove(image_path)
        except Exception as e:
            print("Error removing:", image_path, e)

    # 元ファイル削除して再圧縮（RARもZIPにする）
    os.remove(archive_path)
    zip_path = os.path.splitext(archive_path)[0] + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as dest_file:
        for dir_path, _, file_names in os.walk(temp_dir):
            for file_name in file_names:
                full_path = os.path.join(dir_path, file_name)
                relative_path = os.path.relpath(full_path, temp_dir)
                dest_file.write(full_path, relative_path)
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python compress_image_tool.py <対象フォルダ>")
    else:
        archive_files = []
        for dir_path, _, file_names in os.walk(sys.argv[1]):
            for file_name in file_names:
                if file_name.lower().endswith('.zip') or (file_name.lower().endswith('.rar')):
                    archive_files.append(os.path.join(dir_path, file_name))
        print(f"対象アーカイブファイル数: {len(archive_files)}")
        for f in archive_files:
            print(f"  - {f}")
        total = len(archive_files)
        print(f"\n=== 開始 ==================== 進捗: 0%")
        for idx, archive_path in enumerate(archive_files):
            print(f"{archive_path}")
            process_archive(archive_path)
            percent = int((idx+1) / total * 100)
            print(f"=== アーカイブ({idx+1}/{total}) 完了 === 進捗: {percent}%")
