from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="LingoFlow Story Academy - İnteraktif Dil Stüdyosu",
    page_icon="🎯",
    layout="wide",
)

# API Anahtarı Yönetimi
api_key = st.secrets.get("GROQ_API_KEY") or st.sidebar.text_input(
    "Groq API Key", type="password"
)

if not api_key:
    st.warning("Lütfen devam etmek için geçerli bir Groq API Anahtarı girin.")
    st.stop()

client = Groq(api_key=api_key)

# --- OTURUM DURUMU (STATE) BAŞLANGIÇLARI ---
if "stage" not in st.session_state:
  st.session_state["stage"] = "welcome"
if "user_name" not in st.session_state:
  st.session_state["user_name"] = ""
if "target_lang" not in st.session_state:
  st.session_state["target_lang"] = "İngilizce (English)"
if "current_level" not in st.session_state:
  st.session_state["current_level"] = "A1"
if "user_goal" not in st.session_state:
  st.session_state["user_goal"] = ""
if "user_dream" not in st.session_state:
  st.session_state["user_dream"] = ""
if "modules" not in st.session_state:
  st.session_state["modules"] = []
if "current_module_idx" not in st.session_state:
  st.session_state["current_module_idx"] = 0
if "total_words" not in st.session_state:
  st.session_state["total_words"] = 0
if "achievements" not in st.session_state:
  st.session_state["achievements"] = []
if "exercise_step" not in st.session_state:
  st.session_state["exercise_step"] = 1  # 1: Giriş, 2: Boşluk Doldurma, 3: Çoktan Seçmeli, 4: Yazma & Telaffuz
if "exercise_data" not in st.session_state:
  st.session_state["exercise_data"] = {}


# --- AŞAMA 1: TANIŞMA VE DİL SEÇİMİ ---
if st.session_state["stage"] == "welcome":
  st.title("🎯 LingoFlow İnteraktif Hikaye Akademisi")
  st.markdown(
      "Önce seni motive edip havaya sokacağız, ardından seçenekler, ipuçları ve"
      " eğlenceli egzersizlerle dil becerilerini adım adım zirveye taşıyacağız!"
  )

  col1, col2 = st.columns(2)
  with col1:
    name_input = st.text_input("Size nasıl hitap edelim?", placeholder="Adınız")
  with col2:
    lang_input = st.selectbox(
        "Hangi dili öğrenmek istiyorsun?",
        ["İngilizce (English)", "Almanca (Deutsch)", "İspanyolca (Español)"],
    )

  if st.button("🚀 Yolculuğa Başla", type="primary"):
    if name_input.strip():
      st.session_state["user_name"] = name_input
      st.session_state["target_lang"] = lang_input
      st.session_state["stage"] = "placement"
      st.rerun()
    else:
      st.error("Lütfen devam etmek için adınızı girin.")

# --- AŞAMA 2: SEVİYE TESPİT SINAVI ---
elif st.session_state["stage"] == "placement":
  st.title(
      f"🎯 {st.session_state['user_name']}, Seviye Tespit Sınavına Hoş Geldin!"
  )
  st.markdown("Sana en uygun interaktif planı hazırlamak için 3 kısa soru:")

  with st.form("placement_form"):
    q1 = st.radio(
        "1. Kendini nasıl tanıtabilirsin?",
        [
            "A) I am student / My name is...",
            "B) I have been working here for 5 years...",
            "C) Fluently discussing abstract concepts...",
        ],
    )
    q2 = st.radio(
        "2. Geçmiş zamanda bir olay anlatırken hangisini tercih edersin?",
        [
            "A) Yesterday I go to market",
            "B) Yesterday I went to the market and bought...",
            "C) Had I known earlier, I would have...",
        ],
    )
    q3 = st.radio(
        "3. İletişim kurarken kendinizi nasıl hissediyorsunuz?",
        [
            "A) Çok çekiniyorum, sadece temel kelimeler biliyorum.",
            "B) Basit konularda konuşabiliyorum ama detaylarda zorlanıyorum.",
            "C) Oldukça rahatım, akıcı konuşabiliyorum.",
        ],
    )

    submitted = st.form_submit_button("Sınavı Tamamla ve Hedefini Seç")
    if submitted:
      if "A)" in q1 and "A)" in q2:
        detected_level = "A1"
      elif "B)" in q1 or "B)" in q2:
        detected_level = "B1"
      else:
        detected_level = "B2"

      st.session_state["current_level"] = detected_level
      st.session_state["stage"] = "goal_setup"
      st.rerun()

