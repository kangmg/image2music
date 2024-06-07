# 파일 설명

### 1. meta data 수집
   
- `LASTFM_API_selenium.ipynb` : LastFM API를 통해서 수집한 meta data로부터 youtube url을 크롤링하는 노트북

- `api_utils_selenium.py` : `LASTFM_API_selenium.ipynb`에 필요한 모듈 파일

- `mood_data_csv/*` : LASTFM_API_selenium.ipynb을 통해서 수집한 meta data


### 2. mel spectrogram 획득

- `get_mel_spectrogram.ipynb` : `mood_data_csv/*` 파일로부터 각 노래들을 크롤링한 후 mel spectrogram으로 변환하는 노트북

- mel spectrogram 데이터 파일 : 아래 코드를 통해서 다운로드 가능
  
```bash
# mel spectrogram data 다운로드 코드
wget 'https://drive.usercontent.google.com/download?id=1oZtD1S_vDFRbtFC0hXqemJFxy7FWw7sw&export=download&authuser=1&confirm=t' -O ./mel_spectrogram.zip
```
