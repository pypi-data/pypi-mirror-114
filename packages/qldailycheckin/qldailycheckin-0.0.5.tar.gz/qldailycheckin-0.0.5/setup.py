from setuptools import setup,find_packages

setup(
            name='qldailycheckin',
                version='0.0.5',
                    author='yuxian158',
                        author_email='yuxian158@gmail.com',
                            url='https://sitoi.gitee.io/dailycheckin/',
                                packages=find_packages(),
                                    install_requires=[],
                                        entry_points={
                                                    'console_scripts': [
                                                                    'qldailycheckin=dailycheckin.main:checkin'
                                                                            ]
                                                        }
                                        )
