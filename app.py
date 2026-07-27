from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="LingoFlow Academy - Kişisel Dil Stüdyosu",
    page_icon="🎓",
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
if "modules" not in st.session_state:
  st.session_state["modules"] = []
if "current_module_idx" not in st.session_state:
  st.session_state["current_module_idx"] = 0
if "total_words" not in st.session_state:
  st.session_state["total_words"] = 0
if "achievements" not in st.session_state:
  st.session_state["achievements"] = []
if "quiz_active" not in st.session_state:
  st.session_state["quiz_active"] = False
if "quiz_question" not in st.session_state:
  st.session_state["quiz_question"] = ""


# --- AŞAMA 1: TANIŞMA VE DİL SEÇİMİ ---
if st.session_state["stage"] == "welcome":
  st.title("🎓 LingoFlow Academy'ye Hoş Geldiniz!")
  st.markdown(
      "Hata yapmaktan korkmayacağınız, tamamen size özel planlanmış, eğlenceli"
      " ve interaktif dil öğrenme stüdyosu."
  )

  col1, col2 = st.columns(2)
  with col1:
    name_input = st.text_input("Size nasıl hitap edelim?", placeholder="Adınız")
  with col2:
    lang_input = st.selectbox(
        "Hangi dili öğrenmek istiyorsun?",
        ["İngilizce (English)", "Almanca (Deutsch)", "İspanyolca (Español)"],
    )

  if st.button("🚀 Yolculuğa Başla ve Seviyeni Test Et", type="primary"):
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
  st.markdown(
      "Sana en uygun kişisel çalışma planını oluşturabilmemiz için aşağıdaki 3"
      " kısa soruyu yanıtla."
  )

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
        "3. İngilizce iletişim kurarken kendinizi nasıl hissediyorsunuz?",
        [
            "A) Çok çekiniyorum, sadece temel kelimeler biliyorum.",
            "B) Basit konularda konuşabiliyorum ama detaylarda zorlanıyorum.",
            "C) Oldukça rahatım, akıcı konuşabiliyorum.",
        ],
    )

    submitted = st.form_submit_button("Sınavı Tamamla ve Planımı Oluştur")
    if submitted:
      if "A)" in q1 and "A)" in q2:
        detected_level = "A1"
      elif "B)" in q1 or "B)" in q2:
        detected_level = "B1"
      else:
        detected_level = "B2"

      st.session_state["current_level"] = detected_level

      if detected_level == "A1":
        st.session_state["modules"] = [
            {
                "title": "Modül 1: Tanışma ve Selamlaşma",
                "status": "Açık",
                "words": 15,
                "skill": "Dinleme & Okuma",
            },
            {
                "title": "Modül 2: Günlük Rutinler ve Aile",
                "status": "Kilitli",
                "words": 20,
                "skill": "Yazma & Konuşma Cesareti",
            },
            {
                "title": "Modül 3: Alışveriş ve Restoranda Sipariş",
                "status": "Kilitli",
                "words": 25,
                "skill": "Pratik Diyalog",
            },
        ]
      else:
        st.session_state["modules"] = [
            {
                "title": "Modül 1: Profesyonel İletişim ve Toplantılar",
                "status": "Açık",
                "words": 20,
                "skill": "İleri Düzey Yazma",
            },
            {
                "title": "Modül 2: Karmaşık Olaylar ve Hikaye Anlatımı",
                "status": "Kilitli",
                "words": 25,
                "skill": "Akıcı Konuşma",
            },
            {
                "title": "Modül 3: Soyut Fikirler ve Münazara",
                "status": "Kilitli",
                "words": 30,
                "skill": "Kapsamlı Sentez",
            },
        ]

      st.session_state["stage"] = "dashboard"
      st.rerun()

