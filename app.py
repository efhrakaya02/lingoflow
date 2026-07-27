import json
import os
import streamlit as st

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Lingoflow A1 Master Curriculum",
    page_icon="📚",
    layout="wide",
)


# JSON Verisini Yükleme Fonksiyonu
@st.cache_data
def load_curriculum():
  file_path = "a1_curriculum.json"
  if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
      return json.load(f)
  else:
    # Eğer dosya henüz kaydedilmediyse, doğrudan veri yapısını kullanabilmek için fallback
    return None


data = load_curriculum()

# --- UYGULAMA BAŞLIĞI VE KENAR ÇUCUĞU ---
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

  # Kenar Çubuğu: Modül Seçimi
  st.sidebar.header("📖 Modüller")
  module_titles = [f"Modül {m['module_id']}: {m['title']}" for m in modules]
  selected_module_idx = st.sidebar.selectbox(
      "Çalışmak istediğiniz modülü seçin:", range(len(module_titles)), format_func=lambda x: module_titles[x]
  )

  current_module = modules[selected_module_idx]

  # --- ANA İÇERİK SEKMELERİ ---
  tab_obj, tab_vocab, tab_grammar, tab_exam = st.tabs([
      "🎯 Hedef & Amaç",
      "🗣️ Kelime Hazinesi",
      "💡 Dil Bilgisi (Grammar Pill)",
      "📝 Sınav Simülasyonu",
  ])

  # 1. SEKME: HEDEF
  with tab_obj:
    st.header(f"Modül {current_module['module_id']}: {current_module['title']}")
    st.info(f"**Modülün Amacı:** {current_module['objective']}")
    st.markdown("---")
    st.markdown(
        "Bu modülü tamamlayarak temel seviyedeki bu konuyu pratik yapabilir ve"
        " sınav sorularını çözebilirsiniz."
    )

  # 2. SEKME: KELİME HAZİNESİ
  with tab_vocab:
    st.header("Kelime Kartları & Örnekler")
    vocab_list = current_module.get("vocabulary", [])

    cols = st.columns(2)
    for idx, item in enumerate(vocab_list):
      with cols[idx % 2]:
        st.markdown(
            f"""
                <div style="padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; background-color: #f9f9f9;">
                    <h4 style="margin: 0; color: #1f77b4;">{item['term']}</h4>
                    <p style="margin: 5px 0; font-weight: bold; color: #333;">{item['translation']}</p>
                    <p style="margin: 0; font-style: italic; color: #666;">Örnek: "{item['example']}"</p>
                </div>
                """,
            unsafe_allow_html=True,
        )

  # 3. SEKME: GRAMMAR PILL
  with tab_grammar:
    grammar = current_module.get("grammar_pill", {})
    st.header(f"💡 {grammar.get('title', 'Dil Bilgisi Kuralı')}")
    st.write(grammar.get("explanation", ""))

    st.subheader("Temel Kurallar:")
    for rule in grammar.get("rules", []):
      st.markdown(f"* {rule}")

  # 4. SEKME: SINAV SİMÜLASYONU
  with tab_exam:
    st.header("📝 Sınav ve Pratik Simülasyonu")
    exam = current_module.get("exam_simulation", {})

    # Okuma Parçası / Senaryo
    if "reading" in exam:
      st.markdown("### Okuma / Diyalog Metni")
      st.code(exam["reading"], language="text")

    st.markdown("### Çoktan Seçmeli Sorular")
    questions = exam.get("questions", [])
    user_answers = {}

    for q_idx, q in enumerate(questions):
      st.markdown(f"**Soru {q_idx + 1}:** {q['q']}")
      user_choice = st.radio(
          "Seçiminizi yapın:", q["options"], key=f"q_{current_module['module_id']}_{q_idx}"
      )
      user_answers[q_idx] = (user_choice, q["answer"])

    if st.button("Cevapları Kontrol Et", key=f"check_{current_module['module_id']}"):
      all_correct = True
      for q_idx, (chosen, correct) in user_answers.items():
        if chosen == correct:
          st.success(f"Soru {q_idx + 1}: Doğru! 🎉")
        else:
          st.error(
              f"Soru {q_idx + 1}: Yanlış. Doğru cevap: **{correct}** olmalıydı."
          )
          all_correct = False

    st.markdown("---")
    st.markdown("### Yazma Görevi (Writing Task)")
    st.info(exam.get("writing_task", ""))
    user_writing = st.text_area(
        "Cevabınızı buraya İngilizce olarak yazın:",
        key=f"writing_{current_module['module_id']}",
    )
    if st.button(
        "Yazı Görevini Gönder", key=f"submit_w_{current_module['module_id']}"
    ):
      if user_writing.strip():
        st.success(
            "Harika! Yazma göreviniz başarıyla kaydedildi. Pratiğe devam"
            " edin!"
        )
      else:
        st.warning("Lütfen boş bırakmayın, kısa bir cümle de olsa yazın.")
