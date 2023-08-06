# Python Advanced - 4

## [오픈소스 프로젝트 참가 의미](./chapter04_01.py)

- 오픈소스 프로젝트 참가 장점

## [오픈소스 참여 - 나만의 패키지 만들기 - 1](./chapter04_02.py)

```shell
../../virtual_environment/bin/pip install Pillow
```

- 애니메이션 이미지 변환 패키지 작업
- PNG, JPG to GIF Converter

## [오픈소스 참여 - 나만의 패키지 만들기 - 2](./chapter04_03.py)

- 애니메이션 이미지 변환 패키지 작업
- 클래스, 배포 배키지 형태로 작성

## [오픈소스 참여 - 나만의 패키지 만들기 - 3.1](./chapter04_04.py)

### PyPi에 배포하기

1. [PyPi 회원 가입](https://pypi.org/)
    - `ID`는 설정한 닉네임이 된다.
2. 설치
    1. 가상 환경을 사용할 경우
   ```shell
   # 설치가 되어 있으면 업그레이드 하는 옵션 : --upgrade
   python -m pip install --upgrade setuptools wheel
   ```
    2. 가상 환경을 사용하지 않을 경우
   ```shell
   python -m pip install --user --upgrade setuptools wheel
   ```
3. 빌드

```shell
python ./project/upload_package/setup.py sdist bdist_wheelD
```

### 프로젝트 구조 확인

- [upload_package](./project/upload_package)
    - [pygifconvt_test_bell_stone](./project/upload_package/pygifconvt_test_bell_stone) : 배포할 모듈이 있는 패키지
        - 배포할 패키지 명과 동일하게 작성하는 것을 권장한다.
        - [__init__.py](./project/upload_package/pygifconvt_test_bell_stone/__init__.py) : 반드시 작성해야 패키지로 인식한다.
        - [converter.py](./project/upload_package/pygifconvt_test_bell_stone/converter.py) : 배포하기 위해 작성한 모듈
    - [LICENSE](./project/upload_package/LICENSE) : 라이센스
    - [MANIFEST.in](./project/upload_package/MANIFEST.in) : 부가적인 파일을 빌드업 할 때 포함시킨다.
    - [README.md](./project/upload_package/README.md) : 사용 설명서
    - [requirements.txt](./project/upload_package/requirements.txt) : 패키지를 사용하기 위해 필수적인 모듈
    - [.gitignore](./project/upload_package/.gitignore) : 보통 `PyPI`와 `Github`에 함께 배포하기 때문에, `.gitignore`을 추가하여 불필요한 파일이
      업로드 되지 않게 한다.
    - [setup.cfg](./project/upload_package/setup.cfg) : Optional
    - [setup.py](./project/upload_package/setup.py) : `pypi`에 배포하기 위한 `setup`파일, 아래의 설명 참고

### [setup.py](./project/upload_package/setup.py)

- `name` : 배포할 패키지 이름
- `version` : 버전
- `description` : 설명
- `author` : 제작자
- `author_email` : 제작자의 이메일
- `url` : 해당 패키지의 관련 url
- `install_requires` = 해당 패키지를 사용하기 위해 필수적인 것들
    - 작성되어 있으면 해당 패키지를 설치할 때 같이 설치해준다.
- `include_package_data=True` : 필수
- `package = find_package()`
    - 여기에서는 `setup.py`가 있는 `pygifconvt_test_bell_stone`이 된다.
        - 잘 모르겠으면 같은 경로에 두면 된다.
- `keyword` : 검색할 때 검색이 되도록 설정하는 키워드
- `python_requires` : 최소 파이썬 요구 버전
- `classifiers` : [pypi-classifiers](https://pypi.org/classifiers) 를 참고하여 형식에 맞게 작성한다.

- PyPl Package Deploy

## [오픈소스 참여 - 나만의 패키지 만들기 - 3.2](./)

## 오픈소스 참여 - 나만의 패키지 만들기 - 4

- Github Python 패키지 구조 설명
- Github Package Deploy