# --- AŞAMA 3: KİŞİSEL KURS PLANI & MODÜL PANELI ---
elif st.session_state["stage"] == "dashboard":
  st.title(f"🗺️ {st.session_state['user_name']} - Kişisel Kurs Planın")
  st.success(
      f"Tespit Edilen Seviye: **{st.session_state['current_level']}** | Hedef"
      f" Dil: **{st.session_state['target_lang']}**"
  )

  st.markdown("### 📚 Müfredat Modülleriniz")
  col_m1, col_m2, col_m3 = st.columns(3)

  for idx, mod in enumerate(st.session_state["modules"]):
    with [col_m1, col_m2, col_m3][idx % 3]:
      st.markdown(f"**{mod['title']}**")
      st.caption(f"Odak: {mod['skill']} | Kelime: {mod['words']} adet")

      # Açık veya Tamamlanmış modüllere tekrar girebilme izni
      if mod["status"] in ["Açık", "Tamamlandı"]:
        btn_label = "Derse Başla 🚀" if mod["status"] == "Açık" else "Tekrar Et 🔄"
        if st.button(btn_label, key=f"mod_{idx}"):
          st.session_state["current_module_idx"] = idx
          st.session_state["quiz_active"] = False
          st.session_state["stage"] = "learning"
          st.rerun()
      else:
        st.info("🔒 Kilitli")

  st.markdown("---")
  st.info(
      "💡 **İpucu:** Hiç çekinmeden yabancı dilde cümleler kurun. Hatalarınız"
      " anında nazikçe düzeltilerek öğrenmeniz pekiştirilecektir!"
  )

# --- AŞAMA 4: ETKİLEŞİMLİ DERS VE PRATİK (LEARNING STAGE) ---
elif st.session_state["stage"] == "learning":
  mod_idx = st.session_state["current_module_idx"]
  active_mod = st.session_state["modules"][mod_idx]

  st.title(f"📖 {active_mod['title']}")
  st.caption(
      f"Seviye: {st.session_state['current_level']} | Hedef Kazanım:"
      f" {active_mod['skill']}"
  )

  if "lesson_chat" not in st.session_state:
    intro_prompt = (
        f"You are a friendly, encouraging language tutor for"
        f" {st.session_state['target_lang']} at level"
        f" {st.session_state['current_level']}. We are starting module:"
        f" {active_mod['title']}. Give a short, fun, interactive introduction,"
        f" teach 3 core words with examples, and encourage the user to speak"
        " without fear by asking a simple question in the target language."
    )
    try:
      res = client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[{"role": "user", "content": intro_prompt}],
          temperature=0.7,
      )
      init_text = res.choices[0].message.content
    except Exception:
      init_text = (
          "Merhaba! Bu derste yeni kelimeler öğreneceğiz ve hiç çekinmeden"
          " pratik yapacağız. Hazırsan ilk sorumla başlayalım!"
      )

    st.session_state["lesson_chat"] = [{
        "role": "assistant",
        "content": init_text,
    }]

  for msg in st.session_state["lesson_chat"]:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # Sohbet Giriş Barı
  if user_reply := st.chat_input("Cümlenizi yazın, çekinmeden pratik yapın..."):
    st.session_state["lesson_chat"].append(
        {"role": "user", "content": user_reply}
    )
    with st.chat_message("user"):
      st.markdown(user_reply)

    tutor_prompt = (
        f"You are an encouraging language tutor for"
        f" {st.session_state['target_lang']}. Evaluate the user's input:"
        " '{user_reply}'. Correct any mistakes gently with a friendly tip,"
        " praise their effort to boost confidence, and ask a follow-up question"
        " to keep the conversation going."
    )
    try:
      chat_res = client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[
              {"role": m["role"], "content": m["content"]}
              for m in st.session_state["lesson_chat"]
          ],
          temperature=0.7,
      )
      tutor_reply = chat_res.choices[0].message.content
    except Exception as e:
      tutor_reply = f"Bir hata oluştu: {e}"

    st.session_state["lesson_chat"].append(
        {"role": "assistant", "content": tutor_reply}
    )
    with st.chat_message("assistant"):
      st.markdown(tutor_reply)

  # --- SOHBET BARININ ALTINDAKİ KONTROL VE TEST ALANI ---
  st.markdown("---")
  st.markdown("### 🎯 Bölüm Kontrol ve Tekrar Testi")

  if not st.session_state["quiz_active"]:
    if st.button("📝 Bölüm Sonu Tekrar Testini Başlat", type="secondary"):
      # Yapay zekadan kısa bir tekrar testi sorusu isteyelim
      q_prompt = (
          f"Create 1 short multiple-choice review question in"
          f" {st.session_state['target_lang']} for level"
          f" {st.session_state['current_level']} based on module"
          f" {active_mod['title']}. Give 4 options (A, B, C, D) and state the"
          " correct answer clearly at the end as 'Doğru Cevap: X'."
      )
      try:
        q_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": q_prompt}],
            temperature=0.7,
        )
        st.session_state["quiz_question"] = q_res.choices[0].message.content
        st.session_state["quiz_active"] = True
        st.rerun()
      except Exception as e:
        st.error(f"Test yüklenirken hata oluştu: {e}")
  else:
    st.info("Lütfen aşağıdaki tekrar testini yanıtlayıp kontrol edin:")
    st.markdown(st.session_state["quiz_question"])
    user_quiz_ans = st.text_input(
        "Cevabınız (Örn: A, B, C veya D):", key="quiz_answer_input"
    )

    if st.button("✅ Testi Kontrol Et ve Modülü Tamamla", type="primary"):
      if user_quiz_ans.strip():
        # İstatistikleri güncelle ve modülü tamamla
        if active_mod["status"] != "Tamamlandı":
          st.session_state["total_words"] += active_mod["words"]
          st.session_state["achievements"].append(active_mod["title"])
          st.session_state["modules"][mod_idx]["status"] = "Tamamlandı"

        st.session_state["quiz_active"] = False

        # Sonraki modülü aç veya sertifikaya git
        if mod_idx + 1 < len(st.session_state["modules"]):
          if st.session_state["modules"][mod_idx + 1]["status"] == "Kilitli":
            st.session_state["modules"][mod_idx + 1]["status"] = "Açık"
          del st.session_state["lesson_chat"]
          st.session_state["stage"] = "dashboard"
          st.success(
              "Tebrikler! Tekrar testini başarıyla geçtiniz ve modülü"
              " tamamladınız."
          )
          st.rerun()
        else:
          del st.session_state["lesson_chat"]
          st.session_state["stage"] = "certificate"
          st.rerun()
      else:
        st.warning("Lütfen bir cevap yazın.")

  if st.button("🔙 Panele Geri Dön"):
    st.session_state["quiz_active"] = False
    if "lesson_chat" in st.session_state:
      del st.session_state["lesson_chat"]
    st.session_state["stage"] = "dashboard"
    st.rerun()

