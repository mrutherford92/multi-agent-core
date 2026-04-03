# AI Technology Report

This report details the AI-related technologies and their applications across the projects in this directory. The analysis is based on a review of project configuration files, source code, and directory structures.

---

## 🤖 Chatbot Central

This project is a hub for various AI agent and chatbot applications.

### Technologies Used:
- **LangChain & LangChain Google GenAI**: The core frameworks used for building applications powered by large language models (LLMs). `langchain-google-genai` specifically integrates Google's generative AI models.
- **FAISS (Facebook AI Similarity Search)**: A library for efficient similarity search and clustering of dense vectors. It is used in the `rag_app` for building a Retrieval-Augmented Generation (RAG) system, which allows the chatbot to retrieve relevant information from a local knowledge base.
- **PyPDF**: A library for reading and extracting text from PDF files. This is likely used to ingest documents into the RAG system's knowledge base.
- **Streamlit**: A framework for creating and sharing web apps for machine learning and data science. It is used to build user interfaces for the chatbots and agents.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs. This is likely used to create API endpoints for the AI agents.

### Projects:
- **RAG Chatbot (`rag_app`)**: A chatbot that uses a RAG architecture to answer questions based on a corpus of documents. It leverages `LangChain`, `FAISS`, and `PyPDF` to create and query a vector database.
- **LinkedIn Agent (`linkedin_agent`)**: An AI agent designed to generate posts for LinkedIn. It uses `LangChain` with a Google GenAI model to create content.

---

## 🏡 Real Estate Market Prediction

This project focuses on using machine learning to predict real estate market prices.

### Technologies Used:
- **PyTorch**: A popular open-source machine learning framework. It is the primary tool used for building, training, and evaluating the predictive models.
- **Scikit-learn**: A fundamental library for machine learning in Python. It is likely used for data preprocessing, feature engineering, and potentially for baseline models.
- **Pandas & NumPy**: Essential libraries for data manipulation, and numerical computation, used for handling the real estate datasets.
- **Streamlit**: Used in the `demo-streamlit` app to create an interactive web-based demonstration of the prediction model.
- **FastAPI**: Used to create a `mock-server`, likely for simulating a production environment or providing API access to the trained model.

### Architecture:
The project is structured with a core `prediction_model` library built with `PyTorch` and a `real_estate_sdk` for interacting with the model. A `demo-streamlit` app provides a user-friendly interface for predictions.

---

## 🎨 Neuro-Arts Flutter

This is a sophisticated Flutter application that integrates multiple on-device and cloud-based AI features, focusing on audio, music, and user interaction.

### Technologies Used:
- **TensorFlow Lite (`tflite_flutter`)**: A version of TensorFlow optimized for deploying models on mobile and embedded devices. This is used for on-device machine learning tasks.
- **Google ML Kit (`google_mlkit_pose_detection`)**: A mobile SDK that brings Google's machine learning expertise to mobile apps. This project specifically uses the Pose Detection API, which can detect human body poses in real-time from images or video. This could be used for interactive art, gesture control, or analyzing user posture.
- **Firebase Vertex AI (`firebase_vertexai`)**: Integrates Google Cloud's Vertex AI platform, allowing the app to leverage powerful, scalable AI models for generative AI tasks directly from the mobile app.
- **Cloud Functions for Firebase**: The `functions_chatbot` directory indicates the use of serverless functions to run backend code in response to events. This includes a chatbot powered by `google-cloud-aiplatform`, suggesting it calls out to Google's generative AI models.
- **Audio Processing**: Libraries like `pitch_detector_dart`, `flutter_sound`, and `dart_melty_soundfont` suggest AI-related audio analysis, such as pitch detection for musical applications or voice analysis.

### Features:
The combination of these technologies suggests features like:
- **Real-time Pose Tracking**: For interactive experiences.
- **Generative AI Chatbot**: A chatbot integrated within the app, powered by Google's AI platform.
- **On-device ML**: For low-latency tasks without needing a network connection.
- **Musical AI**: Tools for analyzing pitch and interacting with musical concepts.

---

## 🧠 AYI (Are You Investable)

This project appears to be a system that leverages AI for analysis, likely related to business or investment evaluation, using AWS services.

### Technologies Used:
- **AWS Bedrock**: The `ayi/aws/bedrock` directory and its `requirements.txt` point to the use of Amazon Bedrock, a fully managed service that offers a choice of high-performing foundation models from leading AI companies via a single API.
- **LangChain**: The presence of `langchain`, `langchain-aws`, and `langchain-community` indicates that the project uses the LangChain framework to build LLM-powered applications, specifically integrating with AWS services.
- **FAISS (CPU)**: The inclusion of `faiss-cpu` suggests that this project also involves creating and querying a vector database for similarity searches, a core component of RAG systems.
- **Firebase Admin**: Used for backend integration with Firebase services.
- **PyPDF**: For ingesting PDF documents, likely to populate the FAISS vector database.

### Purpose:
The name "Are You Investable" combined with these technologies suggests an application that might:
- Analyze business plans, pitch decks, or other documents (ingested via `pypdf`).
- Use a RAG system (`LangChain` + `FAISS`) to answer questions about these documents.
- Leverage powerful foundation models via AWS Bedrock to perform analysis, summarization, or generate insights.