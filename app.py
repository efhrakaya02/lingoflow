import json
from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="LingoFlow Pro - JSON Destekli Dil Akademisi",
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

# --- MÜFREDAT JSON VERİ TABANI (A1 VE DİĞER SEVİYELER) ---
CURRICULUM_JSON = """
{
  "A1": [
    {
      "id": 1,
      "title": "Modül 1: Temel Selamlaşma, Tanışma ve Kişisel Bilgiler",
      "duration": "10 dk",
      "words": 20,
      "skill": "Okuma & Temel Tanışma Kalıpları",
      "status": "Açık"
    },
    {
      "id": 2,
      "title": "Modül 2: Günlük Nesneler, Sınırlar ve Soru Zamirleri",
      "duration": "10 dk",
      "words": 25,
      "skill": "Kelime Dağarcığı & Temel Cümle Yapısı",
      "status": "Kilitli"
    },
    {
      "id": 3,
      "title": "Modül 3: Aile, Çevre ve Basit Tanımlamalar",
      "duration": "12 dk",
      "words": 30,
      "skill": "İlişkiler & Sosyal İfade",
      "status": "Kilitli"
    },
    {
      "id": 4,
      "title": "Modül 4: Temel Zamanlar ve Günlük Rutinler Zirvesi",
      "duration": "15 dk",
      "words": 35,
      "skill": "Özgür İfade & A1 Sentezi",
      "status": "Kilitli"
    }
  ],
  "A2": [
    {
      "id": 1,
      "title": "Modül 1: Geçmiş Zaman Anıları ve Hikaye Anlatımı",
      "duration": "10 dk",
      "words": 22,
      "skill": "Geçmiş Zaman & Bağlam",
      "status": "Açık"
    },
    {
      "id": 2,
      "title": "Modül 2: Gelecek Planları ve Seyahat Senaryoları",
      "duration": "10 dk",
      "words": 26,
      "skill": "Gelecek Zaman & Pratik",
      "status": "Kilitli"
    },
    {
      "id": 3,
      "title": "Modül 3: Alışveriş, Restoran ve Sosyal Diyaloglar",
      "duration": "12 dk",
      "words": 30,
      "skill": "Günlük Akış Yönetimi",
      "status": "Kilitli"
    },
    {
      "id": 4,
      "title": "Modül 4: A2 Hedef Zirvesi ve Akıcılık Testi",
      "duration": "15 dk",
      "words": 35,
      "skill": "Sentez & Tamamlama",
      "status": "Kilitli"
    }
  ],
  "B1": [
    {
      "id": 1,
      "title": "Modül 1: Fikir Beyan Etme ve Tartışma Kültürü",
      "duration": "12 dk",
      "words": 25,
      "skill": "Argüman Geliştirme",
      "status": "Açık"
    },
    {
      "id": 2,
      "title": "Modül 2: İş Hayatı ve Profesyonel İletişim",
      "duration": "12 dk",
      "words": 30,
      "skill": "Kariyer Dil Bilgisi",
      "status": "Kilitli"
    },
    {
      "id": 3,
      "title": "Modül 3: Karmaşık Olaylar ve Problem Çözme Senaryoları",
      "duration": "15 dk",
      "words": 35,
      "skill": "Stratejik İletişim",
      "status": "Kilitli"
    },
    {
      "id": 4,
      "title": "Modül 4: B1 Yetkinlik ve Küresel Sunum Zirvesi",
      "duration": "15 dk",
      "words": 40,
      "skill": "İleri Düzey Sentez",
      "status": "Kilitli"
    }
  ],
  "B2": [
    {
      "id": 1,
      "title": "Modül 1: Soyut Kavramlar ve Edebi Metin Analizi",
      "duration": "15 dk",
      "words": 30,
      "skill": "Derinlemesine Anlama",
      "status": "Açık"
    },
    {
      "id": 2,
      "title": "Modül 2: Müzakere, İkna ve Profesyonel Liderlik",
      "duration": "15 dk",
      "words": 35,
      "skill": "İleri Müzakere",
      "status": "Kilitli"
    },
    {
      "id": 3,
      "title": "Modül 3: Küresel Medya ve Teknik Makale İncelemesi",
      "duration": "18 dk",
      "words": 40,
      "skill": "Akademik/Teknik Okuma",
      "status": "Kilitli"
    },
    {
      "id": 4,
      "title": "Modül 4: B2 Zirvesi ve Uzmanlık Sertifikasyonu",
      "duration": "20 dk",
      "words": 50,
      "skill": "Ana Dil Seviyesine Yakın Sentez",
      "status": "Kilitli"
    }
  ]
}
"""

