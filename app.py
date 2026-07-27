from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="LingoFlow Groq - AI Language Assistant",
    page_icon="⚡",
    layout="centered",
)

# Groq API Anahtarı Yönetimi
api_key = st.secrets.get("GROQ_API_KEY") or st.sidebar.text_input(
    "Groq API Key", type="password"
)

if not api_key:
    st.warning("Lütfen devam etmek için geçerli bir Groq API Anahtarı girin.")
    st.stop()

client = Groq(api_key=api_key)

# Arayüz ve Sohbet Yönetimi
st.title("⚡ LingoFlow - Groq Destekli Dil Asistanı")
st.caption(
    "Hızlı ve kesintisiz yanıtlar için Llama 3 altyapısıyla güçlendirilmiştir."
)

if "messages" not in st.session_state:
  st.session_state["messages"] = [{
      "role": "system",
      "content": (
          "You are an advanced, encouraging AI language tutor. Help the user"
          " practice languages, correct grammar, and explain rules warmly."
      ),
  }, {
      "role": "assistant",
      "content": (
          "Merhaba! Groq altyapısına geçtik. Artık hiçbir kota sınırlaması"
          " ve gecikme yaşamadan hızlıca dil pratiği yapabiliriz. Bugün ne"
          " çalışmak istersiniz?"
      ),
  }]

for message in st.session_state["messages"]:
  if message["role"] != "system":
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

if user_input := st.chat_input("Mesajınızı buraya yazın..."):
  st.session_state["messages"].append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  try:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state["messages"]
        ],
        temperature=0.7,
    )
    assistant_reply = completion.choices[0].message.content
  except Exception as e:
    assistant_reply = f"Bir hata oluştu: {e}"

  st.session_state["messages"].append(
      {"role": "assistant", "content": assistant_reply}
  )
  with st.chat_message("assistant"):
    st.markdown(assistant_reply)
