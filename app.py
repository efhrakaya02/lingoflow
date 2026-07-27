import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="İnteraktif Dil Akademisi",
    page_icon="🎓",
    layout="wide"
)

# Oturum Durumu (Session State) Tanımlamaları
if "unlocked_modules" not in st.session_state:
    st.session_state.unlocked_modules = ["Bölüm 1: Temel Dil Bilgisi"]
if "test_completed" not in st.session_state:
    st.session_state.test_completed = False
if "last_score" not in st.session_state:
    st.session_state.last_score = 0

st.title("🎓 İnteraktif Dil Akademisi & Kazanım Değerlendirme Sistemi")

# Sekmeler
tab1, tab2, tab3 = st.tabs(["📚 Müfredat", "📝 Kazanım Tekrar Testi", "📊 İlerleme ve Raporlar"])

with tab1:
    st.header("Eğitim Müfredatı")
    
    st.subheader("Bölüm 1: Temel Dil Bilgisi ve Kelime Dağarcığı")
    st.write("Günlük iletişim kalıpları ve temel gramer yapıları.")
    st.success("🔓 Durum: Erişilebilir")

    st.markdown("---")
    
    st.subheader("Bölüm 2: İleri Düzey Yapılar ve Akıcı İletişim")
    st.write("CEFR/KET standartlarına uygun ileri seviye modül.")
    
    # Kilit Kontrolü
    if "Bölüm 2: İleri Düzey Yapılar ve Akıcı İletişim" in st.session_state.unlocked_modules:
        st.success("🔓 **Durum: Kilidi Açıldı!** Bu modüle erişebilirsiniz.")
    else:
        st.warning("🔒 **Durum: Kilitli.** Bu modülü açmak için 'Kazanım Tekrar Testi'ni başarıyla tamamlamalısınız.")

with tab2:
    st.header("📝 Kazanım Tekrar Testi")
    st.write("Bölüm sonu kazanımlarınızı test edin, değerlendirme raporunuzu alın ve sonraki bölümün kilidini açın.")

    with st.form("kazanim_test_form"):
        st.markdown("### Soru 1: Gramer ve Yapı")
        q1 = st.radio(
            "Aşağıdaki seçeneklerden hangisi 'She has been living here for five years' cümlesinin doğru anlamını verir?",
            (
                "A) Beş yıldır burada yaşıyor ve hala yaşamaya devam ediyor.",
                "B) Beş yıl önce burada yaşayıp taşındı.",
                "C) Gelecek beş yıl burada yaşayacak.",
                "D) Hiç burada yaşamadı."
            ),
            key="form_q1"
        )

        st.markdown("### Soru 2: Kelime Bilgisi")
        q2 = st.text_input("'Geliştirmek, ilerletmek' anlamına gelen İngilizce fiili yazınız:", key="form_q2")

        st.markdown("### Soru 3: Cümle Tamamlama")
        q3 = st.selectbox(
            "If I had more time, I _____ a new project.",
            ("will start", "would start", "started", "had started"),
            key="form_q3"
        )

        # Değerlendir ve Kilidi Aç Butonu
        submitted = st.form_submit_button("Değerlendir ve Kilidi Aç", type="primary")

    # Form Gönderildiğinde İşlenen Mantık
    if submitted:
        with st.spinner("Test sonuçlarınız analiz ediliyor ve değerlendirme raporu hazırlanıyor..."):
            
            # Otomatik Puan Hesaplama
            score = 0
            correct_answers = {
                "q1": "A) Beş yıldır burada yaşıyor ve hala yaşamaya devam ediyor.",
                "q2": "improve",
                "q3": "would start"
            }

            if q1 == correct_answers["q1"]:
                score += 35
            if q2.strip().lower() in ["improve", "improves"]:
                score += 35
            if q3 == correct_answers["q3"]:
                score += 30

            passing_threshold = 70  # %70 başarı barajı
            passed = score >= passing_threshold

            st.session_state.test_completed = True
            st.session_state.last_score = score

            # 1. Değerlendirme Raporunun Sunulması
            st.markdown("---")
            st.markdown("### 📊 Değerlendirme Raporu")
            st.metric(label="Genel Başarı Puanı", value=f"{score}/100")

            st.markdown("""
            * **Kelime Bilgisi ve Yapı (Lexical Resource):** Başarılı
            * **Gramer ve Cümle Kurulumu (Grammatical Accuracy):** Yeterli düzeyde
            * **Akıcılık ve Anlama (Comprehension):** Tamamlandı
            """)

            # 2. Kilit Mekanizması ve Uyarı Kontrolü
            if passed:
                next_module = "Bölüm 2: İleri Düzey Yapılar ve Akıcı İletişim"
                if next_module not in st.session_state.unlocked_modules:
                    st.session_state.unlocked_modules.append(next_module)
                
                st.balloons()
                st.success("Tebrikler! Kazanım tekrar testini başarıyla tamamladınız.")
                st.info(f"🔓 **Sonraki Bölüm Kilidi Açıldı:** '{next_module}' modülüne artık erişebilirsiniz!")
                
            else:
                st.warning(f"⚠️ %{passing_threshold} başarı barajının altında kaldınız (Mevcut Skor: {score}). Lütfen eksik kazanımları gözden geçirip testi tekrar deneyin.")
                st.info("🔒 Sonraki bölümün kilidi henüz açılmadı.")

    # Test daha önceden tamamlandıysa kalıcı raporu gösterme
    elif st.session_state.get("test_completed", False):
        st.markdown("---")
        st.markdown("### 📊 Değerlendirme Raporu (Önceki Deneme)")
        saved_score = st.session_state.get("last_score", 0)
        st.write(f"Son Skorunuz: {saved_score}/100")
        
        if saved_score >= 70:
            st.success("✅ Bu bölüm başarıyla tamamlandı ve sonraki bölümün kilidi açık.")
        else:
            st.warning("⚠️ Test başarı barajının altında kalmıştı. Tekrar deneyebilirsiniz.")

with tab3:
    st.header("📊 İlerleme Durumu ve Modüller")
    st.write("Erişime Açık Olan Modülleriniz:")
    for mod in st.session_state.unlocked_modules:
        st.write(f"- 🟢 {mod}")
        
    st.markdown("---")
    st.caption("Dil Akademisi Modülü - Kilitli İlerleme Altyapısı Aktif.")