# JSON verisini Python sözlüğüne parse etme
CURRICULUM_DATA = json.loads(CURRICULUM_JSON)


# --- OTURUM DURUMU (STATE) BAŞLANGIÇLARI ---
if "stage" not in st.session_state:
  st.session_state["stage"] = "welcome"
if "user_name" not in st.session_state:
  st.session_state["user_name"] = ""
if "target_lang" not in st.session_state:
  st.session_state["target_lang"] = "İngilizce (English)"
if "placement_step" not in st.session_state:
  st.session_state["placement_step"] = 1
if "placement_answers" not in st.session_state:
  st.session_state["placement_answers"] = {}
if "current_level" not in st.session_state:
  st.session_state["current_level"] = "A1"
if "personality_profile" not in st.session_state:
  st.session_state["personality_profile"] = ""
if "user_goal" not in st.session_state:
  st.session_state["user_goal"] = ""
if "user_dream" not in st.session_state:
  st.session_state["user_dream"] = ""
if "modules" not in st.session_state:
  st.session_state["modules"] = []
if "current_module_idx" not in st.session_state:
  st.session_state["current_module_idx"] = 0
if "lesson_step" not in st.session_state:
  st.session_state["lesson_step"] = 1
if "total_words" not in st.session_state:
  st.session_state["total_words"] = 0
if "achievements" not in st.session_state:
  st.session_state["achievements"] = []
if "current_report" not in st.session_state:
  st.session_state["current_report"] = {}
if "quiz_feedback" not in st.session_state:
  st.session_state["quiz_feedback"] = ""
if "writing_feedback" not in st.session_state:
  st.session_state["writing_feedback"] = ""


# --- AŞAMA 1: TANIŞMA VE DİL SEÇİMİ ---
if st.session_state["stage"] == "welcome":
  st.title("🎓 LingoFlow Pro - JSON Destekli Dil Akademisi")
  st.markdown(
      "10 soruluk kapsamlı analiz sınavımızla dil seviyenizi ve öğrenme"
      " profilinizi belirliyor; JSON tabanlı özelleştirilmiş müfredatınızı"
      " yüklüyoruz. Her cevap anında yapay zeka tarafından değerlendirilir."
  )

  col1, col2 = st.columns(2)
  with col1:
    name_input = st.text_input("Size nasıl hitap edelim?", placeholder="Adınız")
  with col2:
    lang_input = st.selectbox(
        "Hangi dili öğrenmek istiyorsun?",
        ["İngilizce (English)", "Almanca (Deutsch)", "İspanyolca (Español)"],
    )

  if st.button("🚀 Analiz Sınavını Başlat", type="primary"):
    if name_input.strip():
      st.session_state["user_name"] = name_input
      st.session_state["target_lang"] = lang_input
      st.session_state["stage"] = "placement"
      st.session_state["placement_step"] = 1
      st.rerun()
    else:
      st.error("Lütfen devam etmek için adınızı girin.")