# --- AŞAMA 3: HİKAYE VE HEDEF BELİRLEME ---
elif st.session_state["stage"] == "goal_setup":
  st.title(f"🌟 {st.session_state['user_name']}, Hayalini Şekillendirelim!")
  st.markdown(
      f"Tespit Edilen Seviye: **{st.session_state['current_level']}** | Bu"
      " dili hangi amaçla öğrenmek istiyorsun?"
  )

  with st.form("story_goal_form"):
    goal_choice = st.selectbox(
        "Temel Hedefin Nedir?",
        [
            "🌍 Seyahat etmek ve dünyayı keşfetmek",
            "💼 Kariyerimde yükselmek ve uluslararası projeler yapmak",
            "🎬 Yabancı filmleri ve kitapları orijinal dilinde anlamak",
            "✈️ Yurtdışına yerleşmek / Yaşam kurmak",
        ],
    )
    dream_input = st.text_area(
        "Hedefine ulaştığında ilk yapmak istediğin şey nedir?",
        placeholder="Örn: New York sokaklarında kahve sipariş etmek...",
    )

    goal_submitted = st.form_submit_button(
        "Motivasyon Odaklı Planımı Başlat 🚀"
    )
    if goal_submitted:
      st.session_state["user_goal"] = goal_choice
      st.session_state["user_dream"] = (
          dream_input if dream_input.strip() else "Kendi hikayesini yazmak"
      )

      lvl = st.session_state["current_level"]
      if lvl == "A1":
        st.session_state["modules"] = [
            {
                "title": (
                    "Bölüm 1: Sahne Senin (Tanışma & Temel İfade Güveni)"
                ),
                "status": "Açık",
                "words": 15,
                "skill": "Dinleme & Özgüven",
            },
            {
                "title": (
                    "Bölüm 2: Günlük Macera (Rotalar & Pratik İhtiyaçlar)"
                ),
                "status": "Kilitli",
                "words": 20,
                "skill": "Boşluk Doldurma & Kelime",
            },
            {
                "title": "Bölüm 3: İlk Büyük Başarı (Diyalog & Telaffuz)",
                "status": "Kilitli",
                "words": 25,
                "skill": "Konuşma Pratiği",
            },
        ]
      else:
        st.session_state["modules"] = [
            {
                "title": "Bölüm 1: Profesyonel Zirve ve Stratejik İletişim",
                "status": "Açık",
                "words": 20,
                "skill": "İleri Sentez",
            },
            {
                "title": "Bölüm 2: Müzakere ve Karmaşık Senaryolar",
                "status": "Kilitli",
                "words": 25,
                "skill": "Akıcı Savunma",
            },
            {
                "title": "Bölüm 3: Küresel Yetkinlik ve Zirve",
                "status": "Kilitli",
                "words": 30,
                "skill": "Kusursuz İfade",
            },
        ]

      st.session_state["stage"] = "dashboard"
      st.rerun()

# --- AŞAMA 4: KİŞİSEL KURS PLANI & HİKAYE PANELI ---
elif st.session_state["stage"] == "dashboard":
  st.title(f"🗺️ {st.session_state['user_name']} - Akademik Yolculuğun")
  st.success(
      f"🎯 **Hedef:** {st.session_state['user_goal']} | 🌟 **Hayalin:**"
      f" *{st.session_state['user_dream']}*"
  )

  st.markdown("### 📚 Eğitim Modülleriniz")
  col_m1, col_m2, col_m3 = st.columns(3)

  for idx, mod in enumerate(st.session_state["modules"]):
    with [col_m1, col_m2, col_m3][idx % 3]:
      st.markdown(f"**{mod['title']}**")
      st.caption(f"Odak: {mod['skill']} | Kelime: {mod['words']} adet")

      if mod["status"] in ["Açık", "Tamamlandı"]:
        btn_label = (
            "Dese Başla 🚀"
            if mod["status"] == "Açık"
            else "Modülü Tekrar Et 🔄"
        )
        if st.button(btn_label, key=f"mod_{idx}"):
          st.session_state["current_module_idx"] = idx
          st.session_state["exercise_step"] = 1
          st.session_state["stage"] = "learning"
          st.rerun()
      else:
        st.info("🔒 Kilitli")

