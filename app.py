from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="LingoFlow Pro - Kapsamlı Dil Akademisi",
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
if "user_goal" not in st.session_state:
  st.session_state["user_goal"] = ""
if "user_dream" not in st.session_state:
  st.session_state["user_dream"] = ""
if "modules" not in st.session_state:
  st.session_state["modules"] = []
if "current_module_idx" not in st.session_state:
  st.session_state["current_module_idx"] = 0
if "lesson_step" not in st.session_state:
  st.session_state["lesson_step"] = 1  # 1: Okuma/Hikaye, 2: Kelime&Kalıp, 3: Test, 4: Yazma
if "total_words" not in st.session_state:
  st.session_state["total_words"] = 0
if "achievements" not in st.session_state:
  st.session_state["achievements"] = []
if "current_report" not in st.session_state:
  st.session_state["current_report"] = {}


# --- AŞAMA 1: TANIŞMA VE DİL SEÇİMİ ---
if st.session_state["stage"] == "welcome":
  st.title("🎓 LingoFlow Pro - Profesyonel Dil Akademisi")
  st.markdown(
      "Yüzeysel değil; **her biri 5-10 dakika süren yoğun, kişiselleştirilmiş ve"
      " karneli** gerçek bir eğitim planıyla dil öğrenin."
  )

  col1, col2 = st.columns(2)
  with col1:
    name_input = st.text_input("Size nasıl hitap edelim?", placeholder="Adınız")
  with col2:
    lang_input = st.selectbox(
        "Hangi dili öğrenmek istiyorsun?",
        ["İngilizce (English)", "Almanca (Deutsch)", "İspanyolca (Español)"],
    )

  if st.button("🚀 Akademik Yolculuğa Başla", type="primary"):
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
  st.markdown("Size en uygun yoğun eğitim müfredatını oluşturmak için:")

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

    submitted = st.form_submit_button("Seviyemi Belirle ve Devam Et")
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
  st.title(f"🌟 {st.session_state['user_name']}, Hedefini ve Hayalini Tanımla")
  st.markdown(
      f"Tespit Edilen Seviye: **{st.session_state['current_level']}** | Bu"
      " eğitimi ne için alıyorsun?"
  )

  with st.form("story_goal_form"):
    goal_choice = st.selectbox(
        "Temel Amacınız Nedir?",
        [
            "🌍 Seyahat etmek ve dünyayı özgürce keşfetmek",
            "💼 Kariyerimde yükselmek, sunum ve müzakereler yapmak",
            "🎬 Yabancı medya, teknik makaleler ve kitapları orijinal okumak",
            "✈️ Yurtdışına yerleşmek ve sosyal hayat kurmak",
        ],
    )
    dream_input = st.text_area(
        "Hedefine ulaştığında ilk gerçekleştireceğin büyük şey nedir?",
        placeholder=(
            "Örn: Uluslararası bir toplantıda akıcı bir şekilde projemi"
            " savunmak..."
        ),
    )

    goal_submitted = st.form_submit_button("Kapsamlı Eğitim Planımı Oluştur 🚀")
    if goal_submitted:
      st.session_state["user_goal"] = goal_choice
      st.session_state["user_dream"] = (
          dream_input if dream_input.strip() else "Kendi başarı hikayesini yazmak"
      )

      # 4 Kapsamlı ve Detaylı Modül
      st.session_state["modules"] = [
          {
              "title": (
                  "Modül 1: Temeller ve Özgüven İnşası (Foundation & First"
                  " Contact)"
              ),
              "status": "Açık",
              "duration": "10 dk",
              "words": 20,
              "skill": "Okuma & Temel Yapılar",
          },
          {
              "title": (
                  "Modül 2: Günlük Senaryolar ve Akış Yönetimi (Core Context)"
              ),
              "status": "Kilitli",
              "duration": "10 dk",
              "words": 25,
              "skill": "Kelime & Cübbe Kalıpları",
          },
          {
              "title": (
                  "Modül 3: Stratejik İletişim ve Problem Çözme (Advanced"
                  " Dialogue)"
              ),
              "status": "Kilitli",
              "duration": "12 dk",
              "words": 30,
              "skill": "İleri Anlama & Pratik",
          },
          {
              "title": "Modül 4: Hedef Zirvesi ve Küresel Yetkinlik (Mastery)",
              "status": "Kilitli",
              "duration": "15 dk",
              "words": 35,
              "skill": "Özgür İfade & Sentez",
          },
      ]

      st.session_state["stage"] = "dashboard"
      st.rerun()