# --- AŞAMA 2: 10 SORULUK ADIM ADIM SEVİYE VE KİŞİLİK ANALİZİ ---
elif st.session_state["stage"] == "placement":
  step = st.session_state["placement_step"]
  st.title(
      f"🎯 {st.session_state['user_name']} - Seviye ve Kişilik Analiz Sınavı"
  )
  st.progress(
      step / 10, text=f"Analiz İlerlemesi: Soru {step} / 10 (JSON Entegreli)"
  )

  question_data = {
      1: {
          "q": "1. Kendinizi en rahat nasıl tanıtırsınız? (Dil Bilgisi ve Temel İfade)",
          "options": [
              "A) I am student / My name is...",
              "B) I have been working in this company for 5 years and managing projects.",
              "C) Fluently discussing complex abstract concepts and theories.",
          ],
      },
      2: {
          "q": "2. Geçmiş zamanda geçen bir olayı aktarırken hangisini tercih edersiniz?",
          "options": [
              "A) Yesterday I go to the market.",
              "B) Yesterday I went to the market and bought some groceries.",
              "C) Had I known about the traffic earlier, I would have taken another route.",
          ],
      },
      3: {
          "q": "3. İngilizce bir makale veya metin okurken yaklaşımınız nasıldır?",
          "options": [
              "A) Sadece çok temel kelimeleri anlarım, sürekli sözlük kullanırım.",
              "B) Ana fikri rahatça anlarım, detaylarda ara sıra zorlanırım.",
              "C) Akıcı bir şekilde edebi veya teknik metinleri zorlanmadan okurum.",
          ],
      },
      4: {
          "q": "4. İngilizce konuşurken veya yazarken en çok zorlandığınız alan nedir?",
          "options": [
              "A) Cümle kurmakta çekiniyorum ve kelime dağarcığım çok az.",
              "B) Zamanlar (tenses) ve akıcı bağlaçlar konusunda hatalar yapabiliyorum.",
              "C) Hiçbir temel zorluğum yok, sadece daha doğal ve sofistike olmak istiyorum.",
          ],
      },
      5: {
          "q": "5. Karmaşık bir soruya hedef dilde yanıt vermeniz gerektiğinde tepkiniz ne olur?",
          "options": [
              "A) Çok kısa ve basit kelimelerle yanıt vermeye çalışırım.",
              "B) Düşüncelerimi ifade edebilirim ancak ifade çeşitliliğim sınırlıdır.",
              "C) Anında zengin kelime dağarcığıyla profesyonelce açıklama yaparım.",
          ],
      },
      6: {
          "q": "6. Bilgi öğrenirken veya problem çözerken hangi yöntemi daha çok seversiniz?",
          "options": [
              "A) Adım adım kuralların ezberlenmesi ve net talimatlar.",
              "B) Gerçek hayat senaryoları ve hikaye tabanlı pratikler.",
              "C) Analitik veriler, istatistikler ve stratejik vakalar.",
          ],
      },
      7: {
          "q": "7. Günlük rutininizde yeni bir şey öğrenmeye ortalama ne kadar süre ayırabilirsiniz?",
          "options": [
              "A) Kısa ve yoğun seanslar (5-10 dakika).",
              "B) Orta vadeli derinlemesine seanslar (15-20 dakika).",
              "C) Uzun ve kapsamlı akademik oturumlar (30+ dakika).",
          ],
      },
      8: {
          "q": "8. Motivasyonunuzu en çok ne artırır?",
          "options": [
              "A) Başarı rozetleri kazanmak ve küçük hedeflere ulaşmak.",
              "B) Kendimi bir hikayenin başrolünde hissetmek ve hayallerime yaklaşmak.",
              "C) Profesyonel sertifikalar almak ve kariyerimde somut ilerleme görmek.",
          ],
      },
      9: {
          "q": "9. Hata yaptığınızda geri bildirim alma tarzınız nasıl olmalıdır?",
          "options": [
              "A) Çok yumuşak ve Türkçe açıklamalı destek.",
              "B) Yapıcı eleştiri ve doğru alternatif cümle gösterimi.",
              "C) Doğrudan hedef dilde profesyonel düzeltme ve ileri düzey uyarı.",
          ],
      },
      10: {
          "q": "10. Bu dili öğrenmenizdeki en baskın nihai psikolojik itki nedir?",
          "options": [
              "A) Özgüven eksikliğini yenmek ve dünyayla iletişim kurabilmek.",
              "B) Hayalini kurduğum yaşamı (seyahat, yerleşim vb.) gerçeğe dönüştürmek.",
              "C) Kariyer basamaklarını hızla tırmanmak ve küresel projelerde lider olmak.",
          ],
      },
  }

  current_q = question_data[step]

  st.markdown(f"### {current_q['q']}")
  st.caption("Lütfen size en uygun seçeneği işaretleyin.")

  ans_key = f"q_{step}"
  selected_ans = st.radio(
      "Seçenekler:",
      current_q["options"],
      index=None,
      key=ans_key,
      label_visibility="collapsed",
  )

  st.markdown("<br>", unsafe_allow_html=True)

  col1, col2 = st.columns([1, 1])
  with col1:
    if step > 1:
      if st.button("⬅️ Önceki Soru"):
        st.session_state["placement_step"] -= 1
        st.rerun()
  with col2:
    if step < 10:
      if st.button("Sonraki Soru ➡️", type="primary"):
        if selected_ans is not None:
          st.session_state["placement_answers"][step] = selected_ans
          st.session_state["placement_step"] += 1
          st.rerun()
        else:
          st.warning("Lütfen ilerlemek için bir seçenek işaretleyin.")
    else:
      if st.button(
          "Analizi Tamamla ve JSON Müfredatımı Yükle 🎯", type="primary"
      ):
        if selected_ans is not None:
          st.session_state["placement_answers"][step] = selected_ans

          answers_summary = "\n".join(
              f"Soru {k}: {v}"
              for k, v in st.session_state["placement_answers"].items()
          )

          analysis_prompt = (
              "Analyze the following 10 placement and personality test answers"
              " for a language learner. Determine their exact CEFR level (A1,"
              " A2, B1, or B2) and summarize their psychological/learning"
              " personality profile. Provide the output in Turkish in this"
              " exact format:\nSEVIYE: [Level]\nPROFIL: [Profile"
              " description]\n\nAnswers:\n" + answers_summary
          )

          try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
            )
            analysis_text = res.choices[0].message.content

            detected_lvl = "A1"
            detected_profile = "Genel öğrenme profili"
            for line in analysis_text.split("\n"):
              if "SEVIYE:" in line:
                detected_lvl = (
                    line.replace("SEVIYE:", "").strip().upper()[:2]
                )
              if "PROFIL:" in line:
                detected_profile = line.replace("PROFIL:", "").strip()

            if detected_lvl not in ["A1", "A2", "B1", "B2"]:
              detected_lvl = "A1"

            st.session_state["current_level"] = detected_lvl
            st.session_state["personality_profile"] = detected_profile
          except Exception:
            st.session_state["current_level"] = "A1"
            st.session_state["personality_profile"] = (
                "Hikaye tabanlı dinamik öğrenici"
            )

          st.session_state["stage"] = "goal_setup"
          st.rerun()
        else:
          st.warning("Lütfen son soruyu da yanıtlayın.")

