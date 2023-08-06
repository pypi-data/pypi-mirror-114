# ********************************************************************************
# FileName : setup
# Description : et보드 전체 패키지의 setup파일
# Author : KETRi
# Created Date : 2021.07.23
# Reference : 패키지를 작성하는 기초적인 방법은 다음 링크를 참고
#             https://packaging.python.org/tutorials/packaging-projects/
#             패키지를 새로 인덱스에 업로드 할 때는 버전넘버도 변경되어야함
#             버전넘버를 변경하지 않고 업로드를 시도하면 실패함
#             이 패키지는 하위 패키지들을 설치하는 패키지임
#             실제하는 작업은 하위 패키지들만 설치하는 작업을 진행함
#             package_data에서 실제 필요한 파일들을 포함할 수 있음
#             포함해야하는 파일이 있다면 여기에 추가, 일부 glob패턴을 지원함
#             install_requires에서 thonny를 반드시 포함할 것
#             install_requires에서 설치해야할 패키지의 이름을 등록하면 같이 설치됨
# Modified : 2021.07.23 : WDW : 헤더수정
# ********************************************************************************

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thonny-etboard-all",
    version="0.0.1",
    author="KETRi",
    author_email="ketri3000@gmail.com",
    description="ET보드 전체 패키지",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://et.ketri.re.kr/",
    project_urls={
        "Bug Tracker": "http://et.ketri.re.kr/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["thonnycontrib.thonny_etboard_all"],
    package_data={"thonnycontrib.thonny_etboard_all" : ["*", "*/*", "*/*/*", "*/*/*/*", "*/*/*/*/*"]},
    install_requires = ["thonny>=3.3.11", "thonny-etboard-basic-examples", "thonny-etboard-micropython-firmware"],
    python_requires=">=3.6",
)