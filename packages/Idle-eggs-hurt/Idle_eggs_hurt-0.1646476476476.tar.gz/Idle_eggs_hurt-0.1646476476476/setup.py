from setuptools import setup, find_packages

setup(
    name='Idle_eggs_hurt',#包名
    version='0.1646476476476',#版本
    description="test",#包简介
    long_description=open('README.md').read(),#读取文件中介绍包的详细内容
    include_package_data=True,#是否允许上传资源文件
    author='PYmili',#作者
    author_email='2097632843@qq.com',#作者邮件
    maintainer='PYmili',#维护者
    maintainer_email='2097632843@qq.com',#维护者邮件
    license='MIT License',#协议
    url='',#包存放地址
    packages=find_packages(),#包的目录
    package_data={
        'cropgbm': ['testdata/*']
    },#包的依赖
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
],
    python_requires='>=3',
    
)
