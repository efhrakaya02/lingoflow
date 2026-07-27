from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="LingoFlow Story Academy - Kişisel Hikaye Stüdyosu",
    page_icon="📖",
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
if "quiz_active" not in st.session_state:
  st.session_state["quiz_active"] = False
if "quiz_question" not in st.session_state:
  st.session_state["quiz_question"] = ""


# --- AŞAMA 1: TANIŞMA VE DİL SEÇİMİ ---
if st.session_state["stage"] == "welcome":
  st.title("📖 LingoFlow Story Academy'ye Hoş Geldiniz!")
  st.markdown(
      "Dili kurallarla değil, **kendi hikayeniz ve hedefleriniz** etrafında"
      " şekillenen sürükleyici bir macera ile öğrenin."
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
  st.markdown(
      "Sana en uygun hikaye tabanlı çalışma planını oluşturabilmemiz için"
      " aşağıdaki 3 kısa soruyu yanıtla."
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
        "3. İletişim kurarken kendinizi nasıl hissediyorsunuz?",
        [
            "A) Çok çekiniyorum, sadece temel kelimeler biliyorum.",
            "B) Basit konularda konuşabiliyorum ama detaylarda zorlanıyorum.",
            "C) Oldukça rahatım, akıcı konuşabiliyorum.",
        ],
    )

    submitted = st.form_submit_button("Sınavı Tamamla ve Hedefini Belirle")
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

# --- AŞAMA 3: HİKAYE VE HEDEF BELİRLEME (STORY SETUP) ---
elif st.session_state["stage"] == "goal_setup":
  st.title(f"🌟 {st.session_state['user_name']}, Şimdi Hikayeni Yazalım!")
  st.markdown(
      f"Tespit Edilen Seviye: **{st.session_state['current_level']}** | Bu"
      " dili öğrenmekteki asıl amacın ne ve başardığında ne yapacaksın?"
  )

  with st.form("story_goal_form"):
    goal_choice = st.selectbox(
        "Bu dili öğrenme amacın nedir?",
        [
            "🌍 Seyahat etmek ve dünyayı keşfetmek",
            "💼 Kariyerimde yükselmek ve uluslararası projelerde yer almak",
            "🎬 Yabancı dizileri, filmleri ve kitapları orijinal dilinde anlamak",
            "✈️ Yurtdışına yerleşmek / Yaşam kurmak",
            "💡 Kişisel gelişim ve yeni bir hobi",
        ],
    )
    dream_input = st.text_area(
        "Hedefine ulaştığında ilk yapmak istediğin şey nedir?",
        placeholder=(
            "Örn: New York sokaklarında kimseye ihtiyaç duymadan kahve"
            " sipariş etmek veya uluslararası bir toplantıda sunum yapmak..."
        ),
    )

    goal_submitted = st.form_submit_button(
        "Kişiselleştirilmiş Hikaye Planımı Oluştur 🚀"
    )
    if goal_submitted:
      st.session_state["user_goal"] = goal_choice
      st.session_state["user_dream"] = (
          dream_input if dream_input.strip() else "Kendi hikayesini yazmak"
      )

      # Seviye ve hedefe göre dinamik modüller oluşturalım
      lvl = st.session_state["current_level"]
      if lvl == "A1":
        st.session_state["modules"] = [
            {
                "title": (
                    "Bölüm 1: Yolculuğun İlk Adımı (Tanışma ve Temel İletişim)"
                ),
                "status": "Açık",
                "words": 15,
                "skill": "Dinleme & Özgüven",
            },
            {
                "title": (
                    "Bölüm 2: Hikayenin Başlangıcı (Günlük Yaşam ve Rotalar)"
                ),
                "status": "Kilitli",
                "words": 20,
                "skill": "Yön ve İhtiyaçlar",
            },
            {
                "title": (
                    "Bölüm 3: İlk Büyük Başarı (Hedefe Doğru İlk Pratik Diyalog)"
                ),
                "status": "Kilitli",
                "words": 25,
                "skill": "Temel Akıcılık",
            },
        ]
      else:
        st.session_state["modules"] = [
            {
                "title": (
                    "Bölüm 1: Profesyonel Zirve ve Stratejik İletişim"
                ),
                "status": "Açık",
                "words": 20,
                "skill": "İleri Düzey Sentez",
            },
            {
                "title": "Bölüm 2: Derinlemesine Senaryolar ve Müzakere",
                "status": "Kilitli",
                "words": 25,
                "skill": "Akıcı Savunma",
            },
            {
                "title": "Bölüm 3: Hikayenin Zirvesi ve Küresel Yetkinlik",
                "status": "Kilitli",
                "words": 30,
                "skill": "Kusursuz İfade",
            },
        ]

      st.session_state["stage"] = "dashboard"
      st.rerun()

# --- AŞAMA 4: KİŞİSEL KURS PLANI & HİKAYE PANELI ---
elif st.session_state["stage"] == "dashboard":
  st.title(f"🗺️ {st.session_state['user_name']} - Hikaye Yolculuğun")
  st.success(
      f"🎯 **Hedef:** {st.session_state['user_goal']} | 🌟 **Hayalin:**"
      f" *{st.session_state['user_dream']}*"
  )

  st.markdown("### 📚 Hikaye Bölümleriniz")
  col_m1, col_m2, col_m3 = st.columns(3)

  for idx, mod in enumerate(st.session_state["modules"]):
    with [col_m1, col_m2, col_m3][idx % 3]:
      st.markdown(f"**{mod['title']}**")
      st.caption(f"Odak: {mod['skill']} | Kelime: {mod['words']} adet")

      if mod["status"] in ["Açık", "Tamamlandı"]:
        btn_label = (
            "Hikayeye Devam Et 🚀"
            if mod["status"] == "Açık"
            else "Bölümü Tekrar Et 🔄"
        )
        if st.button(btn_label, key=f"mod_{idx}"):
          st.session_state["current_module_idx"] = idx
          st.session_state["quiz_active"] = False
          st.session_state["stage"] = "learning"
          st.rerun()
      else:
        st.info("🔒 Kilitli")

  st.markdown("---")
  st.info(
      "💡 **Hikaye Notu:** Seviyenize uygun olarak bu bölümde anadil desteği"
      " optimize edilmiştir. Çekinmeden hedef dilde cümleler kurun!"
  )

# --- AŞAMA 5: ETKİLEŞİMLİ HİKAYE VE DERS (LEARNING STAGE) ---
elif st.session_state["stage"] == "learning":
  mod_idx = st.session_state["current_module_idx"]
  active_mod = st.session_state["modules"][mod_idx]

  st.title(f"📖 {active_mod['title']}")
  st.caption(
      f"Seviye: {st.session_state['current_level']} | Hedef Hikaye Amacı:"
      f" {st.session_state['user_goal']}"
  )

  # Seviyeye göre anadil (Türkçe) yardım oranını belirleyen talimat
  level_instruction = ""
  if st.session_state["current_level"] == "A1":
    level_instruction = (
        "Since the user is at A1 level, provide supportive explanations and"
        " tips in Turkish, while keeping the core sentences in the target"
        " language."
    )
  elif st.session_state["current_level"] == "A2":
    level_instruction = (
        "Since the user is at A2 level, use a balance of target language and"
        " light Turkish guidance for complex rules."
    )
  else:
    level_instruction = (
        "Since the user is at B1/B2 level, communicate almost entirely in the"
        " target language with minimal Turkish guidance."
    )

  if "lesson_chat" not in st.session_state:
    intro_prompt = (
        f"You are an inspiring story-driven language coach for"
        f" {st.session_state['target_lang']}. The user's ultimate dream is:"
        f" '{st.session_state['user_dream']}'. We are in module:"
        f" {active_mod['title']}. {level_instruction} Create a short, engaging"
        " story narrative that connects this lesson to their dream, teach 3"
        " practical words, and ask an encouraging question in the target"
        " language to get them speaking without fear."
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
          "Merhaba! Hikayemizin bu bölümünde hedefine bir adım daha"
          " yaklaşıyoruz. Hazırsan ilk pratik sorumuzla başlayalım!"
      )

    st.session_state["lesson_chat"] = [{
        "role": "assistant",
        "content": init_text,
    }]

  for msg in st.session_state["lesson_chat"]:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # Sohbet Giriş Barı
  if user_reply := st.chat_input("Hikayeye katkıda bulun, cümle kur..."):
    st.session_state["lesson_chat"].append(
        {"role": "user", "content": user_reply}
    )
    with st.chat_message("user"):
      st.markdown(user_reply)

    tutor_prompt = (
        f"You are an encouraging story coach for"
        f" {st.session_state['target_lang']}. {level_instruction} Evaluate the"
        f" user input: '{user_reply}'. Correct mistakes gently, connect the"
        " response back to their dream ('{st.session_state['user_dream']}'),"
        " praise their effort, and ask a follow-up question."
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

  # --- BÖLÜM KONTROL VE TEKRAR TESTİ (SOHBETİN ALTINDA) ---
  st.markdown("---")
  st.markdown("### 🎯 Bölüm Kontrol ve Hikaye Tekrar Testi")

  if not st.session_state["quiz_active"]:
    if st.button("📝 Bölüm Sonu Tekrar Testini Başlat", type="secondary"):
      q_prompt = (
          f"Create 1 short multiple-choice story-based review question in"
          f" {st.session_state['target_lang']} for level"
          f" {st.session_state['current_level']} connecting to"
          f" '{st.session_state['user_goal']}'. Give 4 options (A, B, C, D) and"
          " state the correct answer clearly at the end as 'Doğru Cevap: X'."
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

    if st.button("✅ Testi Kontrol Et ve Bölümü Tamamla", type="primary"):
      if user_quiz_ans.strip():
        if active_mod["status"] != "Tamamlandı":
          st.session_state["total_words"] += active_mod["words"]
          st.session_state["achievements"].append(active_mod["title"])
          st.session_state["modules"][mod_idx]["status"] = "Tamamlandı"

        st.session_state["quiz_active"] = False

        if mod_idx + 1 < len(st.session_state["modules"]):
          if st.session_state["modules"][mod_idx + 1]["status"] == "Kilitli":
            st.session_state["modules"][mod_idx + 1]["status"] = "Açık"
          del st.session_state["lesson_chat"]
          st.session_state["stage"] = "dashboard"
          st.success(
              "Tebrikler! Hikayenin bu bölümünü başarıyla tamamladın ve sonraki"
              " bölüme açıldı."
          )
          st.rerun()
        else:
          del st.session_state["lesson_chat"]
          st.session_state["stage"] = "certificate"
          st.rerun()
      else:
        st.warning("Lütfen bir cevap yazın.")

  if st.button("🔙 Hikaye Paneline Geri Dön"):
    st.session_state["quiz_active"] = False
    if "lesson_chat" in st.session_state:
      del st.session_state["lesson_chat"]
    st.session_state["stage"] = "dashboard"
    st.rerun()

# --- AŞAMA 6: SERTİFİKA VE GELİŞİM TABLOSU ---
elif st.session_state["stage"] == "certificate":
  st.title("🏆 Harika Bir Hikayeyi Zirvede Tamamladın!")
  st.balloons()

  st.markdown(
      f"""
    <div style="border: 4px solid #4CAF50; padding: 30px; border-radius: 15px; text-align: center; background-color: #f9f9f9;">
        <h2>🎓 HİKAYE BAŞARI VE YETERLİLİK SERTİFİKASI 🎓</h2>
        <p>Bu sertifika,</p>
        <h3><b>{st.session_state['user_name']}</b></h3>
        <p>adlı öğrencimizin <b>{st.session_state['target_lang']}</b> dilinde başarıyla tamamladığı</p>
        <h4><b>{st.session_state['current_level']} Seviyesi Hikaye Programını</b></h4>
        <p>başarıyla bitirdiğini, <i>"{st.session_state['user_dream']}"</i> hayaline bir adım daha yaklaştığını belgelemektedir.</p>
        <hr style="width: 50%; margin: 20px auto;">
        <p><b>Temel Hedef:</b> {st.session_state['user_goal']}</p>
        <p><b>Toplam Öğrenilen Kelime:</b> {st.session_state['total_words']} adet</p>
        <p><b>Tamamlanan Bölümler:</b> {', '.join(st.session_state['achievements'])}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("🌟 Yeni Seviye ve Yeni Hikayeye Geçiş Yap", type="primary"):
    if st.session_state["current_level"] == "A1":
      st.session_state["current_level"] = "A2"
    elif st.session_state["current_level"] == "A2":
      st.session_state["current_level"] = "B1"
    else:
      st.session_state["current_level"] = "B2/C1"

    st.session_state["modules"] = [
        {
            "title": f"Bölüm 1: {st.session_state['current_level']} Hikaye Genişlemesi",
            "status": "Açık",
            "words": 30,
            "skill": "İleri Akıcılık",
        },
        {
            "title": f"Bölüm 2: {st.session_state['current_level']} Karmaşık Senaryolar",
            "status": "Kilitli",
            "words": 35,
            "skill": "Doğal Konuşma",
        },
    ]
    st.session_state["stage"] = "dashboard"
    st.rerun()