# --- AŞAMA 3: HİKAYE, HEDEF VE SEVİYE DÜZELTME (OVERRIDE) ---
elif st.session_state["stage"] == "goal_setup":
  st.title(f"🌟 {st.session_state['user_name']}, Kişisel Hedefini Tanımla")
  st.success(
      f"🔍 **JSON Analiz Sonucu:** Seviyeniz **{st.session_state['current_level']}**"
      f" | Profil: *{st.session_state['personality_profile']}*"
  )

  st.markdown(
      "💡 *Not: Analiz sonucunda belirlenen seviyeyi dilediğiniz gibi"
      " değiştirebilir; seçtiğiniz seviyeye uygun JSON müfredatının"
      " yüklenmesini sağlayabilirsiniz.*"
  )

  with st.form("story_goal_form"):
    level_options = ["A1", "A2", "B1", "B2"]
    current_lvl_idx = (
        level_options.index(st.session_state["current_level"])
        if st.session_state["current_level"] in level_options
        else 0
    )

    selected_level_override = st.selectbox(
        "Eğitim Seviyenizi Onaylayın / Değiştirin:",
        level_options,
        index=current_lvl_idx,
    )

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

    goal_submitted = st.form_submit_button(
        "JSON Müfredatımı Aktive Et ve Başla 🚀"
    )
    if goal_submitted:
      st.session_state["current_level"] = selected_level_override
      st.session_state["user_goal"] = goal_choice
      st.session_state["user_dream"] = (
          dream_input if dream_input.strip() else "Kendi başarı hikayesini yazmak"
      )

      # JSON veritabanından seçilen seviyenin modüllerini çek ve ata
      lvl = st.session_state["current_level"]
      st.session_state["modules"] = list(CURRICULUM_DATA.get(lvl, CURRICULUM_DATA["A1"]))

      st.session_state["stage"] = "dashboard"
      st.rerun()