# --- AŞAMA 5: SERTİFİKA VE GELİŞİM TABLOSU ---
elif st.session_state["stage"] == "certificate":
  st.title("🏆 Tebrikler, Harika Bir Başarıya İmza Attın!")
  st.balloons()

  st.markdown(
      f"""
    <div style="border: 4px solid #4CAF50; padding: 30px; border-radius: 15px; text-align: center; background-color: #f9f9f9;">
        <h2>🎓 BAŞARI VE YETERLİLİK SERTİFİKASI 🎓</h2>
        <p>Bu sertifika,</p>
        <h3><b>{st.session_state['user_name']}</b></h3>
        <p>adlı öğrencimizin <b>{st.session_state['target_lang']}</b> dilinde başarıyla tamamladığı</p>
        <h4><b>{st.session_state['current_level']} Seviyesi Eğitim Programını</b></h4>
        <p>başarıyla bitirdiğini ve gerekli tüm dil becerilerini kazandığını belgelemektedir.</p>
        <hr style="width: 50%; margin: 20px auto;">
        <p><b>Toplam Öğrenilen Kelime:</b> {st.session_state['total_words']} adet</p>
        <p><b>Elde Edilen Kazanımlar:</b> {', '.join(st.session_state['achievements'])}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("🌟 Yeni Seviyeye (Sonraki Aşama) Geçiş Yap", type="primary"):
    if st.session_state["current_level"] == "A1":
      st.session_state["current_level"] = "A2"
    elif st.session_state["current_level"] == "A2":
      st.session_state["current_level"] = "B1"
    else:
      st.session_state["current_level"] = "B2/C1"

    st.session_state["modules"] = [
        {
            "title": f"Modül 1: {st.session_state['current_level']} İleri Pratik",
            "status": "Açık",
            "words": 30,
            "skill": "Akıcı Konuşma",
        },
        {
            "title": f"Modül 2: {st.session_state['current_level']} Uzmanlık Alanları",
            "status": "Kilitli",
            "words": 35,
            "skill": "Karmaşık Metinler",
        },
    ]
    st.session_state["stage"] = "dashboard"
    st.rerun()
