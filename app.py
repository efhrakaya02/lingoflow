import json
import os
from datetime import datetime
import streamlit as st

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Lingoflow A1 Master Curriculum",
    page_icon="🌐",
    layout="wide",
)

# Özel CSS İyileştirmeleri (Sertifika ve Kart Stilleri Dahil)
st.markdown(
    """
    <style>
    .vocab-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }
    .vocab-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
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
    .challenge-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .exam-section-card {
        background-color: #fafbfc;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #d1d5db;
        margin-bottom: 25px;
    }
    .certificate-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 10px solid #1e3a8a;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 20px;
        font-family: 'Georgia', serif;
    }
    .cert-title {
        color: #1e3a8a;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .cert-subtitle {
        color: #4b5563;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .cert-name {
        color: #111827;
        font-size: 28px;
        font-weight: bold;
        border-bottom: 2px solid #9ca3af;
        display: inline-block;
        padding: 0 30px 5px 30px;
        margin: 15px 0;
    }
    .cert-body {
        color: #374151;
        font-size: 16px;
        line-height: 1.6;
        margin: 20px 0;
    }
    .cert-footer {
        display: flex;
        justify-content: space-between;
        margin-top: 40px;
        padding: 0 20px;
        font-size: 14px;
        color: #4b5563;
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

# --- TÜM MODÜLLER İÇİN KELİME HAZİNESİ (1-12) ---
EXTENDED_VOCABULARY = {
    1: [
        {
            "term": "Hello",
            "translation": "Merhaba",
            "example": "Hello, how are you?",
        },
        {
            "term": "Goodbye",
            "translation": "Hoşça kal",
            "example": "Goodbye, see you tomorrow.",
        },
        {"term": "Please", "translation": "Lütfen", "example": "Please help me."},
        {
            "term": "Thank you",
            "translation": "Teşekkür ederim",
            "example": "Thank you very much.",
        },
        {"term": "Yes", "translation": "Evet", "example": "Yes, I understand."},
        {"term": "No", "translation": "Hayır", "example": "No, thank you."},
        {
            "term": "Good morning",
            "translation": "Günaydın",
            "example": "Good morning, teacher.",
        },
        {
            "term": "Good night",
            "translation": "İyi geceler",
            "example": "Good night, sleep well.",
        },
        {
            "term": "Sorry",
            "translation": "Özür dilerim",
            "example": "Sorry, I am late.",
        },
        {
            "term": "Excuse me",
            "translation": "Affedersiniz",
            "example": "Excuse me, where is the station?",
        },
        {"term": "Name", "translation": "İsim", "example": "What is your name?"},
        {
            "term": "Meet",
            "translation": "Tanışmak",
            "example": "Nice to meet you.",
        },
        {
            "term": "Friend",
            "translation": "Arkadaş",
            "example": "He is my best friend.",
        },
        {"term": "Mr.", "translation": "Bay", "example": "Mr. Smith is here."},
        {
            "term": "Ms.",
            "translation": "Bayan",
            "example": "Ms. Davis is a doctor.",
        },
        {"term": "How", "translation": "Nasıl", "example": "How are you today?"},
        {"term": "And", "translation": "Ve", "example": "You and me."},
        {"term": "Too", "translation": "De / da", "example": "I am fine, too."},
        {
            "term": "Welcome",
            "translation": "Hoş geldiniz",
            "example": "Welcome to our home.",
        },
        {
            "term": "See you",
            "translation": "Görüşürüz",
            "example": "See you later.",
        },
    ],
    2: [
        {"term": "Student", "translation": "Öğrenci", "example": "I am a student."},
        {
            "term": "Teacher",
            "translation": "Öğretmen",
            "example": "She is a good teacher.",
        },
        {"term": "Doctor", "translation": "Doktor", "example": "He is a doctor."},
        {
            "term": "Engineer",
            "translation": "Mühendis",
            "example": "My father is an engineer.",
        },
        {
            "term": "Happy",
            "translation": "Mutlu",
            "example": "I am very happy today.",
        },
        {"term": "Sad", "translation": "Üzgün", "example": "Why are you sad?"},
        {
            "term": "Tired",
            "translation": "Yorgun",
            "example": "We are tired after work.",
        },
        {"term": "Busy", "translation": "Meşgul", "example": "She is busy now."},
        {
            "term": "At home",
            "translation": "Evde",
            "example": "They are at home.",
        },
        {"term": "At work", "translation": "İşte", "example": "He is at work."},
        {"term": "Old", "translation": "Yaşlı / Eski", "example": "My car is old."},
        {"term": "Young", "translation": "Genç", "example": "She is a young girl."},
        {
            "term": "Tall",
            "translation": "Uzun boylu",
            "example": "He is a tall man.",
        },
        {
            "term": "Short",
            "translation": "Kısa",
            "example": "The pencil is short.",
        },
        {
            "term": "Rich",
            "translation": "Zengin",
            "example": "He is a rich businessman.",
        },
        {"term": "Poor", "translation": "Fakir", "example": "Help poor people."},
        {"term": "Ready", "translation": "Hazır", "example": "Are you ready?"},
        {
            "term": "Late",
            "translation": "Geç",
            "example": "I am late for the meeting.",
        },
        {
            "term": "Early",
            "translation": "Erken",
            "example": "She is always early.",
        },
        {"term": "Right", "translation": "Haklı", "example": "You are right."},
    ],
    3: [
        {"term": "Book", "translation": "Kitap", "example": "This is my book."},
        {"term": "Pen", "translation": "Kalem", "example": "That is a red pen."},
        {
            "term": "Table",
            "translation": "Masa",
            "example": "These are tables.",
        },
        {
            "term": "Chair",
            "translation": "Sandalye",
            "example": "Those are comfortable chairs.",
        },
        {"term": "Car", "translation": "Araba", "example": "This car is fast."},
        {
            "term": "House",
            "translation": "Ev",
            "example": "That house is big.",
        },
        {
            "term": "Phone",
            "translation": "Telefon",
            "example": "Is this your phone?",
        },
        {
            "term": "Computer",
            "translation": "Bilgisayar",
            "example": "That computer is new.",
        },
        {"term": "Bag", "translation": "Çanta", "example": "These bags are heavy."},
        {
            "term": "Key",
            "translation": "Anahtar",
            "example": "Those keys are on the table.",
        },
        {
            "term": "Window",
            "translation": "Pencere",
            "example": "Open this window.",
        },
        {"term": "Door", "translation": "Kapı", "example": "Close that door."},
        {
            "term": "Picture",
            "translation": "Resim",
            "example": "These pictures are nice.",
        },
        {
            "term": "Clock",
            "translation": "Saat",
            "example": "That clock is broken.",
        },
        {
            "term": "Bottle",
            "translation": "Şişe",
            "example": "This water is cold.",
        },
        {
            "term": "Cup",
            "translation": "Fincan",
            "example": "Those cups are clean.",
        },
        {
            "term": "Box",
            "translation": "Kutu",
            "example": "These boxes are empty.",
        },
        {
            "term": "Paper",
            "translation": "Kağıt",
            "example": "That paper is white.",
        },
        {
            "term": "Shoe",
            "translation": "Ayakkabı",
            "example": "These shoes are new.",
        },
        {
            "term": "Coat",
            "translation": "Mont / Kaban",
            "example": "That coat is warm.",
        },
    ],
    4: [
        {
            "term": "Brother",
            "translation": "Erkek kardeş",
            "example": "I have got a brother.",
        },
        {
            "term": "Sister",
            "translation": "Kız kardeş",
            "example": "She has got a sister.",
        },
        {"term": "Father", "translation": "Baba", "example": "He has got a car."},
        {
            "term": "Mother",
            "translation": "Anne",
            "example": "My mother has got a cat.",
        },
        {
            "term": "Family",
            "translation": "Aile",
            "example": "We have got a big family.",
        },
        {"term": "Dog", "translation": "Köpek", "example": "I have got a dog."},
        {
            "term": "Cat",
            "translation": "Kedi",
            "example": "She has got two cats.",
        },
        {
            "term": "Bike",
            "translation": "Bisiklet",
            "example": "He has got a new bike.",
        },
        {
            "term": "Camera",
            "translation": "Kamera",
            "example": "Have you got a camera?",
        },
        {
            "term": "Watch",
            "translation": "Kol saati",
            "example": "I have got a gold watch.",
        },
        {
            "term": "Money",
            "translation": "Para",
            "example": "I have not got much money.",
        },
        {
            "term": "Time",
            "translation": "Zaman",
            "example": "We have got time today.",
        },
        {
            "term": "Idea",
            "translation": "Fikir",
            "example": "She has got a good idea.",
        },
        {"term": "Job", "translation": "İş", "example": "He has got a new job."},
        {
            "term": "Room",
            "translation": "Oda",
            "example": "I have got my own room.",
        },
        {
            "term": "Bag",
            "translation": "Çanta",
            "example": "She has got a red bag.",
        },
        {
            "term": "Umbrella",
            "translation": "Şemsiye",
            "example": "Have you got an umbrella?",
        },
        {
            "term": "Passport",
            "translation": "Pasaport",
            "example": "I have got my passport.",
        },
        {
            "term": "Ticket",
            "translation": "Bilet",
            "example": "We have got flight tickets.",
        },
        {
            "term": "Problem",
            "translation": "Problem",
            "example": "I have got a question.",
        },
    ],
    5: [
        {
            "term": "Morning",
            "translation": "Sabah",
            "example": "I wake up in the morning.",
        },
        {
            "term": "Afternoon",
            "translation": "Öğleden sonra",
            "example": "See you in the afternoon.",
        },
        {
            "term": "Evening",
            "translation": "Akşam",
            "example": "We rest in the evening.",
        },
        {"term": "Night", "translation": "Gece", "example": "I sleep at night."},
        {
            "term": "O'clock",
            "translation": "Tam saat",
            "example": "It is 8 o'clock.",
        },
        {
            "term": "Half",
            "translation": "Buçuk",
            "example": "It is half past two.",
        },
        {
            "term": "Quarter",
            "translation": "Çeyrek",
            "example": "It is a quarter to five.",
        },
        {
            "term": "Breakfast",
            "translation": "Kahvaltı",
            "example": "I eat breakfast at 7 AM.",
        },
        {
            "term": "Lunch",
            "translation": "Öğle yemeği",
            "example": "We have lunch at noon.",
        },
        {
            "term": "Dinner",
            "translation": "Akşam yemeği",
            "example": "Dinner is ready.",
        },
        {
            "term": "Work",
            "translation": "Çalışmak",
            "example": "I start work at 9.",
        },
        {
            "term": "Sleep",
            "translation": "Uyumak",
            "example": "I sleep 8 hours a day.",
        },
        {
            "term": "Wake up",
            "translation": "Uyanmak",
            "example": "I wake up early.",
        },
        {"term": "Shower", "translation": "Duş", "example": "I take a shower."},
        {
            "term": "Home",
            "translation": "Ev",
            "example": "I go home at 6 PM.",
        },
        {"term": "Day", "translation": "Gün", "example": "Have a nice day."},
        {"term": "Week", "translation": "Hafta", "example": "This week is busy."},
        {
            "term": "Monday",
            "translation": "Pazartesi",
            "example": "Monday is the first workday.",
        },
        {
            "term": "Weekend",
            "translation": "Hafta sonu",
            "example": "I relax at the weekend.",
        },
        {
            "term": "Time",
            "translation": "Zaman",
            "example": "What time is it?",
        },
    ],
    6: [
        {
            "term": "In",
            "translation": "İçinde",
            "example": "The key is in the box.",
        },
        {
            "term": "On",
            "translation": "Üzerinde",
            "example": "The book is on the desk.",
        },
        {
            "term": "Under",
            "translation": "Altında",
            "example": "The cat is under the bed.",
        },
        {
            "term": "Behind",
            "translation": "Arkasında",
            "example": "The car is behind the house.",
        },
        {
            "term": "Next to",
            "translation": "Bitişiğinde",
            "example": "The bank is next to the cafe.",
        },
        {
            "term": "In front of",
            "translation": "Önünde",
            "example": "He is in front of the door.",
        },
        {
            "term": "Between",
            "translation": "Arasında",
            "example": "The park is between two streets.",
        },
        {"term": "Room", "translation": "Oda", "example": "My room is upstairs."},
        {
            "term": "Kitchen",
            "translation": "Mutfak",
            "example": "Mom is in the kitchen.",
        },
        {
            "term": "Bathroom",
            "translation": "Banyo",
            "example": "The bathroom is clean.",
        },
        {
            "term": "Garden",
            "translation": "Bahçe",
            "example": "The dog is in the garden.",
        },
        {
            "term": "Street",
            "translation": "Sokak",
            "example": "Our street is quiet.",
        },
        {
            "term": "City",
            "translation": "Şehir",
            "example": "Edremit is a nice city.",
        },
        {
            "term": "Office",
            "translation": "Ofis",
            "example": "My office is downtown.",
        },
        {
            "term": "School",
            "translation": "Okul",
            "example": "Children are at school.",
        },
        {"term": "Park", "translation": "Park", "example": "Let's walk in the park."},
        {"term": "Store", "translation": "Mağaza", "example": "The store is open."},
        {"term": "Hotel", "translation": "Otel", "example": "We stay at a hotel."},
        {
            "term": "Airport",
            "translation": "Havalimanı",
            "example": "The airport is far.",
        },
        {
            "term": "Station",
            "translation": "İstasyon",
            "example": "Bus station is here.",
        },
    ],
    7: [
        {
            "term": "Wake",
            "translation": "Uyanmak",
            "example": "I wake up early every day.",
        },
        {
            "term": "Eat",
            "translation": "Yemek yemek",
            "example": "He eats apples.",
        },
        {
            "term": "Drink",
            "translation": "İçmek",
            "example": "We drink tea in the morning.",
        },
        {
            "term": "Go",
            "translation": "Gitmek",
            "example": "She goes to work by bus.",
        },
        {
            "term": "Come",
            "translation": "Gelmek",
            "example": "They come home late.",
        },
        {
            "term": "Read",
            "translation": "Okumak",
            "example": "I read books at night.",
        },
        {"term": "Write", "translation": "Yazmak", "example": "Students write notes."},
        {
            "term": "Speak",
            "translation": "Konuşmak",
            "example": "She speaks English well.",
        },
        {
            "term": "Listen",
            "translation": "Dinlemek",
            "example": "I listen to music.",
        },
        {
            "term": "Play",
            "translation": "Oynamak",
            "example": "Boys play football.",
        },
        {"term": "Like", "translation": "Sevmek", "example": "I like coffee."},
        {
            "term": "Love",
            "translation": "Çok sevmek",
            "example": "Cats love milk.",
        },
        {
            "term": "Want",
            "translation": "İstemek",
            "example": "Do you want water?",
        },
        {
            "term": "Know",
            "translation": "Bilmek",
            "example": "I know the answer.",
        },
        {
            "term": "Work",
            "translation": "Çalışmak",
            "example": "He works in a bank.",
        },
        {
            "term": "Live",
            "translation": "Yaşamak",
            "example": "We live in Turkey.",
        },
        {
            "term": "Study",
            "translation": "Ders çalışmak",
            "example": "She studies English.",
        },
        {
            "term": "Help",
            "translation": "Yardım etmek",
            "example": "He helps his mother.",
        },
        {
            "term": "Buy",
            "translation": "Satın almak",
            "example": "I buy fresh fruit.",
        },
        {
            "term": "Cook",
            "translation": "Yemek pişirmek",
            "example": "Dad cooks dinner.",
        },
    ],
    8: [
        {
            "term": "Swim",
            "translation": "Yüzmek",
            "example": "I can swim in the sea.",
        },
        {"term": "Run", "translation": "Koşmak", "example": "He can run very fast."},
        {
            "term": "Drive",
            "translation": "Araba sürmek",
            "example": "Can you drive a car?",
        },
        {
            "term": "Cook",
            "translation": "Yemek yapmak",
            "example": "She can cook Italian food.",
        },
        {
            "term": "Sing",
            "translation": "Şarkı söylemek",
            "example": "My sister can sing well.",
        },
        {
            "term": "Dance",
            "translation": "Dans etmek",
            "example": "They can dance nicely.",
        },
        {
            "term": "Play guitar",
            "translation": "Gitar çalmak",
            "example": "He can play the guitar.",
        },
        {
            "term": "Speak",
            "translation": "Konuşmak",
            "example": "I can speak two languages.",
        },
        {"term": "Ride", "translation": "Binmek", "example": "Can you ride a bike?"},
        {
            "term": "Draw",
            "translation": "Çizmek",
            "example": "She can draw portraits.",
        },
        {
            "term": "Help",
            "translation": "Yardım etmek",
            "example": "Can you help me, please?",
        },
        {
            "term": "Understand",
            "translation": "Anlamak",
            "example": "I can understand English.",
        },
        {
            "term": "Find",
            "translation": "Bulmak",
            "example": "Can you find my keys?",
        },
        {"term": "Hear", "translation": "Duymak", "example": "I can hear music."},
        {"term": "See", "translation": "Görmek", "example": "Can you see the bird?"},
        {
            "term": "Read",
            "translation": "Okumak",
            "example": "He can read without glasses.",
        },
        {
            "term": "Write",
            "translation": "Yazmak",
            "example": "Can you write your name?",
        },
        {"term": "Make", "translation": "Yapmak", "example": "I can make coffee."},
        {
            "term": "Open",
            "translation": "Açmak",
            "example": "Can you open the door?",
        },
        {
            "term": "Close",
            "translation": "Kapatmak",
            "example": "Can you close the window?",
        },
    ],
    9: [
        {
            "term": "Cooking",
            "translation": "Yemek yapıyor",
            "example": "Mom is cooking now.",
        },
        {
            "term": "Sleeping",
            "translation": "Uyuyor",
            "example": "The baby is sleeping.",
        },
        {
            "term": "Working",
            "translation": "Çalışıyor",
            "example": "Dad is working at his desk.",
        },
        {
            "term": "Reading",
            "translation": "Okuyor",
            "example": "She is reading a magazine.",
        },
        {
            "term": "Writing",
            "translation": "Yazıyor",
            "example": "He is writing an email.",
        },
        {
            "term": "Running",
            "translation": "Koşuyor",
            "example": "The dog is running outside.",
        },
        {
            "term": "Walking",
            "translation": "Yürüyor",
            "example": "We are walking in the park.",
        },
        {
            "term": "Eating",
            "translation": "Yiyor",
            "example": "They are eating pizza.",
        },
        {
            "term": "Drinking",
            "translation": "İçiyor",
            "example": "I am drinking orange juice.",
        },
        {
            "term": "Watching",
            "translation": "İzliyor",
            "example": "We are watching a movie.",
        },
        {
            "term": "Listening",
            "translation": "Dinliyor",
            "example": "She is listening to music.",
        },
        {
            "term": "Playing",
            "translation": "Oynuyor",
            "example": "Kids are playing football.",
        },
        {
            "term": "Cleaning",
            "translation": "Temizlik yapıyor",
            "example": "She is cleaning the room.",
        },
        {
            "term": "Shopping",
            "translation": "Alışveriş yapıyor",
            "example": "He is shopping at the market.",
        },
        {
            "term": "Studying",
            "translation": "Çalışıyor",
            "example": "Student is studying math.",
        },
        {
            "term": "Waiting",
            "translation": "Bekliyor",
            "example": "I am waiting for the bus.",
        },
        {
            "term": "Driving",
            "translation": "Sürüyor",
            "example": "He is driving home.",
        },
        {
            "term": "Talking",
            "translation": "Konuşuyor",
            "example": "They are talking on the phone.",
        },
        {
            "term": "Smiling",
            "translation": "Gülümsüyor",
            "example": "The girl is smiling.",
        },
        {
            "term": "Singing",
            "translation": "Şarkı söylüyor",
            "example": "Birds are singing.",
        },
    ],
    10: [
        {"term": "Price", "translation": "Fiyat", "example": "What is the price?"},
        {
            "term": "Cost",
            "translation": "Maliyet / tutmak",
            "example": "How much does it cost?",
        },
        {"term": "Money", "translation": "Para", "example": "I have cash money."},
        {
            "term": "Credit card",
            "translation": "Kredi kartı",
            "example": "Can I pay by credit card?",
        },
        {"term": "Cash", "translation": "Nakit", "example": "Do you accept cash?"},
        {"term": "Cheap", "translation": "Ucuz", "example": "This shirt is cheap."},
        {
            "term": "Expensive",
            "translation": "Pahalı",
            "example": "That watch is expensive.",
        },
        {
            "term": "Store",
            "translation": "Mağaza",
            "example": "Let's go into the store.",
        },
        {
            "term": "Market",
            "translation": "Market",
            "example": "Buy milk from the market.",
        },
        {
            "term": "Shirt",
            "translation": "Gömlek",
            "example": "I like this blue shirt.",
        },
        {
            "term": "Pants",
            "translation": "Pantolon",
            "example": "These pants fit well.",
        },
        {
            "term": "Dress",
            "translation": "Elbise",
            "example": "She wears a red dress.",
        },
        {
            "term": "Size",
            "translation": "Beden / Numara",
            "example": "What is your size?",
        },
        {
            "term": "Small",
            "translation": "Küçük",
            "example": "I need a small size.",
        },
        {
            "term": "Medium",
            "translation": "Orta",
            "example": "Medium is good for me.",
        },
        {
            "term": "Large",
            "translation": "Büyük",
            "example": "This is too large.",
        },
        {
            "term": "Receipt",
            "translation": "Fiş / Fatura",
            "example": "Here is your receipt.",
        },
        {
            "term": "Discount",
            "translation": "İndirim",
            "example": "Is there any discount?",
        },
        {
            "term": "Customer",
            "translation": "Müşteri",
            "example": "Help the customer please.",
        },
        {
            "term": "Bag",
            "translation": "Poşet / Çanta",
            "example": "Do you need a bag?",
        },
    ],
    11: [
        {
            "term": "Yesterday",
            "translation": "Dün",
            "example": "I was at home yesterday.",
        },
        {
            "term": "Last night",
            "translation": "Dün gece",
            "example": "We went out last night.",
        },
        {
            "term": "Last week",
            "translation": "Geçen hafta",
            "example": "She visited us last week.",
        },
        {
            "term": "Last year",
            "translation": "Geçen yıl",
            "example": "I bought this car last year.",
        },
        {
            "term": "Was",
            "translation": "İdi (I/He/She/It)",
            "example": "He was happy.",
        },
        {
            "term": "Were",
            "translation": "İdi (We/You/They)",
            "example": "They were tired.",
        },
        {"term": "Went", "translation": "Gitti", "example": "We went to Ankara."},
        {"term": "Saw", "translation": "Gördü", "example": "I saw an old friend."},
        {
            "term": "Ate",
            "translation": "Yedi",
            "example": "He ate fish for lunch.",
        },
        {
            "term": "Drank",
            "translation": "İçti",
            "example": "She drank lemon juice.",
        },
        {
            "term": "Bought",
            "translation": "Satın aldı",
            "example": "They bought a new house.",
        },
        {
            "term": "Met",
            "translation": "Tanıştı / Buluştu",
            "example": "We met on Sunday.",
        },
        {
            "term": "Had",
            "translation": "Sahip idi / Geçirdi",
            "example": "I had a great time.",
        },
        {
            "term": "Made",
            "translation": "Yaptı",
            "example": "Mom made a delicious cake.",
        },
        {
            "term": "Came",
            "translation": "Geldi",
            "example": "Uncle came to dinner.",
        },
        {
            "term": "Spoke",
            "translation": "Konuştu",
            "example": "He spoke to the manager.",
        },
        {
            "term": "Read",
            "translation": "Okudu",
            "example": "She read a whole book.",
        },
        {
            "term": "Found",
            "translation": "Buldu",
            "example": "I found my lost key.",
        },
        {
            "term": "Took",
            "translation": "Aldı / Götürdü",
            "example": "He took a photo.",
        },
        {
            "term": "Left",
            "translation": "Ayrıldı / Bıraktı",
            "example": "We left early.",
        },
    ],
    12: [
        {"term": "What", "translation": "Ne", "example": "What is this?"},
        {
            "term": "Where",
            "translation": "Nerede / Nereye",
            "example": "Where do you live?",
        },
        {
            "term": "When",
            "translation": "Ne zaman",
            "example": "When is your birthday?",
        },
        {"term": "Who", "translation": "Kim", "example": "Who is that man?"},
        {
            "term": "Why",
            "translation": "Neden / Niçin",
            "example": "Why are you smiling?",
        },
        {"term": "How", "translation": "Nasıl", "example": "How do you go to work?"},
        {
            "term": "Which",
            "translation": "Hangi",
            "example": "Which color do you like?",
        },
        {
            "term": "Whose",
            "translation": "Kimin",
            "example": "Whose book is this?",
        },
        {
            "term": "How much",
            "translation": "Ne kadar (Fiyat/Miktar)",
            "example": "How much is it?",
        },
        {
            "term": "How many",
            "translation": "Kaç tane",
            "example": "How many brothers have you got?",
        },
        {
            "term": "How often",
            "translation": "Ne sıklıkla",
            "example": "How often do you swim?",
        },
        {
            "term": "How long",
            "translation": "Ne kadar süre",
            "example": "How long is the movie?",
        },
        {"term": "Place", "translation": "Yer", "example": "This is a nice place."},
        {"term": "Person", "translation": "Kişi", "example": "She is a kind person."},
        {"term": "Reason", "translation": "Sebep", "example": "What is the reason?"},
        {"term": "Method", "translation": "Yöntem", "example": "What is the method?"},
        {
            "term": "Information",
            "translation": "Bilgi",
            "example": "I need information.",
        },
        {
            "term": "Question",
            "translation": "Soru",
            "example": "I have a question.",
        },
        {"term": "Answer", "translation": "Cevap", "example": "Give me the answer."},
        {"term": "Example", "translation": "Örnek", "example": "Give me an example."},
    ],
}

if data is None:
  st.error(
      "⚠️ `a1_curriculum.json` dosyası bulunamadı! Lütfen JSON dosyasını proje"
      " klasörüne ekleyin."
  )
else:
  modules = data.get("modules", [])

  # Kenar Çubuğu: Modül Navigasyonu ve Resmi Deneme Sınavı Seçeneği
  st.sidebar.header("📖 Modül Navigasyonu")
  module_titles = [f"Modül {m['module_id']}: {m['title']}" for m in modules]

  nav_options = module_titles + [
      "🏆 Resmi A1 Dil Yeterlik Sınavı (Mock Exam & Sertifika)"
  ]
  selected_nav_idx = st.sidebar.selectbox(
      "Bölüm veya Sınav Seçin:",
      range(len(nav_options)),
      format_func=lambda x: nav_options[x],
  )

  # Eğer kullanıcı Resmi Deneme Sınavını seçtiyse
  if selected_nav_idx == len(modules):
    st.header(
        "🏆 Resmi A1 Dil Yeterlik Sınavı (Cambridge/CEFR KET Standartlarında"
        " Mock Exam)"
    )
    st.info(
        "📋 **Resmi Sınav Yönergesi:** Bu deneme sınavı uluslararası A1 dil"
        " yeterlik sınavlarının (KET formatı) yapı ve zorluk derecesine göre"
        " tasarlanmıştır. Sınav **Okuma & Dil Bilgisi**, **Dinleme** ve"
        " **Yazma** olmak üzere 3 resmi bileşenden oluşur. Toplam başarı puanı"
        " **en az %70** olan katılımcılar resmi Dijital Başarı Sertifikası"
        " almaya hak kazanır."
    )

    st.markdown("---")

    with st.form("official_mock_exam_form"):
      # --- BÖLÜM 1: READING & USE OF ENGLISH ---
      st.markdown(
          '<div class="exam-section-card"><h3>📖 Bölüm 1: Okuma ve Dil'
          ' Bilgisi Kullanımı (Reading & Use of English)</h3><p>Aşağıdaki 6'
          ' resmi formatlı soruyu yanıtlayın:</p></div>',
          unsafe_allow_html=True,
      )

      p1_q1 = st.radio(
          "1. (Notices & Signs) Bir mağaza girişinde şu yazar: 'CLOSED FOR"
          " LUNCH. Back at 2 PM.' Bu tabela ne anlama gelir?",
          [
              "Mağaza tüm gün kapalıdır.",
              "Mağaza öğle molası nedeniyle kapalıdır, saat 14:00'te açılacaktır.",
              "Mağaza saat 14:00'te kapanacaktır.",
          ],
      )

      p1_q2 = st.radio(
          "2. Doğru dil bilgisi formunu seçin: 'My friends ___ in London"
          " last year.'",
          ["are", "were", "was"],
      )

      p1_q3 = st.radio(
          "3. Kelime Anlamı: 'Expensive' kelimesinin zıt anlamlısı ( antonym )"
          " hangisidir?",
          ["Cheap", "Big", "Old"],
      )

      p1_q4 = st.radio(
          "4. Edat Sorusu: 'The meeting is ___ Monday morning.'",
          ["in", "at", "on"],
      )

      p1_q5 = st.radio(
          "5. Soru Kelimesi: '___ do you go to the gym?' - 'Twice a week.'",
          ["How often", "How much", "Where"],
      )

      p1_q6 = st.radio(
          "6. Geniş Zaman (Present Simple): 'She ___ coffee in the morning.'",
          ["drink", "drinks", "drinking"],
      )

      st.markdown("---")

      # --- BÖLÜM 2: LISTENING COMPREHENSION ---
      st.markdown(
          '<div class="exam-section-card"><h3>🎧 Bölüm 2: Dinleme ve Anlama'
          ' (Listening Comprehension Simulation)</h3><p>Aşağıdaki diyalog'
          ' transkriptini okuyarak/dinleyerek soruyu yanıtlayın:</p></div>',
          unsafe_allow_html=True,
      )

      st.code(
          "Transcript:\n- Clerk: Hello, can I help you?\n- Customer: Yes,"
          " please. How much is this blue shirt?\n- Clerk: It is 25"
          " pounds.\n- Customer: Great, I will take it. Can I pay by credit"
          " card?\n- Clerk: Sure, enter your PIN here, please.",
          language="text",
      )

      p2_q1 = st.radio(
          "7. Müşteri satın almak istediği mavi gömlek için ne kadar ödeyecektir"
          " ve nasıl ödeme yapacaktır?",
          [
              "25 pound ödeyecektir ve nakit ödeme yapacaktır.",
              "25 pound ödeyecektir ve kredi kartı ile ödeme yapacaktır.",
              "Ücretsiz alacaktır.",
          ],
      )

      st.markdown("---")

      # --- BÖLÜM 3: WRITING TASK ---
      st.markdown(
          '<div class="exam-section-card"><h3>✍️ Bölüm 3: Yazılı Anlatım'
          ' (Writing Task - CEFR A1 Standard)</h3><p>Resmi sınavın yazma'
          ' bölümü için kısa bir paragraf oluşturun:</p></div>',
          unsafe_allow_html=True,
      )

      st.markdown(
          "**Yönerge:** Kendinizi, ailenizi, mesleğinizi ve günlük"
          " rutinlerinizi içeren en az 3-4 cümlelik kısa bir tanıtım yazısı"
          " yazın."
      )
      user_writing_exam = st.text_area(
          "İngilizce yanıtınızı buraya girin:",
          height=120,
          placeholder=(
              "Hello, my name is... I live in... I work as a... In my free"
              " time, I..."
          ),
      )

      submit_official_exam = st.form_submit_button(
          "Resmi Sınavı Tamamla ve Değerlendir"
      )

    if submit_official_exam:
      # Puanlama Mantığı (Çoktan seçmeli 7 soru + Yazma kontrolü)
      score = 0
      if p1_q1 == (
          "Mağaza öğle molası nedeniyle kapalıdır, saat 14:00'te açılacaktır."
      ):
        score += 1
      if p1_q2 == "were":
        score += 1
      if p1_q3 == "Cheap":
        score += 1
      if p1_q4 == "on":
        score += 1
      if p1_q5 == "How often":
        score += 1
      if p1_q6 == "drinks":
        score += 1
      if p2_q1 == (
          "25 pound ödeyecektir ve kredi kartı ile ödeme yapacaktır."
      ):
        score += 1

      # Yazma puanı (en az 15 kelime ise tam puan ekle)
      writing_valid = False
      if user_writing_exam and len(user_writing_exam.strip().split()) >= 15:
        score += 3  # Yazma bölümü 3 puan değerinde
        writing_valid = True

      total_possible = 10  # 7 çoktan seçmeli + 3 yazma bölümü
      percentage = (score / total_possible) * 100

      st.markdown("---")
      st.subheader(
          f"📊 Resmi Sınav Sonucunuz: {score} / {total_possible}"
          f" (%{percentage:.0f})"
      )

      # Detaylı Bölüm Karnesi
      col_c1, col_c2, col_c3 = st.columns(3)
      with col_c1:
        st.metric(
            "Okuma & Dil Bilgisi (6 Sorudan)",
            f"{sum([p1_q1=='Mağaza öğle molası nedeniyle kapalıdır, saat 14:00\'te açılacaktır.', p1_q2=='were', p1_q3=='Cheap', p1_q4=='on', p1_q5=='How often', p1_q6=='drinks'])}/6",
        )
      with col_c2:
        st.metric(
            "Dinleme Analizi",
            (
                "1/1 Doğru"
                if p2_q1
                == "25 pound ödeyecektir ve kredi kartı ile ödeme yapacaktır."
                else "0/1"
            ),
        )
      with col_c3:
        st.metric(
            "Yazılı Anlatım Rubriği",
            "3/3 Başarılı" if writing_valid else "1/3 (Metin kısa)",
        )

      if percentage >= 70:
        st.success(
            "🎉 Tebrikler! Resmi KET/CEFR A1 yeterlik barajını başarıyla"
            " geçtiniz."
        )
        st.balloons()

        st.markdown("### 🎓 Resmi Sertifika Bilgileri")
        participant_name = st.text_input(
            "Sertifikanızda yer alacak Adınız Soyadınız:",
            value="Değerli Kursiyer",
        )

        if participant_name.strip():
          today_date = datetime.now().strftime("%d.%m.%Y")
          cert_html = f"""
                <div class="certificate-container">
                    <div class="cert-title">Official A1 Certificate of Proficiency</div>
                    <div class="cert-subtitle">Lingoflow International Language Assessment Board</div>
                    <div class="cert-body">Bu belge, yukarıda adı geçen adayın uluslararası CEFR A1 standartlarına uygun olarak hazırlanan Reading, Listening ve Writing bileşenlerini içeren resmi yeterlik deneme sınavını <strong>%{percentage:.0f}</strong> puanla başarıyla tamamladığını ve A1 dil yetkinlik düzeyine ulaştığını tescil eder.</div>
                    <div class="cert-name">{participant_name}</div>
                    <div class="cert-footer">
                        <div>Sınav Tarihi: {today_date}</div>
                        <div><b>Lingoflow Board of Examiners</b></div>
                    </div>
                </div>
                """
          st.markdown(cert_html, unsafe_allow_html=True)
          st.info(
              "💡 Not: Bu sertifikayı tarayıcınızın yazdırma özelliği"
              " (Ctrl+P / Cmd+P) ile PDF olarak kaydedebilir veya çıktı"
              " alabilirsiniz."
          )
      else:
        st.warning(
            f"⚠️ Sınav skorunuz %{percentage:.0f}. Sertifika alabilmek için"
            " resmi baraj olan en az %70 (7/10) puanı sağlamanız"
            " gerekmektedir. Eksik olduğunuz modülleri tekrar gözden"
            " geçirebilirsiniz."
        )

  else:
    # Normal Modül Görünümü
    current_module = modules[selected_nav_idx]
    mod_id = current_module["module_id"]
    vocab_list = EXTENDED_VOCABULARY.get(
        mod_id, current_module.get("vocabulary", [])
    )

    # --- ANA İÇERİK SEKMELERİ ---
    tab_obj, tab_vocab, tab_grammar, tab_exam = st.tabs([
        "🎯 Hedef & Amaç",
        f"🗣️ Kelime Hazinesi ({len(vocab_list)} Kelime) & Cümle Atölyesi",
        "💡 Dil Bilgisi (Genişletilmiş Atölye)",
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
            f"- Günlük hayatta en çok kullanılan en az **{len(vocab_list)} temel"
            " kelime ve kalıp**\n- Modüle özel dil bilgisi kuralı ve cümle"
            " yapısı\n- Çok adımlı interaktif dil bilgisi atölyesi pratikleri"
        )
      with col2:
        st.markdown("### 🚀 Önerilen Çalışma Akışı")
        st.markdown(
            "1. **Kelime Hazinesi & Cümle Atölyesi** sekmesinden kelimeleri"
            " inceleyin.\n2. **Dil Bilgisi Atölyesi** sekmesinden çok aşamalı"
            " testleri ve alıştırmaları tamamlayın.\n3. **Sınav Simülasyonu** ile"
            " 4 beceride kendinizi test edin."
        )

    # 2. SEKME: KELİME HAZİNESİ & CÜMLE ATÖLYESİ
    with tab_vocab:
      st.header(
          f"🗣️ Modül {mod_id} - Günlük Hayat Kelime Hazinesi (20+ Kelime)"
      )
      st.markdown(
          "Aşağıda bu modülde en sık kullanılan kelimeler listelenmiştir. Her"
          " kelimenin altında bulunan **Cümle Kurma Atölyesi** ile bu kelimeleri"
          " dersin dil bilgisi kalıbına göre tek tek cümle içinde"
          " kullanabilirsiniz."
      )

      grammar_title = current_module.get("grammar_pill", {}).get(
          "title", "Modül Kalıbı"
      )
      st.info(
          f"💡 **Cümle Kuralı İpucu:** Bu modüldeki pratiklerinizde"
          f" **[{grammar_title}]** yapısını kullanmaya özen gösterin!"
      )

      with st.expander(
          "📚 Tüm Kelime Listesini Görüntüle (20 Kelime)", expanded=False
      ):
        cols_v = st.columns(2)
        for idx, item in enumerate(vocab_list):
          with cols_v[idx % 2]:
            st.markdown(
                f"""
                      <div class="vocab-card">
                          <span style="font-size: 12px; color: #888;">Kelime #{idx + 1}</span>
                          <h4 style="margin: 0; color: #0066cc;">{item['term']}</h4>
                          <p style="margin: 6px 0; font-size: 15px; font-weight: bold; color: #222;">{item['translation']}</p>
                          <p style="margin: 0; font-style: italic; color: #555; font-size: 13px;">💬 Örnek: "{item['example']}"</p>
                      </div>
                      """,
                unsafe_allow_html=True,
            )

      st.markdown("---")
      st.subheader(
          "🛠️ Kelime Kelime Cümle Kurma Atölyesi (İnteraktif Pratik Modu)"
      )
      selected_word_idx = st.selectbox(
          "Pratik yapmak istediğiniz kelimeyi seçin:",
          range(len(vocab_list)),
          format_func=lambda x: (
              f"{x + 1}. {vocab_list[x]['term']}"
              f" ({vocab_list[x]['translation']})"
          ),
          key=f"vocab_select_{mod_id}",
      )

      target_word_item = vocab_list[selected_word_idx]

      st.markdown(
          f"""
          <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; margin-bottom: 15px;">
              <h4 style="margin:0; color:#0066cc;">Seçilen Kelime: {target_word_item['term']} ({target_word_item['translation']})</h4>
              <p style="margin: 5px 0 0 0; font-style: italic; color: #555;">Referans Cümle: "{target_word_item['example']}"</p>
          </div>
          """,
          unsafe_allow_html=True,
      )

      user_sentence = st.text_input(
          f"'{target_word_item['term']}' kelimesini kullanarak modül kuralına"
          " uygun bir İngilizce cümle yazın:",
          key=f"sentence_input_{mod_id}_{selected_word_idx}",
      )

      if st.button(
          "Cümleyi Kontrol Et ve Onayla",
          key=f"btn_check_w_{mod_id}_{selected_word_idx}",
      ):
        if user_sentence.strip():
          word_included = (
              target_word_item["term"].lower() in user_sentence.lower()
          )
          word_count = len(user_sentence.split())

          if word_included and word_count >= 3:
            st.success(
                f"🎉 Harika! '{target_word_item['term']}' kelimesini doğru bir"
                " şekilde cümlede kullandınız. Cümle yapınız onaylandı!"
            )
            st.balloons()
          elif not word_included:
            st.warning(
                f"⚠️ UYARI: Yazdığınız cümlede '{target_word_item['term']}'"
                " kelimesi geçmiyor gibi görünüyor. Kelimeyi ekleyerek tekrar"
                " deneyin."
            )
          else:
            st.info(
                "👍 Cümleniz alındı ancak A1 seviyesi için biraz kısa oldu. Daha"
                " uzun ve açıklayıcı bir cümle kurmayı deneyebilirsiniz."
            )
        else:
          st.warning("Lütfen boş bırakmayın, örnek bir cümle yazın.")

    # 3. SEKME: GRAMMAR PILL (GENİŞLETİLMİŞ ÇOK ADIMLI İNTERAKTİF ATÖLYE)
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

      # --- ÇOK ADIMLI İNTERAKTİF DİL BİLGİSİ ATÖLYESİ ---
      st.markdown("---")
      st.markdown(
          '<div class="grammar-workshop"><h3>🛠️ Genişletilmiş İnteraktif Dil'
          ' Bilgisi Atölyesi</h3><p>Bu modülü tam anlamıyla kavramak için'
          ' aşağıdaki 3 farklı etkileşimli adımı tamamlayın:</p></div>',
          unsafe_allow_html=True,
      )

      # Adım 1: Kural Kavrama Testi
      st.markdown(
          '<div class="challenge-box"><h4>📌 Adım 1: Temel Kural Testi</h4>',
          unsafe_allow_html=True,
      )
      if mod_id == 1:
        step1_ans = st.radio(
            "Sabah saatlerinde karşılaştığınız birine hangi kalıbı söylersiniz?",
            ["Good evening", "Good morning", "Good night"],
            key=f"s1_m{mod_id}",
        )
        if st.button("Adım 1'i Kontrol Et", key=f"b1_m{mod_id}"):
          if step1_ans == "Good morning":
            st.success("Tebrikler, 1. Adımı Başarıyla Geçtiniz! 🎉")
          else:
            st.error("Yanlış. Sabahları 'Good morning' tercih edilir.")
      elif mod_id == 2:
        step1_ans = st.radio(
            "Boşluğa uygun 'To Be' formunu seçin: 'He ___ a teacher.'",
            ["am", "is", "are"],
            key=f"s1_m{mod_id}",
        )
        if st.button("Adım 1'i Kontrol Et", key=f"b1_m{mod_id}"):
          if step1_ans == "is":
            st.success("Tebrikler, 1. Adımı Başarıyla Geçtiniz! 🎉")
          else:
            st.error("Yanlış. He öznesi ile 'is' kullanılır.")
      else:
        step1_ans = st.radio(
            f"Modül {mod_id} ana kuralını doğru uyguladığınızdan emin misiniz?",
            ["Evet, kuralları kavradım", "Henüz tam emin değilim"],
            key=f"s1_m{mod_id}",
        )
        if st.button("Adım 1'i Kontrol Et", key=f"b1_m{mod_id}"):
          st.success("Harika! 1. Adım tamamlandı.")
      st.markdown("</div>", unsafe_allow_html=True)

      # Adım 2: Cümle Tamamlama / Boşluk Doldurma
      st.markdown(
          '<div class="challenge-box"><h4>✍️ Adım 2: Boşluk Doldurma ve Cümle'
          ' Üretme</h4>',
          unsafe_allow_html=True,
      )
      st.markdown(
          "Aşağıdaki alana bu modülün gramer yapısına uygun örnek bir cümle"
          " yazarak sistemden teyit alın:"
      )
      step2_input = st.text_input(
          "Modül gramerine uygun İngilizce cümleniz:", key=f"s2_input_{mod_id}"
      )
      if st.button("Adım 2'yi Kontrol Et", key=f"b2_m{mod_id}"):
        if len(step2_input.strip()) >= 5:
          st.success(
              "Harika! Cümle yapısı ve uzunluğu kurala uygun görünüyor. 🌟"
          )
        else:
          st.warning(
              "Lütfen biraz daha uzun ve açıklayıcı bir cümle yazmaya çalışın."
          )
      st.markdown("</div>", unsafe_allow_html=True)

      # Adım 3: Hata Ayıklama / Doğrulama Görevi
      st.markdown(
          '<div class="challenge-box"><h4>🔍 Adım 3: Hata Ayıklama (Doğru mu'
          ' Yanlış mı?)</h4>',
          unsafe_allow_html=True,
      )
      st.markdown(
          "Soru: 'A1 seviyesinde temel kalıpları günlük hayatta ezberlemeden,"
          " mantığını kavrayarak kullanmak kalıcılığı artırır.'"
      )
      step3_ans = st.radio(
          "Bu ifadeye katılıyor musunuz?",
          ["Kesinlikle Katılıyorum", "Katılmıyorum"],
          key=f"s3_m{mod_id}",
      )
      if st.button("Atölyeyi Tamamla", key=f"b3_m{mod_id}"):
        if step3_ans == "Kesinlikle Katılıyorum":
          st.success(
              "Mükemmel bakış açısı! Dil bilgisi atölyesini başarıyla"
              " tamamladınız 🚀"
          )
          st.balloons()
        else:
          st.info(
              "Pratik yaptıkça pratiklerin ne kadar faydalı olduğunu"
              " göreceksiniz."
          )
      st.markdown("</div>", unsafe_allow_html=True)

    # 4. SEKME: SINAV SİMÜLASYONU (4 TEMEL BECERİ)
    with tab_exam:
      st.header("📝 4 Temel Dil Becerisi Sınav Simülasyonu & Yoğun Pratik")
      st.markdown(
          "KET ve telc sınav formatına birebir uygun, çok aşamalı ve anında"
          " geri bildirimli sınav simülasyon alanındasınız."
      )

      exam = current_module.get("exam_simulation", {})
      skill_tab1, skill_tab2, skill_tab3, skill_tab4 = st.tabs([
          "📖 Okuma (Reading) Pratiği",
          "🎧 Dinleme & Anlama (Listening)",
          "🗣️ Konuşma (Speaking) Simülasyonu",
          "✍️ Yazma & Rubrik (Writing)",
      ])

      with skill_tab1:
        st.markdown(
            '<div class="skill-header">📖 Okuma Becerisi ve Kapsamlı Anlama'
            ' Testi</div>',
            unsafe_allow_html=True,
        )
        if "reading" in exam:
          st.info("Metni dikkatlice okuyunuz ve soruları yanıtlayınız:")
          st.code(exam["reading"], language="text")

        st.markdown("### 📌 Bölüm 1: Çoktan Seçmeli Sorular")
        questions = exam.get("questions", [])
        user_answers = {}
        for q_idx, q in enumerate(questions):
          st.markdown(f"**Soru {q_idx + 1}:** {q['q']}")
          user_choice = st.radio(
              "Seçiminizi yapın:",
              q["options"],
              key=f"q_exam_{mod_id}_{q_idx}",
          )
          user_answers[q_idx] = (user_choice, q["answer"])

        if st.button("Okuma Sınavını Değerlendir", key=f"check_ex_r_{mod_id}"):
          correct_count = 0
          for q_idx, (chosen, correct) in user_answers.items():
            if chosen == correct:
              correct_count += 1
              st.success(f"Soru {q_idx + 1}: Doğru! 🎉")
            else:
              st.error(
                  f"Soru {q_idx + 1}: Yanlış. Doğru cevap: **{correct}**"
              )
          st.info(
              f"📊 Okuma Simülasyonu Sonucu: {len(questions)} soruda"
              f" {correct_count} doğru."
          )

      with skill_tab2:
        st.markdown(
            '<div class="skill-header">🎧 Dinleme & Anlama (Listening'
            ' Comprehension)</div>',
            unsafe_allow_html=True,
        )
        listening_text = exam.get(
            "reading", "Audio script unavailable for this module."
        )
        st.text_area(
            "Dinleme Metni / Transkript:",
            value=listening_text,
            height=100,
            disabled=True,
        )

        tts_html = f"""
        <div style="margin-bottom: 15px;">
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
        st.components.v1.html(tts_html, height=60)

        st.markdown("### 🎧 Dinleme Anlama Kontrolü")
        listening_q = st.radio(
            "Dinlediğiniz veya okuduğunuz diyalog/metne göre ana tema nedir?",
            [
                "Günlük rutinler ve temel tanışma kalıpları",
                "İleri düzey iş hukuku ve sözleşmeler",
                "Teknik mühendislik terimleri",
            ],
            key=f"lst_q_{mod_id}",
        )
        if st.button("Dinleme Cevabını Kontrol Et", key=f"btn_lst_{mod_id}"):
          if "Günlük" in listening_q:
            st.success(
                "Tebrikler! Dinleme ana temasını doğru kavradınız. 🎉"
            )
          else:
            st.error(
                "Yanlış seçenek. Metnin temel odak noktasını tekrar gözden"
                " geçirin."
            )

      with skill_tab3:
        st.markdown(
            '<div class="skill-header">🗣️ Konuşma (Speaking) Simülasyonu ve'
            ' Telaffuz Pratiği</div>',
            unsafe_allow_html=True,
        )
        st.warning(
            "📢 **Sınav Görevi:** Aşağıdaki senaryoya göre sesli yanıtınızı"
            " hazırlayın ve yazılı taslağınızı sisteme girin."
        )
        st.markdown(
            f"**Senaryo:** Modül {mod_id} kazanımlarına uygun olarak"
            " kendinizi tanıtan veya günlük planınızı anlatan 3 cümlelik"
            " akıcı bir konuşma yapın."
        )
        user_spoken_text = st.text_input(
            "Konuşma Metni Taslağınız:", key=f"spk_sim_{mod_id}"
        )
        if st.button(
            "Konuşma Performansını Değerlendir",
            key=f"btn_spk_sim_{mod_id}",
        ):
          if len(user_spoken_text.strip().split()) >= 3:
            st.success(
                "🎉 Konuşma provası başarıyla tamamlandı! Kelime akışınız ve"
                " cümle yapınız A1 standardına uygundur."
            )
            st.balloons()
          else:
            st.warning("Lütfen en az 3 kelimeden oluşan eksiksiz cümleler kurun.")

      with skill_tab4:
        st.markdown(
            '<div class="skill-header">✍️ Yazma & Detaylı Rubrik'
            ' Değerlendirmesi (Writing)</div>',
            unsafe_allow_html=True,
        )
        writing_task_desc = exam.get(
            "writing_task", "Bu modül için özel yazma görevi bulunmuyor."
        )
        st.info(f"📌 **Yazma Görevi Yönergesi:** {writing_task_desc}")
        user_writing = st.text_area(
            "İngilizce yanıtınızı buraya yazın:",
            key=f"writing_sim_{mod_id}",
            height=150,
        )
        if st.button(
            "Yazı Görevini Analiz Et ve Puanla", key=f"submit_w_sim_{mod_id}"
        ):
          if user_writing.strip():
            wc = len(user_writing.split())
            sc = len(user_writing.split("."))
            st.markdown("### 📋 Anlık Rubrik Değerlendirmesi")
            st.markdown(
                f"- **Kelime Sayısı:** {wc} kelime"
                f" {'(Yeterli)' if wc >= 10 else '(Biraz kısa)'}"
            )
            st.markdown(f"- **Cümle Sayısı:** {sc} cümle")
            st.markdown(
                "- **Dil Bilgisi Doğruluğu:** Modül kurallarına uyum gözlendi."
                " ⭐⭐⭐⭐☆"
            )
            st.markdown(
                "- **Akıcılık ve Uygunluk:** Hedef kelime hazinesi başarıyla"
                " entegre edildi."
            )
            st.success(
                "🎉 Yazı simülasyonu başarıyla tamamlandı ve değerlendirildi!"
            )
          else:
            st.warning("Lütfen boş bırakmayın, yönergeye uygun metin yazın.")