# --- AŞAMA 5: İNTERAKTİF İSTASYONLU DERS (LEARNING STAGE) ---
elif st.session_state["stage"] == "learning":
  mod_idx = st.session_state["current_module_idx"]
  active_mod = st.session_state["modules"][mod_idx]

  st.title(f"📖 {active_mod['title']}")
  st.caption(
      f"Seviye: {st.session_state['current_level']} | Hayalin:"
      f" {st.session_state['user_dream']}"
  )

  # Adım kontrolü için sekmeler veya görsel ilerleme çubuğu
  step = st.session_state["exercise_step"]

  st.progress(
      step / 3,
      text=f"Egzersiz Adımı: {step} / 3 (Motivasyon -> Test/Boşluk -> Yazma"
      " & Telaffuz)",
  )

  # --- ADIM 1: MOTİVASYON VE HİKAYE GİRİŞİ ---
  if step == 1:
    st.subheader("🔥 1. Aşama: Motivasyon ve Hikaye Başlangıcı")
    st.markdown(
        f"Harika bir yolculuktasın! Amacımız: *{st.session_state['user_goal']}*."
        f" Bugün bu modülde, '{st.session_state['user_dream']}' hedefine bir"
        " adım daha yaklaşmak için kelime dağarcığımızı ısıtıyoruz."
    )

    # Kısa bir motivasyon metni üretelim
    if "intro_text" not in st.session_state:
      prompt_intro = (
          f"You are an inspiring language coach. The user wants to achieve:"
          f" '{st.session_state['user_goal']}' and their dream is:"
          f" '{st.session_state['user_dream']}'. Write a short, powerful,"
          f" highly motivating welcome message in Turkish mixed with"
          f" {st.session_state['target_lang']} to get them in the mood to learn"
          " without fear."
      )
      try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_intro}],
            temperature=0.7,
        )
        st.session_state["intro_text"] = res.choices[0].message.content
      except Exception:
        st.session_state["intro_text"] = (
            "Hazırsan zihnini aç ve kelimelerin gücünü hisset! Başlıyoruz."
        )

    st.info(st.session_state["intro_text"])

    if st.button(
        "İpucu ve Boşluk Doldurma Egzersizine Geç ➡️", type="primary"
    ):
      st.session_state["exercise_step"] = 2
      st.rerun()

  # --- ADIM 2: BOŞLUK DOLDURMA VE SEÇENEKLİ SORULAR ---
  elif step == 2:
    st.subheader("🧩 2. Aşama: Boşluk Doldurma ve Çoktan Seçmeli Pratik")
    st.markdown(
        "Aşağıdaki alıştırmada ipuçlarını kullanarak doğru seçeneği bulmaya"
        " çalış."
    )

    if "quiz_generated" not in st.session_state:
      q_prompt = (
          f"Create 1 fill-in-the-blank or multiple-choice exercise in"
          f" {st.session_state['target_lang']} for level"
          f" {st.session_state['current_level']} related to"
          f" {active_mod['title']}. Include a helpful hint in Turkish, 4"
          f" options (A, B, C, D), and state the correct answer clearly at the"
          f" end as 'Dogru Cevap: X'."
      )
      try:
        q_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": q_prompt}],
            temperature=0.7,
        )
        st.session_state["quiz_generated"] = q_res.choices[0].message.content
      except Exception:
        st.session_state["quiz_generated"] = (
            "Soru yüklenemedi. Lütfen tekrar deneyin."
        )

    st.markdown(st.session_state["quiz_generated"])

    user_ans = st.radio(
        "Seçiminizi yapın:", ["Seçiniz...", "A", "B", "C", "D"], key="q_choice"
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      if st.button("Cevabı Kontrol Et ve İlerle 🚀", type="primary"):
        if user_ans != "Seçiniz...":
          st.success(
              "Harika analiz! Cevabınız kaydedildi. Şimdi son aşamaya"
              " geçiyoruz."
          )
          st.session_state["exercise_step"] = 3
          if "quiz_generated" in st.session_state:
            del st.session_state["quiz_generated"]
          st.rerun()
        else:
          st.warning("Lütfen bir seçenek işaretleyin.")
    with col_btn2:
      if st.button("💡 İpucu İste"):
        st.info(
            "İpucu: Cümlenin zamanına (tense) ve kelimenin cümledeki konumuna"
            " dikkat et! Fiilin doğru formunu arıyoruz."
        )

  # --- ADIM 3: YAZMA, DİNLEME VE TELAFUZ GELİŞTİRME ---
  elif step == 3:
    st.subheader("🗣️ 3. Aşama: Yazma, Dinleme ve Telaffuz Çalışması")
    st.markdown(
        "Şimdi öğrendiklerini kendi cümlelerinle ifade etme zamanı! Hiç"
        " çekinmeden yaz, telaffuz ve kulak dolgunluğu ipuçlarını incele."
    )

    writing_input = st.text_area(
        "Bu modüldeki anahtar kelimeleri kullanarak kendi cümleni yaz:",
        placeholder="Örn: I want to practice every day to achieve my dream...",
    )

    if st.button("Cümlemi Kontrol Et ve Modülü Tamamla 🏆", type="primary"):
      if writing_input.strip():
        # İstatistikleri güncelle
        if active_mod["status"] != "Tamamlandı":
          st.session_state["total_words"] += active_mod["words"]
          st.session_state["achievements"].append(active_mod["title"])
          st.session_state["modules"][mod_idx]["status"] = "Tamamlandı"

        st.balloons()
        st.success(
            "Mükemmel çaba! Cümlendeki ifadeler çok başarılı. Telaffuz için"
            " kelimeleri sesli okumayı unutma."
        )

        if mod_idx + 1 < len(st.session_state["modules"]):
          if st.session_state["modules"][mod_idx + 1]["status"] == "Kilitli":
            st.session_state["modules"][mod_idx + 1]["status"] = "Açık"
          st.session_state["stage"] = "dashboard"
          if "intro_text" in st.session_state:
            del st.session_state["intro_text"]
          st.rerun()
        else:
          st.stage = "certificate"
          st.rerun()
      else:
        st.warning(
            "Lütfen küçük de olsa bir cümle yazarak pratik yapmayı dene."
        )

  st.markdown("---")
  if st.button("🔙 Panele Geri Dön"):
    if "intro_text" in st.session_state:
      del st.session_state["intro_text"]
    if "quiz_generated" in st.session_state:
      del st.session_state["quiz_generated"]
    st.session_state["stage"] = "dashboard"
    st.rerun()