# --- AŞAMA 4: DAHİLİ KURS PANELI (DASHBOARD) ---
elif st.session_state["stage"] == "dashboard":
  st.title(f"🗺️ {st.session_state['user_name']} - Müfredat ve Eğitim Paneli")
  st.success(
      f"🎯 **Hedef:** {st.session_state['user_goal']} | 🌟 **Hayalin:**"
      f" *{st.session_state['user_dream']}*"
  )

  st.markdown("### 📚 Yoğun Eğitim Modülleriniz (5-10 Dk Dersler)")

  for idx, mod in enumerate(st.session_state["modules"]):
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
      st.markdown(f"**{mod['title']}**")
      st.caption(
          f"Süre: ~{mod['duration']} | Odak: {mod['skill']} | Hedef Kelime:"
          f" {mod['words']} adet"
      )
    with col2:
      st.markdown(f"Durum: **{mod['status']}**")
    with col3:
      if mod["status"] in ["Açık", "Tamamlandı"]:
        btn_txt = "Dese Başla 📖" if mod["status"] == "Açık" else "Tekrar Et 🔄"
        if st.button(btn_txt, key=f"mod_btn_{idx}", type="primary"):
          st.session_state["current_module_idx"] = idx
          st.session_state["lesson_step"] = 1
          # Önceki modül geçici içeriklerini temizle
          for key in [
              "reading_content",
              "vocab_content",
              "quiz_content",
              "writing_checked",
          ]:
            if key in st.session_state:
              del st.session_state[key]
          st.session_state["stage"] = "learning"
          st.rerun()
      else:
        st.info("🔒 Kilitli")
    st.markdown("---")

