---

# 🌟 AiChatApp

AiChatApp is a Python-based chatbot application designed to provide intelligent and responsive conversational experiences. Utilizing natural language processing (NLP) techniques, this app understands and responds to user inputs meaningfully.

---

## ✨ Features

- 🔐 **User Authentication**: Secure login and signup functionality to manage user access.
- 💬 **Interactive Chat Interface**: Engaging chat interface for seamless user interaction.
- 🛠️ **Customizable Intents**: Easily modify intents and responses through the `intents.json` file.
- 📚 **Model Training**: Train the chatbot model with ease using the `train.py` script.

---

## 🛠 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/none159/AiChatApp.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd AiChatApp
   ```
3. **Install Dependencies**:
   Ensure you have Python installed. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

1. **Train the Model**:
   Before running the application, train the chatbot model:
   ```bash
   python train.py
   ```
2. **Run the Application**:
   Launch the application:
   ```bash
   python home.py
   ```
3. **Start Chatting**:
   Interact with the chatbot via its intuitive interface!

---

## 📂 Project Structure

Here's an overview of the key files and their purposes:

| File/Directory    | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `home.py`         | Main application script to launch the chat interface.        |
| `login.py`        | Manages user login functionality.                            |
| `signup.py`       | Handles user registration.                                   |
| `chat.py`         | Processes user inputs and generates responses.               |
| `train.py`        | Script to train the chatbot model.                           |
| `model.py`        | Defines the chatbot model architecture.                      |
| `nltkutils.py`    | Utility functions for NLP tasks.                             |
| `intents.json`    | Predefined intents and responses for the chatbot.            |
| `requirements.txt`| Lists all dependencies required to run the application.      |

---

## 🎨 Customization

1. Open the `intents.json` file to add or edit intents and responses.
2. Retrain the model using:
   ```bash
   python train.py
   ```

---