# --- AŞAMA 4: DAHİLİ KURS PANELI (DASHBOARD) ---
elif st.session_state["stage"] == "dashboard":
  st.title(f"🗺️ {st.session_state['user_name']} - JSON Müfredat Paneli")
  st.success(
      f"🎯 **Aktif Seviye:** {st.session_state['current_level']} | 🎯"
      f" **Hedef:** {st.session_state['user_goal']}"
  )

  st.markdown("### 📚 JSON Dosyasından Yüklenen Yoğun Eğitim Modülleriniz")

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
        btn_txt = "Derse Başla 📖" if mod["status"] == "Açık" else "Tekrar Et 🔄"
        if st.button(btn_txt, key=f"mod_btn_{idx}", type="primary"):
          st.session_state["current_module_idx"] = idx
          st.session_state["lesson_step"] = 1
          st.session_state["quiz_feedback"] = ""
          st.session_state["writing_feedback"] = ""
          for key in [
              "reading_content",
              "vocab_content",
              "quiz_content",
          ]:
            if key in st.session_state:
              del st.session_state[key]
          st.session_state["stage"] = "learning"
          st.rerun()
      else:
        st.info("🔒 Kilitli")
    st.markdown("---")

# --- AŞAMA 5: KAPSAMLI DERS İŞLEYİŞİ (LEARNING STAGE) ---
elif st.session_state["stage"] == "learning":
  mod_idx = st.session_state["current_module_idx"]
  active_mod = st.session_state["modules"][mod_idx]
  step = st.session_state["lesson_step"]

  st.title(f"📖 {active_mod['title']}")
  st.progress(
      step / 4,
      text=(
          f"Eğitim İlerlemesi: Adım {step} / 4 ("
          "1:Okuma->2:Kelime/Kalıp->3:Test ve Anlık Değerlendirme->4:Yazma ve"
          " Hata Düzeltme)"
      ),
  )

  # --- ADIM 1: ZENGİN OKUMA VE HİKAYE METNİ ---
  if step == 1:
    st.subheader("📜 1. Bölüm: Bağlamsal Okuma ve Hikaye Analizi")
    st.markdown(
        "JSON modül içeriğine ve kişisel profilinize uygun hazırlanmış ders"
        " metni:"
    )

    if "reading_content" not in st.session_state:
      prompt_read = (
          f"Create a rich, professional, 2-paragraph educational reading"
          f" passage in {st.session_state['target_lang']} for level"
          f" {st.session_state['current_level']} titled '{active_mod['title']}',"
          f" tailored to user profile: '{st.session_state['personality_profile']}'"
          f" and dream: '{st.session_state['user_dream']}'."
          " Include a clear Turkish summary/translation right below it."
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
        "Bu modülde ustalaşmanız gereken temel yapı taşları ve kalıplar:"
    )

    if "vocab_content" not in st.session_state:
      prompt_vocab = (
          f"List 5 essential vocabulary words and 3 key sentence patterns from"
          f" module '{active_mod['title']}' for"
          f" {st.session_state['target_lang']} at level"
          f" {st.session_state['current_level']}. Explain meanings and"
          " usages in Turkish with examples."
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

  # --- ADIM 3: İNTERAKTİF TEST VE ANLIK DEĞERLENDİRME ---
  elif step == 3:
    st.subheader(
        "🧩 3. Bölüm: Bilgiyi Pekiştirme ve Anlık Yapay Zeka Değerlendirmesi"
    )
    st.markdown(
        "Modül kazanımlarını test edin, cevaplarınız anında değerlendirilsin."
    )

    if "quiz_content" not in st.session_state:
      prompt_quiz = (
          f"Create 2 high-quality multiple choice or fill-in-the-blank"
          f" educational exercises related to '{active_mod['title']}' in"
          f" {st.session_state['target_lang']} for level"
          f" {st.session_state['current_level']}. Provide helpful hints in"
          " Turkish, 4 options (A, B, C, D) per question, and explicitly"
          " include 'Dogru Cevaplar: ...' at the very end."
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

    if st.button("Cevaplarımı Değerlendir ve Hataları Düzelt 🔍"):
      if user_ans_q3.strip():
        eval_prompt = (
            f"Evaluate the user's quiz answers: '{user_ans_q3}' against the"
            f" following quiz content:\n{st.session_state['quiz_content']}\nProvide"
            " a clear, encouraging evaluation in Turkish. Point out which ones"
            " are correct, which ones are incorrect, explain why, and provide"
            " corrections for any mistakes."
        )
        try:
          res = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              messages=[{"role": "user", "content": eval_prompt}],
              temperature=0.3,
          )
          st.session_state["quiz_feedback"] = res.choices[0].message.content
        except Exception:
          st.session_state["quiz_feedback"] = (
              "Değerlendirme yapılırken hata oluştu."
          )
      else:
        st.warning("Lütfen değerlendirilmesi için cevaplarınızı yazın.")

    if st.session_state["quiz_feedback"]:
      st.info(st.session_state["quiz_feedback"])

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
          st.warning("Lütfen test cevaplarınızı giriniz.")

  # --- ADIM 4: YAZMA VE ANLIK DÜZELTME PRATİĞİ ---
  elif step == 4:
    st.subheader(
        "✍️ 4. Bölüm: Aktif Yazma ve Anlık Yapay Zeka Hata Düzeltme"
    )
    st.markdown(
        f"Bu modülde öğrendiğiniz kelime ve kalıplarla, hayalinize ('"
        f"{st.session_state['user_dream']}') atıfta bulunan en az 2 cümlelik"
        " kendi cümlenizi yazın. Yazdığınız metin anında taranıp düzeltilecektir:"
    )

    user_writing = st.text_area(
        "Cümlelerinizi buraya yazın:",
        placeholder=(
            "Örn: In order to reach my dream, I practice every day..."
        ),
        key="writing_input_field",
    )

    if st.button("Yazımı Değerlendir ve Eksikleri Düzelt 🔍"):
      if user_writing.strip():
        write_eval_prompt = (
            f"Evaluate the following user-written text in"
            f" {st.session_state['target_lang']}: '{user_writing}'. Provide"
            " constructive feedback in Turkish, point out grammatical, spelling,"
            " or vocabulary errors, explain missing points, and provide fully"
            " corrected/improved professional versions of the sentences."
        )
        try:
          res = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              messages=[{"role": "user", "content": write_eval_prompt}],
              temperature=0.3,
          )
          st.session_state["writing_feedback"] = res.choices[0].message.content
        except Exception:
          st.session_state["writing_feedback"] = "Yazı değerlendirilemedi."
      else:
        st.warning("Lütfen değerlendirilecek bir metin yazın.")

    if st.session_state["writing_feedback"]:
      st.success(st.session_state["writing_feedback"])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Dersi Tamamla ve Bölüm Karnesini Gör 🏆", type="primary"):
      if user_writing.strip():
        st.session_state["current_report"] = {
            "module_title": active_mod["title"],
            "learned_words": active_mod["words"],
            "user_text": user_writing,
            "status": "Başarıyla Tamamlandı",
        }

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
        <h3 style="color: #1b5e20; text-align: center;">📚 LingoFlow Pro JSON Eğitim Karnesi</h3>
        <hr>
        <p><b>Öğrenci Adı:</b> {st.session_state['user_name']}</p>
        <p><b>Hedef Dil / Seviye / Profil:</b> {st.session_state['target_lang']} ({st.session_state['current_level']}) - {st.session_state['personality_profile']}</p>
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
            Harika bir çalışma çıkardınız! JSON tabanlı modül başarıyla işlendi.
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  col1, col2 = st.columns(2)
  with col1:
    if st.button("🗺️ Müfredat Paneline Geri Dön", type="primary"):
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
        <p>tarafından <b>{st.session_state['target_lang']}</b> dilinde tamamlanan program sonucunda,</p>
        <h3><b>{st.session_state['current_level']} Seviyesi JSON Müfredat Serisi</b>ni</h3>
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
