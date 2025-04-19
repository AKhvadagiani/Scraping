import nltk
import warnings
import requests
import time



nllb_langs = {
    "af": "afr_Latn",
    "ak": "aka_Latn",
    "am": "amh_Ethi",
    "ar": "arb_Arab",
    "as": "asm_Beng",
    "ay": "ayr_Latn",
    "az": "azj_Latn",
    "bm": "bam_Latn",
    "be": "bel_Cyrl",
    "bn": "ben_Beng",
    "bho": "bho_Deva",
    "bs": "bos_Latn",
    "bg": "bul_Cyrl",
    "ca": "cat_Latn",
    "ceb": "ceb_Latn",
    "cs": "ces_Latn",
    "ckb": "ckb_Arab",
    "tt": "crh_Latn",
    "cy": "cym_Latn",
    "da": "dan_Latn",
    "de": "deu_Latn",
    "el": "ell_Grek",
    "en": "eng_Latn",
    "eo": "epo_Latn",
    "et": "est_Latn",
    "eu": "eus_Latn",
    "ee": "ewe_Latn",
    "fa": "pes_Arab",
    "fi": "fin_Latn",
    "fr": "fra_Latn",
    "gd": "gla_Latn",
    "ga": "gle_Latn",
    "gl": "glg_Latn",
    "gn": "grn_Latn",
    "gu": "guj_Gujr",
    "ht": "hat_Latn",
    "ha": "hau_Latn",
    "he": "heb_Hebr",
    "hi": "hin_Deva",
    "hr": "hrv_Latn",
    "hu": "hun_Latn",
    "hy": "hye_Armn",
    "nl": "nld_Latn",
    "ig": "ibo_Latn",
    "ilo": "ilo_Latn",
    "id": "ind_Latn",
    "is": "isl_Latn",
    "it": "ita_Latn",
    "jv": "jav_Latn",
    "ja": "jpn_Jpan",
    "kn": "kan_Knda",
    "ka": "kat_Geor",
    "kk": "kaz_Cyrl",
    "km": "khm_Khmr",
    "rw": "kin_Latn",
    "ko": "kor_Hang",
    "ku": "kmr_Latn",
    "lo": "lao_Laoo",
    "lv": "lvs_Latn",
    "ln": "lin_Latn",
    "lt": "lit_Latn",
    "lb": "ltz_Latn",
    "lg": "lug_Latn",
    "lus": "lus_Latn",
    "mai": "mai_Deva",
    "ml": "mal_Mlym",
    "mr": "mar_Deva",
    "mk": "mkd_Cyrl",
    "mg": "plt_Latn",
    "mt": "mlt_Latn",
    "mni-Mtei": "mni_Beng",
    "mni": "mni_Beng",
    "mn": "khk_Cyrl",
    "mi": "mri_Latn",
    "ms": "zsm_Latn",
    "my": "mya_Mymr",
    "no": "nno_Latn",
    "ne": "npi_Deva",
    "ny": "nya_Latn",
    "om": "gaz_Latn",
    "or": "ory_Orya",
    "pl": "pol_Latn",
    "pt": "por_Latn",
    "ps": "pbt_Arab",
    "qu": "quy_Latn",
    "ro": "ron_Latn",
    "ru": "rus_Cyrl",
    "sa": "san_Deva",
    "si": "sin_Sinh",
    "sk": "slk_Latn",
    "sl": "slv_Latn",
    "sm": "smo_Latn",
    "sn": "sna_Latn",
    "sd": "snd_Arab",
    "so": "som_Latn",
    "es": "spa_Latn",
    "sq": "als_Latn",
    "sr": "srp_Cyrl",
    "su": "sun_Latn",
    "sv": "swe_Latn",
    "sw": "swh_Latn",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "tg": "tgk_Cyrl",
    "tl": "tgl_Latn",
    "th": "tha_Thai",
    "ti": "tir_Ethi",
    "ts": "tso_Latn",
    "tk": "tuk_Latn",
    "tr": "tur_Latn",
    "ug": "uig_Arab",
    "uk": "ukr_Cyrl",
    "ur": "urd_Arab",
    "uz": "uzn_Latn",
    "vi": "vie_Latn",
    "xh": "xho_Latn",
    "yi": "ydd_Hebr",
    "yo": "yor_Latn",
    "zh-CN": "zho_Hans",
    "zh": "zho_Hans",
    "zh-TW": "zho_Hant",
    "zu": "zul_Latn",
    "pa": "pan_Guru"
}

def get_nllb_lang(lang):
    try:
        nllb_lang = nllb_langs[lang]
    except:
        nllb_lang = "eng_Latn"
    return nllb_lang



HOST = "148.251.182.183"
PORT = "6060"
BASE = "/RTOKaprU81iaxv_vjay+i324" 

def api_translate_text(source: str, target:str, text: str) -> str:
    translated_text: str = ""
    if not text:
        warnings.warn("Cannot translate empty string!")
        return translated_text

    limit = 2000  # chars
    source_lang = get_nllb_lang(source)
    target_lang = get_nllb_lang(target)

    for sentence in nltk.sent_tokenize(text):
        attempts = 10
        api_status = 429
        nllb_call = 'http://' + HOST + ':' + PORT + BASE + '/translate?source=' + sentence[:limit] + '&src_lang=' + source_lang + '&tgt_lang='+ target_lang 
        while attempts > 0 and api_status != 200:
            try:
                nllb_response = requests.get(nllb_call, timeout=30)
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                print("Timeout")
                continue
            #print(nllb_response.status_code)
            api_status = nllb_response.status_code
            attempts -= 1
            if api_status == 200:
                translated_sentence = nllb_response.json()["translation"][0]
                if len(translated_text) > 0:
                    translated_text = translated_text + " " + translated_sentence
                else:
                    translated_text = translated_sentence
            elif api_status != 200:
                time.sleep(15)
                print('Slow down request and sleep for 15 seconds')
            else:
                print('Another error occurred')

    return translated_text

