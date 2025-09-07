# compress_image_tool
A tool to compress images into archive files to save space on your PC

# Operating environment

Windows 11

# Support extension

### Target file
- zip
- rar

### Target image
- jpg
- png
- bmp
- webp

# Prerequisite

Install the followings.
- 7-Zip
- Python
- Pillow
    ```bash
    pip install pillow
    ```
- rarfile
    ```bash
    pip install rarfile
    ```

# How to use

```bash
python compress_image_tool.py "C:\path\to\target_folder"
```