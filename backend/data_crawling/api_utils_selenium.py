import pandas as pd
import urllib
import json
from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm.notebook import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings('ignore')


if __IPYTHON__:
  from tqdm.notebook import tqdm
else:
  from tqdm import tqdm

  # 한글 -> 영어 변환
MOOD_TAGS_CONVERSION = {
    "가벼운"            :   "Light",
    "감상적인"          :   "Sentimental",
    "강렬한"            :   "Intense",
    "강한"              :   "Strong",
    "고양되는"          :   "Uplifting",
    "공격적인"          :   "Aggresive",
    "관능적인"          :   "Sensual",
    "구슬픈"            :   "Melancholy",
    "극적인"            :   "Dramatic",
    "긍정적인"          :   "Positive",
    "꿈꾸는 듯한"       :   "Dreamy",
    "낭만적인"          :   "Romantic",
    "달콤한"            :   "Sweet",
    "따뜻한"            :   "Warm",
    "무서운"            :   "Scary",
    "밝은"              :   "Bright",
    "복잡한"            :   "Complex",
    "부드러운"          :   "Smooth",
    "분위기 있는"       :   "Atmospheric",
    "사나운"            :   "Fierce",
    "사랑스러운"        :   "Lovely",
    "서정적인"          :   "Lyrical",
    "섹시한"            :   "Sexy",
    "슬프고도 아름다운" :   "Bittersweet",
    "슬픈"              :   "Sad",
    "신나는"            :   "Exciting",
    "신비한"            :   "Mysterious",
    "심각한"            :   "Serious",
    "외로운"            :   "Lonely",
    "우울한"            :   "Gloomy",
    "웅장한"            :   "Epic",
    "자신만만한"        :   "Confident",
    "잔잔한"            :   "Calm",
    "재미있는"          :   "Fun",
    "점잖은"            :   "Gentle",
    "정력적인"          :   "Energetic",
    "진지한"            :   "Earnest",
    "질주하는"          :   "Driving",
    "차가운"            :   "Cold",
    "친밀한"            :   "Intimate",
    "쾌활한"            :   "Cheerful",
    "편안한"            :   "Relaxed",
    "행복한"            :   "Happy",
    "향수어린"          :   "Nostalgic",
    "화난"              :   "Angry"
}

# 영어 -> 한글 변환
MOOD_TAGS_CONVERSION_REVERSE = {v: k for k, v in MOOD_TAGS_CONVERSION.items()}

# 감정 태그 리스트
AVAILABLE_MOOD_TAGS_KOR = list(MOOD_TAGS_CONVERSION.keys())
AVAILABLE_MOOD_TAGS_EN  = list(MOOD_TAGS_CONVERSION.values())


# 13가지 무드 정보
A_cluster = {"MOOD" : ["Amusing"]}
B_cluster = {"MOOD" : ["Annoying"]}
C_cluster = {"MOOD" : ["Anxious","Tense"]}
D_cluster = {"MOOD" : ["Beautiful"]}
E_cluster = {"MOOD" : ["Calm","Relaxing"]}
F_cluster = {"MOOD" : ["Dreamy"]}
G_cluster = {"MOOD" : ["Energizing","Pump-up"]}
H_cluster = {"MOOD" : ["Erotic"]}
I_cluster = {"MOOD" : ["Defiant"]}
J_cluster = {"MOOD" : ["Joyful","Cheerful"]}
K_cluster = {"MOOD" : ["Sad","Depressing"]}
L_cluster = {"MOOD" : ["Scary"]}
M_cluster = {"MOOD" : ["Triumphant","Heroic"]}

clusters = [A_cluster, B_cluster, C_cluster, D_cluster, E_cluster, F_cluster, G_cluster, H_cluster, I_cluster, J_cluster, K_cluster, L_cluster, M_cluster]
clusters_name = ["A_cluster", "B_cluster", "C_cluster", "D_cluster", "E_cluster", "F_cluster", "G_cluster", "H_cluster", "I_cluster", "J_cluster", "K_cluster", "L_cluster", "M_cluster"]



def get_API_result(moodTag:str, API_KEY, result_max=222)->dict:
  """
  Last.FM API를 이용한 mood tag 기반 음악 검색 API 함수
  """
  # api 결과 받기
  API_URL = f"https://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={moodTag}&limit={result_max}&api_key={API_KEY}&format=json"
  with urllib.request.urlopen(API_URL) as response:
    status = response.status
    if status == 200:
      result = response.read().decode()
      json_data = json.loads(result)
      return json_data
    else:
      raise Exception(f"Fail to get API response.\n\nStatus code : {status}")


def data_formatter(API_result:dict, moodTag:str, save_csv=False)->pd.DataFrame:
  """
  Description
  -----------
  API 결과를 DataFrame으로 변환하는 함수

  Parameters
  ----------
  -  API_result(dict)  : Last FM API 반환 결과
  -  moodTag(str)      : mood tag ( AVAILABLE_MOOD_TAGS_EN 에 포함된 태그 )
  -  save_csv(bool)    : csv 파일로 저장 여부
    - True  : csv 파일로 저장
    - False : DataFrame 반환

  Returns
  -------
  - DataFrame
  """
  # inner funciton for data parsing
  def parser(single_music:dict, moodTag:str)->dict:
    music_name = single_music["name"]
    duration = single_music["duration"]
    artist = single_music["artist"]["name"]
    lastfm_url = single_music["url"]
    return {"artist":artist, "music_name":music_name, "duration":duration, "lastfm_url":lastfm_url, 
            "youtube_url": None, "mood_EN":moodTag, "mood_KOR": MOOD_TAGS_CONVERSION_REVERSE[moodTag] if moodTag in AVAILABLE_MOOD_TAGS_KOR else None}

  music_list = API_result["tracks"]["track"]
  parsed_music_list = list(parser(music, moodTag) for music in music_list)
 
  # API 결과를 DataFrame으로 변환
  df = pd.DataFrame(parsed_music_list)

  # df 반환 또는 csv로 저장
  if save_csv:
    df.to_csv(f"./mood_data_csv/{moodTag}.csv", index=False)
  else:
    return df
  
def get_yotube_url(df:pd.DataFrame, driver):
  '''
  Description
  -----------
  df에서 LastFM url을 찾아 selenium webdriver에서 접속 후 youtube url을 파싱 --> df에 추가하는 함수

  Parameter
  ---------
  - df(pd.DataFrame) : lastfm_url 행으로 가지고 youtube_url 행은 NaN 값으로 가지고 있는 df
  - driver : selenium driver 
  '''
  warnings.filterwarnings('ignore')
  total = df.shape[0]
  for row in tqdm(df.iterrows(), total=total):
    
    if row[1].loc[["youtube_url"]].isnull().item():
      try:
        # 랜덤 시간 대기
        random_sleep_time = random.uniform(0.7, 2)
        sleep(random_sleep_time)
        # yt url 획득
        lastfm_url = row[1]["lastfm_url"]
        driver.get(lastfm_url)
        # YouTube 링크 요소를 찾을 때까지 최대 10초 대기
        wait = WebDriverWait(driver, 10)
        yt_ele = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mantle_skin > header > div.header-new-inner > div.header-new-content > div > div > a')))
        # YouTube 링크 획득
        yt_url = yt_ele.get_attribute('href')
        df.loc[row[0], 'youtube_url'] = yt_url
      except:
        pass