from setuptools import setup

setup(
    name='qldailycheckin',
    version='0.0.3',
    author='yuxian158',
    author_email='yuxian158@gmail.com',
    url='https://sitoi.gitee.io/dailycheckin/',
    packages=['dailycheckin'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'qldailycheckin=dailycheckin.main:checkin'
        ]
    }
)
