# 🤖 AI Resume Job Recommender

An AI-powered web application that analyzes resumes and recommends relevant job opportunities based on skills, keywords, and job requirements.

## 🌐 Live Demo

🚀 **Try the application here:**

https://harshiairesumerecommender.streamlit.app/

---

## 📌 About the Project

The **AI Resume Job Recommender** is a machine learning-based web application designed to help students, fresh graduates, and job seekers find suitable job opportunities.

Users can upload their resume, and the application analyzes the resume content and compares the candidate's skills with available job descriptions.

The system then recommends relevant jobs based on the similarity between the resume and job requirements.

---

## ✨ Features

- 📄 Resume upload
- 🔍 Resume text extraction
- 🧠 Resume skill and keyword analysis
- 💼 Job recommendation
- 🎯 Resume-to-job matching
- 📊 Job relevance scoring
- 🔎 Job search and filtering
- 🌐 Interactive Streamlit web application
- 🚀 Publicly deployed application
- 📱 Accessible from desktop and mobile devices

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Natural Language Processing (NLP)**
- **Machine Learning**
- **Scikit-learn**
- **Regular Expressions**
- **CSV Dataset**

---

## ⚙️ How the Application Works

```text
              USER
                │
                ▼
        Upload Resume
                │
                ▼
       Extract Resume Text
                │
                ▼
      Extract Skills & Keywords
                │
                ▼
       Process Job Dataset
                │
                ▼
      Compare Resume & Jobs
                │
                ▼
       Calculate Match Score
                │
                ▼
       Recommend Relevant Jobs
                │
                ▼
        Display Results
📊 Dataset

The application uses a job dataset containing information related to different job opportunities.

The dataset includes information such as:

Job Title
Company
Job Description
Required Skills
Location
Job-related information

The dataset is processed using Python and Pandas before being used by the recommendation system.

🧠 Recommendation System

The application analyzes important information from the uploaded resume and compares it with job descriptions.

The matching process focuses on:

Candidate skills
Resume keywords
Job requirements
Job descriptions
Similarity between resume and job information

The system then presents the most relevant job opportunities to the user.

💻 Project Structure
AI_Resume_Job_Recommender/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
└── dataset/
    │
    └── jobs.csv
🚀 Run the Project Locally
1. Clone the repository
git clone https://github.com/Harshi1904/AI_Resume_Job_Recommender.git
2. Open the project folder
cd AI_Resume_Job_Recommender
3. Install dependencies
pip install -r requirements.txt
4. Run the Streamlit application
streamlit run app.py

The application will open in your browser.

🎯 Use Cases

This project can be useful for:

🎓 College students
👩‍💻 Fresh graduates
💼 Job seekers
🧑‍💼 Career guidance
📄 Resume analysis
🎯 Job matching
🚀 Internship searches
🔮 Future Enhancements

The project can be further improved by adding:

🤖 Advanced NLP-based semantic matching
📊 Resume skill-gap analysis
🎯 Personalized job recommendations
📈 Job recommendation ranking
💡 Resume improvement suggestions
🔗 Job portal API integration
👤 User accounts and profiles
📧 Job alerts
📱 Improved mobile interface
🧠 Large Language Model-based resume analysis
🌐 Deployment

The application is deployed using Streamlit Community Cloud.

Live Application

👉 https://harshiairesumerecommender.streamlit.app/

👩‍💻 Developer
Chandra Harshitha

B.Tech – Computer Science and Engineering

GitHub:
https://github.com/Harshi1904

⭐ Project Goal

The goal of this project is to create an intelligent job recommendation system that helps candidates discover suitable career opportunities by matching their resume skills and experience with relevant job requirements.

❤️ Acknowledgement

This project was developed as a practical implementation of Python, Machine Learning, Natural Language Processing, and Data Analysis concepts.

⭐ If you find this project useful, consider giving the repository a star!
