import streamlit as st
import os
import tempfile
import PyPDF2
import os
import zipfile

def split_pdf_by_page_count(input_pdf_path, output_folder=None, pages_per_file=50):
    if not output_folder:
        output_folder = input_pdf_path.replace('.pdf','')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开PDF文件
    reader = PyPDF2.PdfReader(input_pdf_path)
    total_pages = len(reader.pages)

    file_counter = 1
    output_file_start = input_pdf_path.split('/')[-1].replace('.pdf', '')
    # 遍历PDF的所有页面
    for start_page in range(0, total_pages, pages_per_file):
        end_page = min(start_page + pages_per_file, total_pages)

        output_filename = os.path.join(output_folder, f'{output_file_start}_part_{file_counter}.pdf')
        print('saved:', output_filename)
        with open(output_filename, 'wb') as output_file:
            writer = PyPDF2.PdfWriter()
            for page_number in range(start_page, end_page):
                page = reader.pages[page_number]
                writer.add_page(page)
            writer.write(output_file)

        file_counter += 1
    
    folder_to_zip(output_folder, f'{output_folder}.zip')
    print(f'PDF has been split into {file_counter - 1} files.')
    print('os.list:', os.listdir(output_folder))
    return f'{output_folder}.zip'



def folder_to_zip(folder_path, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    print(f'Folder {folder_path} has been successfully zipped to {zip_filename}.')

# 使用示例
folder_path = 'path_to_your_folder'  # 替换为你想要打包的文件夹路径
zip_filename = 'output_zip_filename.zip'  # 替换为你想要创建的zip文件的名称
folder_to_zip(folder_path, zip_filename)

st.title("PDF分割器")
st.text("请上传文件")
pages_per_file = st.text_input("分割页数", value=50)
uploaded_file = st.file_uploader("请选择文件进行上传", type=["pdf"])

if uploaded_file is not None :
    if st.button('确认分割'):
        try:
            pages = int(pages_per_file)
        except:
            st.warning('页数格式错误！')
        if pages < 0:
            st.warning('页数不能小于0！')
        if pages == 0:
            st.warning('页数为0')
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as buffer:
                    buffer.write(uploaded_file.getbuffer())
                    print('file_path:', file_path)
                    zip_filepath = split_pdf_by_page_count(file_path, pages_per_file=pages)
                    download_link = st.download_button(label="下载文件", data=open(zip_filepath, "rb"), file_name=zip_filepath.split('/')[-1])


