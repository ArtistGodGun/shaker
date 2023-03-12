# shaker-music-engine

## 230312
### install (for Colab)
```shell
!sudo apt install -y fluidsynth
!pip install --upgrade pyfluidsynth
!sudo apt install ffmpeg
!pip install -r requirements.txt
```
### using
```shell
# -1 is ALL example File Generator
python main.py -1
# 0~11
# 0: 'dancingqueen',
# 1: 'getlucky',
# 2: 'dandan',
# 3: 'celebrity',
# 4: 'boongboong',
# 5: '1245',
# 6: 'flytothemoon',
# 7: 'grenade',
# 8: 'dynamite',
# 9: 'her',
# 10: 'hobbang',
# 11: 'test'
python main.py 0
```

## 220706
### install
* ffmpeg과 fluidsynth가 설치되어 있어야 합니다
```shell
brew install ffmpeg
brew install fluidsynth
```
* 패키지 설치
```shell
pip install -r requirements.txt
```
### using
* 곡선택 (main.py)
    - line32 - song_num 번호 선택 (-1 : 전체곡, 0~13 : 각 곡)
* 장르선택 (main.py)
    - line40 - GenreList.bossa 또는 GenreList.newage를 변경하여 선택
* 속도선택 (main.py)
    - line 41 - 리스트 ['orig', 'fast', 'slow'] 중 변경하여 선택
* 커맨드 입력
```shell
python main.py

-> output/xxx.midi and xxx.mp3
```
### 결과물 설명
* midi - 미디파일
* audio - DirectAudio + ReverbAudio
* 결과물 갯수 = 곡 종류 * 장르 종류 * bpm종류
* 같은 곡, 같은 장르여도 bpm에 따라 음악이 다름 (단순 빠르고 느린게 아님)

### 기타 설명
* input(folder) : 테스트 미디파일이 들어있는 폴더
* output(folder) : 결과파일이 저장될 폴더
* SGM.SF2 : 사운드폰트파일
* ir.wav : 리버브에 쓰이는 Pulse


## 220627
### Quick Start
* 곡 선택
- main.py - line29 -  song_num의 번호 선택
* 장르 선택
- main.py - line57 - GenreList선택


## 220603
### Quick Start
* pip install mido
- 실행 : python main.py
- main.py -> line 26의 번호를 수정하여 원하는 곡을 편곡 (-1 : 전곡, 0~12 : 각 곡의 index)
- 결과물 : output/

### FLOW
#### 1.Parser
- 미디파일을 읽음
- tick(int), bpm(float), key(int), melody_structure(list), chord_info(list) 리턴
- tick : 한 박자의 tick 수 
- bpm : 미디파일의 BPM
- key : 미디파일의 키(문자열)을 basic_note_number에 따라 변경
- melody_structure : [[노트, 길이], [노트, 길이], ...]의 형태로 변경
- chord_info : [[코드테이블넘버, 길이], [코드테이블넘버, 길이],....]의 형태로 변경

#### 2.Reharmonization
- 원곡 코드를 변형해주는 부분
- Parser의 결과 값을 입력 받음
- 현재 대리코드 수준의 리하모니제이션까지 가능
- 멜로디와 코드를 비교하여 적절한 대리코드 추천
- [[코드테이블넘버, 길이], [코드테이블넘버, 길이],....]의 형태를 리턴
#### 3.MakeStructure
- 송폼을 구분하여 장르와 곡에 따라 적절한 코드, 아르페지오 패턴을 적용함
- 최소 4마디 단위로 송폼을 구분. 220603 기준 송폼에 큰 의미는 없음
- [[코드테이블넘버, 길이], [코드리듬], [아르페지오리듬], [아르페지오노트]] 의 형태로 리턴
- 가장 많은 연구와 분석이 필요한 부분

#### 4.SetScore
- MakeStructure의 결과값을 미디포맷에 맞게 변형해주는 부분
- 코드 보이싱, 코드 노트 값, 코드 리듬을 설정
- 아르페지오 노트 값, 아르페지오 리듬을 설정
- 코드와 아르페지오로 나뉘어서 리턴
#### 5.Generator
- 멜로디, 코드, 아르페지오를 미디파일로 출력해주는 부분
- 4.SetScore를 기계적으로 미디화 하는 부분
- output/곡이름_result_장르.mid 경로로 저장
#### 0.common
- 어느 모듈에서든 공통으로 쓰이는 기준값 및 함수를 모아놓은 부분


## 220519
- Git 생성
