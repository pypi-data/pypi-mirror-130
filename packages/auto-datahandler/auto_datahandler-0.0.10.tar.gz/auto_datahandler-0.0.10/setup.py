import setuptools

setuptools.setup(
    name="auto_datahandler", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.10", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    updatetime="20211210",
    author="唐国钦", #作者
    author_email="dreamertgq@163.com", #邮箱
    description="数据（段落、评论、图片、视频）的自动化处理 在之前项目packageDIY的基础上进行代码的简化和整合", #描述
    long_description='数据（段落、评论、图片、视频）的自动化处理 在之前项目packageDIY的基础上进行代码的简化和整合', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://github.com/Tommy-pixels/auto_datahandler", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    REQUIRED = [
        'requests', 'pymysql', 'baidu-aip','beautifulsoup4','fake-useragent','matplotlib',
        'opencv-python','openpyxl','Pillow','PyAutoGUI','requests','requests-toolbelt',
        'Scrapy','scrapy-splash','selenium','xlrd', 'moviepy', 'openpyxl'
    ],
    python_requires='>=3.6.8',  #支持python版本
)