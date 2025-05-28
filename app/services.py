import requests


def translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Переводит название города с помощью MyMemory API.
    """
    url = 'https://api.mymemory.translated.net/get'
    params = {
        'q': text,
        'langpair': f'{source_lang}|{target_lang}'
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        result = response.json()
        return result['responseData']['translatedText']
    except Exception as e:
        print(f'Translation error: {e}')
        return text
