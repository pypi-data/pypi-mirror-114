import setuptools

# with open('README.md', encoding='utf-8') as f: # README.md 내용 읽어오기
#         long_description = f.read()

setuptools.setup(
    name='rainod', # 패키지 명
    version='1.0.7',
    description='2조 패키지',
    author='dojun',
    author_email='ehwns4337@naver.com',
    url='',
    license='MIT', # MIT에서 정한 표준 라이센스 따른다
    #py_modules=['rb'], # 패키지에 포함되는 모듈
    python_requires='>=3',
    install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지
    packages=setuptools.find_packages(), # 패키지가 들어있는 폴더들
)