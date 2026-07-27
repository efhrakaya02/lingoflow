import json
import os
import streamlit as st

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Lingoflow A1 Master Curriculum",
    page_icon="🌐",
    layout="wide",
)

# Özel CSS İyileştirmeleri
st.markdown(
    """
    <style>
    .vocab-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }
    .vocab-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
    }
    .skill-header {
        background-color: #f0f2f6;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .grammar-workshop {
        background-color: #f4f8fb;
        padding: 20px;
        border-radius: 10px;
        border: 1px dashed #0066cc;
        margin-top: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# JSON Verisini Yükleme Fonksiyonu
@st.cache_data
def load_curriculum():
  file_path = "a1_curriculum.json"
  if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
      return json.load(f)
  else:
    return None


data = load_curriculum()

# --- UYGULAMA BAŞLIĞI VE KENAR ÇUBUĞU ---
st.title("🌐 Lingoflow A1 Master Curriculum")
st.markdown(
    "CEFR A1 ve Uluslararası Sertifikasyon Sınavları (KET/telc) Uyumlu İnteraktif"
    " Öğrenme Platformu"
)

if data is None:
  st.error(
      "⚠️ `a1_curriculum.json` dosyası bulunamadı! Lütfen JSON dosyasını proje"
      " klasörüne ekleyin."
  )
else:
  modules = data.get("modules", [])

  # Kenar Çubuğu: Modül Seçimi ve İlerleme
  st.sidebar.header("📖 Modül Navigasyonu")
  module_titles = [f"Modül {m['module_id']}: {m['title']}" for m in modules]
  selected_module_idx = st.sidebar.selectbox(
      "Çalışmak istediğiniz modülü seçin:", range(len(module_titles)), format_func=lambda x: module_titles[x]
  )

  current_module = modules[selected_module_idx]
  mod_id = current_module["module_id"]

  # --- ANA İÇERİK SEKMELERİ ---
  tab_obj, tab_vocab, tab_grammar, tab_exam = st.tabs([
      "🎯 Hedef & Amaç",
      "🗣️ Kelime Hazinesi",
      "💡 Dil Bilgisi (Grammar Pill)",
      "📝 4 Temel Beceri Sınavı & Simülasyonu",
  ])

  # 1. SEKME: HEDEF & AMAÇ
  with tab_obj:
    st.header(f"Modül {mod_id}: {current_module['title']}")
    st.info(f"🎯 **Modülün Ana Hedefi:** {current_module['objective']}")

    col1, col2 = st.columns(2)
    with col1:
      st.markdown("### 📌 Bu Modülde Neler Öğreneceksiniz?")
      st.markdown(
          "- Günlük hayatta sık kullanılan temel kelime kalıpları\n- Dil bilgisi"
          " kurallarının mantığı ve pratik yapıları\n- Uluslararası sınav"
          " formatına uygun soru çözme teknikleri"
      )
    with col2:
      st.markdown("### 🚀 Çalışma Tavsiyesi")
      st.markdown(
          "1. Önce **Kelime Hazinesi** sekmesinden kartları inceleyin.\n2."
          " **Dil Bilgisi** sekmesinden kuralları okuyup *Mini Pratik* yapın.\n3."
          " Son olarak **Sınav Simülasyonu** ile 4 beceride kendinizi test"
          " edin."
      )

  # 2. SEKME: KELİME HAZİNESİ (İNTERAKTİF KARTLAR)
  with tab_vocab:
    st.header("🗣️ Kelime Hazinesi & Örnek Cümleler")
    st.markdown(
        "Bu modüle ait anahtar kelimeleri ve örnek kullanımlarını aşağıda"
        " bulabilirsiniz:"
    )

    vocab_list = current_module.get("vocabulary", [])
    cols = st.columns(2)
    for idx, item in enumerate(vocab_list):
      with cols[idx % 2]:
        st.markdown(
            f"""
                <div class="vocab-card">
                    <h4 style="margin: 0; color: #0066cc;">{item['term']}</h4>
                    <p style="margin: 8px 0; font-size: 16px; font-weight: bold; color: #222;">{item['translation']}</p>
                    <p style="margin: 0; font-style: italic; color: #555;">💬 Örnek: "{item['example']}"</p>
                </div>
                """,
            unsafe_allow_html=True,
        )

  # 3. SEKME: GRAMMAR PILL (DİL BİLGİSİ + İNTERAKTİF ATÖLYE)
  with tab_grammar:
    grammar = current_module.get("grammar_pill", {})
    st.header(f"💡 {grammar.get('title', 'Dil Bilgisi Kuralı')}")

    st.markdown(
        f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #0066cc; margin-bottom: 20px;">
        <h4 style="margin-top:0; color:#333;">Kural Açıklaması</h4>
        <p style="font-size: 16px; color: #444;">{grammar.get('explanation', '')}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("📌 Temel Kurallar ve İstisnalar:")
    for rule in grammar.get("rules", []):
      st.markdown(f"* **{rule}**")

    # --- İNTERAKTİF DİL BİLGİSİ ATÖLYESİ (MİNİ PRATİK) ---
    st.markdown("---")
    st.markdown(
        '<div class="grammar-workshop"><h3>🛠️ İnteraktif Dil Bilgisi Atölyesi'
        ' (Anında Pratik)</h3><p>Öğrendiğiniz kuralı hemen pekiştirmek için'
        ' aşağıdaki hızlı meydan okumayı tamamlayın:</p></div>',
        unsafe_allow_html=True,
    )

    # Modüle özel dinamik mini pratik senaryoları
    if mod_id == 1:
      st.markdown("**Soru:** Doğru selamlaşma kalıbını seçin:")
      ans1 = st.radio(
          "Sabah vakti birine ne denir?",
          ["Good evening", "Good morning", "Goodbye"],
          key="g_mod1",
      )
      if st.button("Kontrol Et", key="btn_g1"):
        if ans1 == "Good morning":
          st.success("Tebrikler! Doğru cevap 🎉")
        else:
          st.error("Yanlış. Sabahları 'Good morning' denir.")

    elif mod_id == 2:
      st.markdown(
          "**Soru:** 'She' öznesiyle hangi 'To Be' (am/is/are) formu kullanılır?"
      )
      ans2 = st.radio(
          "Boşluğu doldurun: She ___ a doctor.", ["am", "is", "are"], key="g_mod2"
      )
      if st.button("Kontrol Et", key="btn_g2"):
        if ans2 == "is":
          st.success("Harika! 'She is' doğru kullanımdır 🎉")
        else:
          st.error(
              "Yanlış. Tekil öznelerde (He/She/It) 'is' fiili kullanılır."
          )

    elif mod_id == 3:
      st.markdown(
          "**Soru:** Uzaktaki birden fazla nesneyi işaret etmek için hangi zamir"
          " kullanılır?"
      )
      ans3 = st.radio(
          "Seçiminizi yapın:", ["This", "These", "Those"], key="g_mod3"
      )
      if st.button("Kontrol Et", key="btn_g3"):
        if ans3 == "Those":
          st.success("Mükemmel! 'Those' uzak çoğul demektir 🎉")
        else:
          st.error(
              "Yanlış. Uzaktaki çoğullar için 'Those' kelimesi kullanılır."
          )

    elif mod_id == 4:
      st.markdown(
          "**Soru:** 'He' zamiri için sahip olma (have/has got) yapısı nasıldır?"
      )
      ans4 = st.radio(
          "Seçiminizi yapın:",
          ["He have got a car", "He has got a car", "He is got a car"],
          key="g_mod4",
      )
      if st.button("Kontrol Et", key="btn_g4"):
        if ans4 == "He has got a car":
          st.success("Doğru! 3. tekil şahıslarda 'has got' kullanılır 🎉")
        else:
          st.error("Yanlış. Doğru yapı 'He has got a car' şeklindedir.")

    elif mod_id == 5:
      st.markdown(
          "**Soru:** Kesin saatlerin önüne hangi zaman edatı (preposition)"
          " getirilir?"
      )
      ans5 = st.radio(
          "Örnek: ___ 5 o'clock", ["in", "on", "at"], key="g_mod5"
      )
      if st.button("Kontrol Et", key="btn_g5"):
        if ans5 == "at":
          st.success("Harika! Kesin saatler için 'at' kullanılır 🎉")
        else:
          st.error("Yanlış. Saatlerin önüne 'at' gelmelidir (at 5 o'clock).")

    elif mod_id == 6:
      st.markdown(
          "**Soru:** Kedi masanın altındaysa İngilizce nasıl ifade edilir?"
      )
      ans6 = st.radio(
          "Seçiminizi yapın:",
          [
              "The cat is on the table",
              "The cat is under the table",
              "The cat is in the table",
          ],
          key="g_mod6",
      )
      if st.button("Kontrol Et", key="btn_g6"):
        if ans6 == "The cat is under the table":
          st.success("Tebrikler! 'Under' altında anlamına gelir 🎉")
        else:
          st.error("Yanlış. 'Under' kelimesi 'altında' demektir.")

    elif mod_id == 7:
      st.markdown(
          "**Soru:** Geniş zamanda (Present Simple) 'He' öznesinde fiil nasıl"
          " çekimlenir?"
      )
      ans7 = st.radio(
          "Boşluğu doldurun: He ___ (work) in an office.",
          ["work", "works", "working"],
          key="g_mod7",
      )
      if st.button("Kontrol Et", key="btn_g7"):
        if ans7 == "works":
          st.success("Mükemmel! He/She/It ile fiil '-s' takısı alır 🎉")
        else:
          st.error("Yanlış. Geniş zamanda tekil şahıslarda fiile '-s' eklenir.")

    elif mod_id == 8:
      st.markdown(
          "**Soru:** Yetenek bildiren 'can' fiilinden sonra gelen asıl fiil nasıl"
          " yazılır?"
      )
      ans8 = st.radio(
          "Seçiminizi yapın:",
          ["Yalın (ek almamış hali)", "-ing takısı alarak", "Geçmiş zaman"],
          key="g_mod8",
      )
      if st.button("Kontrol Et", key="btn_g8"):
        if ans8 == "Yalın (ek almamış hali)":
          st.success("Doğru! 'Can' modal fiilinden sonra fiil yalın gelir 🎉")
        else:
          st.error("Yanlış. 'Can' sonrasında fiiller ek almaz (yalın kalır).")

    elif mod_id == 9:
      st.markdown(
          "**Soru:** Şu an yapılan bir eylemi anlatan (Present Continuous)"
          " cümlede fiilin sonuna ne eklenir?"
      )
      ans9 = st.radio(
          "Seçiminizi yapın:", ["-s", "-ed", "-ing"], key="g_mod9"
      )
      if st.button("Kontrol Et", key="btn_g9"):
        if ans9 == "-ing":
          st.success("Harika! Continuous yapılarda '-ing' eki şarttır 🎉")
        else:
          st.error("Yanlış. Şu anki zaman için fiile '-ing' eklenir.")

    elif mod_id == 10:
      st.markdown(
          "**Soru:** Bir ürünün tekil fiyatını sormak için hangi kalıp"
          " kullanılır?"
      )
      ans10 = st.radio(
          "Seçiminizi yapın:",
          ["How much are these?", "How much is this?", "How many is this?"],
          key="g_mod10",
      )
      if st.button("Kontrol Et", key="btn_g10"):
        if ans10 == "How much is this?":
          st.success("Tebrikler! Tekil ürünler için 'How much is this?' denir 🎉")
        else:
          st.error(
              "Yanlış. Tekil ürünlerde 'is this', çoğullarda 'are these' kullanılır."
          )

    elif mod_id == 11:
      st.markdown(
          "**Soru:** Geçmiş zamandaki durum bildiren 'We' öznesi için hangi"
          " geçmiş yardımcı fiil kullanılır?"
      )
      ans11 = st.radio(
          "Boşluğu doldurun: We ___ at home yesterday.",
          ["was", "were", "are"],
          key="g_mod11",
      )
      if st.button("Kontrol Et", key="btn_g11"):
        if ans11 == "were":
          st.success("Mükemmel! You/We/They için 'were' kullanılır 🎉")
        else:
          st.error(
              "Yanlış. 'We' çoğul bir öznedir, geçmiş hali 'were' olmalıdır."
          )

    else:
      st.markdown(
          "**Soru:** Bu modüldeki genel soru kelimelerinden (Wh-) yer soran"
          " kelime hangisidir?"
      )
      ans12 = st.radio(
          "Seçiminizi yapın:", ["What", "Where", "When"], key="g_mod12"
      )
      if st.button("Kontrol Et", key="btn_g12"):
        if ans12 == "Where":
          st.success("Doğru! 'Where' nerede/yer sorar 🎉")
        else:
          st.error("Yanlış. Yer sormak için 'Where' kullanılır.")

  # 4. SEKME: SINAV SİMÜLASYONU (4 TEMEL BECERİ: OKUMA, DİNLEME, KONUŞMA, YAZMA)
  with tab_exam:
    st.header("📝 4 Temel Dil Becerisi Sınav Simülasyonu")
    st.markdown(
        "KET ve telc sınav formatına birebir uygun olarak hazırlanmış pratik"
        " alanları:"
    )

    exam = current_module.get("exam_simulation", {})

    # Alt Sekmeler ile 4 Beceriye Bölme
    skill_tab1, skill_tab2, skill_tab3, skill_tab4 = st.tabs([
        "📖 Okuma (Reading)",
        "🎧 Dinleme (Listening)",
        "🗣️ Konuşma (Speaking)",
        "✍️ Yazma (Writing)",
    ])

    # --- 1. OKUMA ---
    with skill_tab1:
      st.markdown(
          '<div class="skill-header">📖 Okuma Becerisi ve Anlama</div>',
          unsafe_allow_html=True,
      )
      if "reading" in exam:
        st.info("Aşağıdaki metni dikkatlice okuyunuz:")
        st.code(exam["reading"], language="text")

      st.markdown("### Sorular")
      questions = exam.get("questions", [])
      user_answers = {}

      for q_idx, q in enumerate(questions):
        st.markdown(f"**Soru {q_idx + 1}:** {q['q']}")
        user_choice = st.radio(
            "Seçiminizi yapın:",
            q["options"],
            key=f"q_{current_module['module_id']}_{q_idx}",
        )
        user_answers[q_idx] = (user_choice, q["answer"])

      if st.button(
          "Cevapları Kontrol Et", key=f"check_{current_module['module_id']}"
      ):
        for q_idx, (chosen, correct) in user_answers.items():
          if chosen == correct:
            st.success(f"Soru {q_idx + 1}: Doğru! 🎉")
          else:
            st.error(
                f"Soru {q_idx + 1}: Yanlış. Doğru cevap: **{correct}**"
                " olmalıydı."
            )

    # --- 2. DİNLEME ---
    with skill_tab2:
      st.markdown(
          '<div class="skill-header">🎧 Dinleme (Listening) Simülasyonu</div>',
          unsafe_allow_html=True,
      )
      st.markdown(
          "Aşağıdaki butona tıklayarak veya metni tarayıcınıza okutarak"
          " dinleme simülasyonunu gerçekleştirebilir ve sesli anlama pratiği"
          " yapabilirsiniz."
      )

      listening_text = exam.get(
          "reading", "Audio script unavailable for this module."
      )
      st.text_area(
          "Dinleme Metni (Audio Script):", value=listening_text, height=100
      )

      tts_html = f"""
            <div style="margin-top: 10px;">
                <button onclick="speakText()" style="background-color: #0066cc; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">🔊 Metni Sesli Dinle (Play Audio)</button>
            </div>
            <script>
            function speakText() {{
                const text = {json.dumps(listening_text)};
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                window.speechSynthesis.speak(utterance);
            }}
            </script>
            """
      st.components.v1.html(tts_html, height=70)

    # --- 3. KONUŞMA ---
    with skill_tab3:
      st.markdown(
          '<div class="skill-header">🗣️ Konuşma (Speaking) Pratiği</div>',
          unsafe_allow_html=True,
      )
      st.markdown(
          "Bu bölümde hedef, modül konusuna uygun olarak sesli ifade becerinizi"
          " geliştirmektir."
      )

      st.warning(
          "📢 **Konuşma Görevi:** Bu modüldeki hedef kelimeleri ve dil bilgisi"
          " kalıplarını kullanarak yüksek sesle kendi kendine en az 3 cümle"
          " kurun."
      )

      user_spoken_text = st.text_input(
          "Konuşma provası yaparken söyleyeceğiniz cümleleri buraya yazarak"
          " önce taslak oluşturun:"
      )
      if st.button("Konuşma Taslağını Kaydet"):
        if user_spoken_text.strip():
          st.success(
              "Harika! Konuşma taslağınız kaydedildi. Şimdi bunu yüksek"
              " sesle okuyun."
          )
        else:
          st.warning("Lütfen pratik yapmak için birkaç kelime veya cümle girin.")

    # --- 4. YAZMA ---
    with skill_tab4:
      st.markdown(
          '<div class="skill-header">✍️ Yazma (Writing) Görevi</div>',
          unsafe_allow_html=True,
      )
      writing_task_desc = exam.get(
          "writing_task", "Bu modül için özel yazma görevi bulunmuyor."
      )
      st.info(f"📌 **Yazma Görevi Yönergesi:** {writing_task_desc}")

      user_writing = st.text_area(
          "Cevabınızı İngilizce olarak buraya yazın:",
          key=f"writing_{current_module['module_id']}",
          height=150,
      )

      if st.button(
          "Yazı Görevini Gönder", key=f"submit_w_{current_module['module_id']}"
      ):
        if user_writing.strip():
          word_count = len(user_writing.split())
          st.success(
              f"🎉 Yazı görevi başarıyla gönderildi! Kelime sayısı: {word_count}."
              " Harika bir pratik çıkardınız!"
          )
        else:
          st.warning(
              "Lütfen boş bırakmayın, yönergeye uygun şekilde en az bir cümle"
              " yazın."
          )