# --- AŞAMA 5: KAPSAMLI DERS İŞLEŞİ (LEARNING STAGE) ---
elif st.session_state["stage"] == "learning":
  mod_idx = st.session_state["current_module_idx"]
  active_mod = st.session_state["modules"][mod_idx]
  step = st.session_state["lesson_step"]

  st.title(f"📖 {active_mod['title']}")
  st.progress(
      step / 4,
      text=(
          f"Eğitim İlerlemesi: Adım {step} / 4 ("
          "1:Okuma->2:Kelime/Kalıp->3:Test->4:Yazma)"
      ),
  )

  # --- ADIM 1: ZENGİN OKUMA VE HİKAYE METNİ ---
  if step == 1:
    st.subheader("📜 1. Bölüm: Bağlamsal Okuma ve Hikaye Analizi")
    st.markdown(
        "Bu bölümde hedefiniz doğrultusunda hazırlanmış gerçek hayat"
        " senaryosunu inceleyin."
    )

    if "reading_content" not in st.session_state:
      prompt_read = (
          f"Create a rich, professional, 2-paragraph educational reading"
          f" passage in {st.session_state['target_lang']} for level"
          f" {st.session_state['current_level']}, tailored to the user's dream:"
          f" '{st.session_state['user_dream']}' and module '{active_mod['title']}'."
          " Include a clear Turkish summary/translation right below it to"
          " ensure complete comprehension."
      )
      try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_read}],
            temperature=0.7,
        )
        st.session_state["reading_content"] = res.choices[0].message.content
      except Exception:
        st.session_state["reading_content"] = (
            "Okuma metni yüklenirken hata oluştu."
        )

    st.markdown(st.session_state["reading_content"])
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Kelime ve Cümle Kalıplarına Geç ➡️", type="primary"):
      st.session_state["lesson_step"] = 2
      st.rerun()

  # --- ADIM 2: KELİME VE CÜMLE KALIBI ANALİZİ ---
  elif step == 2:
    st.subheader("🔑 2. Bölüm: Kritik Kelimeler ve Cümle Kalıpları")
    st.markdown(
        "Bu derste ustalaşmanız gereken temel yapı taşları ve kalıplar:"
    )

    if "vocab_content" not in st.session_state:
      prompt_vocab = (
          f"List 5 essential vocabulary words and 3 key sentence patterns from"
          f" the previous context for {st.session_state['target_lang']} at"
          f" level {st.session_state['current_level']}. Explain their"
          f" meanings and usages in Turkish clearly with examples."
      )
      try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_vocab}],
            temperature=0.7,
        )
        st.session_state["vocab_content"] = res.choices[0].message.content
      except Exception:
        st.session_state["vocab_content"] = "Kelime listesi yüklenemedi."

    st.markdown(st.session_state["vocab_content"])
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
      if st.button("⬅️ Geri Dön"):
        st.session_state["lesson_step"] = 1
        st.rerun()
    with col2:
      if st.button("İnteraktif Teste Geç ➡️", type="primary"):
        st.session_state["lesson_step"] = 3
        st.rerun()

  # --- ADIM 3: İNTERAKTİF TEST VE BOŞLUK DOLDURMA ---
  elif step == 3:
    st.subheader(
        "🧩 3. Bölüm: Bilgiyi Pekiştirme (Boşluk Doldurma ve Çoktan Seçmeli)"
    )
    st.markdown("Öğrendiklerinizi test etme zamanı.")

    if "quiz_content" not in st.session_state:
      prompt_quiz = (
          f"Create 2 high-quality multiple choice or fill-in-the-blank"
          f" educational exercises in {st.session_state['target_lang']} for"
          f" level {st.session_state['current_level']} based on module"
          f" '{active_mod['title']}'. Provide helpful hints in Turkish, 4"
          f" options (A, B, C, D) per question, and explicitly include 'Dogru"
          f" Cevaplar: ...' at the very end."
      )
      try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_quiz}],
            temperature=0.7,
        )
        st.session_state["quiz_content"] = res.choices[0].message.content
      except Exception:
        st.session_state["quiz_content"] = "Test yüklenemedi."

    st.markdown(st.session_state["quiz_content"])
    user_ans_q3 = st.text_input(
        "Cevaplarınızı giriniz (Örn: 1-A, 2-C):", key="quiz_input_field"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
      if st.button("⬅️ Kelime Analizine Dön"):
        st.session_state["lesson_step"] = 2
        st.rerun()
    with col2:
      if st.button("Yazma Pratiğine Geç ➡️", type="primary"):
        if user_ans_q3.strip():
          st.session_state["lesson_step"] = 4
          st.rerun()
        else:
          st.warning("Lütfen test cevaplarınızı yazın.")

  # --- ADIM 4: YAZMA VE ÜRETİM PRATİĞİ ---
  elif step == 4:
    st.subheader("✍️ 4. Bölüm: Aktif Yazma ve Cümle Üretimi")
    st.markdown(
        f"Bu modülde öğrendiğiniz kelime ve kalıplarla, hayalinize ('"
        f"{st.session_state['user_dream']}') atıfta bulunan en az 2 cümlelik"
        " kendi cümlenizi yazın:"
    )

    user_writing = st.text_area(
        "Cümlelerinizi buraya yazın:",
        placeholder=(
            "Örn: In order to reach my dream, I practice every day..."
        ),
    )

    if st.button("Dersi Tamamla ve Bölüm Karnesini Gör 🏆", type="primary"):
      if user_writing.strip():
        # Karnede gösterilecek verileri hazırla
        st.session_state["current_report"] = {
            "module_title": active_mod["title"],
            "learned_words": active_mod["words"],
            "user_text": user_writing,
            "status": "Başarıyla Tamamlandı",
        }

        # Modülü güncelle
        if active_mod["status"] != "Tamamlandı":
          st.session_state["total_words"] += active_mod["words"]
          st.session_state["achievements"].append(active_mod["title"])
          st.session_state["modules"][mod_idx]["status"] = "Tamamlandı"

        st.session_state["stage"] = "report_card"
        st.rerun()
      else:
        st.warning(
            "Lütfen ilerlemek için metin kutusuna cümlelerinizi yazınız."
        )

# --- AŞAMA 6: BÖLÜM KARNESİ (REPORT CARD) ---
elif st.session_state["stage"] == "report_card":
  report = st.session_state["current_report"]

  st.title("🎖️ RESMİ BÖLÜM KARNESİ VE DEĞERLENDİRME RAPORU")
  st.balloons()

  st.markdown(
      f"""
    <div style="border: 3px solid #2e7d32; padding: 25px; border-radius: 12px; background-color: #f1f8e9;">
        <h3 style="color: #1b5e20; text-align: center;">📚 LingoFlow Pro Eğitim Karnesi</h3>
        <hr>
        <p><b>Öğrenci Adı:</b> {st.session_state['user_name']}</p>
        <p><b>Hedef Dil / Seviye:</b> {st.session_state['target_lang']} ({st.session_state['current_level']})</p>
        <p><b>Tamamlanan Modül:</b> {report.get('module_title')}</p>
        <p><b>Durum:</b> <span style="color: green; font-weight: bold;">{report.get('status')}</span></p>
        <hr>
        <p><b>✨ Kazanımlar ve İstatistikler:</b></p>
        <ul>
            <li>Bu derste eklenen dağarcık: <b>+{report.get('learned_words')} kelime ve kalıp</b></li>
            <li>Toplam biriken kelime: <b>{st.session_state['total_words']} kelime</b></li>
            <li>Yazdığınız Pratik Cümle: <i>"{report.get('user_text')}"</i></li>
        </ul>
        <p style="text-align: center; color: #388e3c; font-weight: bold; margin-top: 20px;">
            Harika bir çalışma çıkardınız! Bilgiler kalıcı hafızanıza işlendi.
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  col1, col2 = st.columns(2)
  with col1:
    if st.button("🗺️ Müfredat Paneline Geri Dön", type="primary"):
      # Sonraki modülü aç
      next_idx = st.session_state["current_module_idx"] + 1
      if next_idx < len(st.session_state["modules"]):
        if st.session_state["modules"][next_idx]["status"] == "Kilitli":
          st.session_state["modules"][next_idx]["status"] = "Açık"
      st.session_state["stage"] = "dashboard"
      st.rerun()
  with col2:
    if st.button("🌟 Tüm Kurs Sertifikasını İncele"):
      st.session_state["stage"] = "certificate"
      st.rerun()

# --- AŞAMA 7: KURS BİTİRME SERTİFİKASI ---
elif st.session_state["stage"] == "certificate":
  st.title("🏆 MÜKEMMEL BAŞARI - SERTİFİKA ALANI")
  st.balloons()

  st.markdown(
      f"""
    <div style="border: 5px solid #ffb300; padding: 35px; border-radius: 15px; text-align: center; background-color: #fffde7;">
        <h1 style="color: #f57f17;">🎓 ÜSTÜN BAŞARI SERTİFİKASI 🎓</h1>
        <p>Bu belge,</p>
        <h2><b>{st.session_state['user_name']}</b></h2>
        <p>tarafından <b>{st.session_state['target_lang']}</b> dilinde tamamlanan yoğun program sonucunda,</p>
        <h3><b>{st.session_state['current_level']} Seviyesi Profesyonel Eğitim Serisi</b>ni</h3>
        <p>başarıyla bitirdiğini ve <i>"{st.session_state['user_dream']}"</i> hedefine ulaştığını tasdik eder.</p>
        <hr style="width: 40%; margin: 20px auto;">
        <p><b>Toplam Kazanılan Kelime:</b> {st.session_state['total_words']} adet</p>
        <p><b>Tamamlanan Modüller:</b> {', '.join(st.session_state['achievements'])}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("🔄 Ana Menüye Dön ve Yeniden Başla"):
    for key in list(st.session_state.keys()):
      del st.session_state[key]
    st.rerun()
