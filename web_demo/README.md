## streamlit 데모 웹페이지

- ngrok 기반 데모 웹
  - 빠르지만 Token 발급 필요.
    - [ngrok 페이지](https://ngrok.com/)에서 회원가입 후 Authtoken 발급

- localtunnel 기반 웹
  - 느리지만 Token 정보 필요 X

### 사용 방법 

- 아래 colab demo notebook 실행시 streamlit page 접속 링크 확인 가능
- LLM API를 지정해주지 않으면 Playground & LLM으로 추천 받기 기능 사용 불가
  - LLAMA API는 주석처리된 API 사용
  - ChatGPT는 발급 필요
  - Solar, Mistral, Gemini는 무료 리소스를 이용
  

### Colab Demo

| Colab NoteBook | Web Service |
|:-:|:-:|
| <a target="_blank" href="https://colab.research.google.com/github/kangmg/image2music/blob/main/web_demo/MOODSic_localtunnel.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | localtunnel |
| <a target="_blank" href="https://colab.research.google.com/github/kangmg/image2music/blob/main/web_demo/MOODSic_ngrok.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | ngrok | 
