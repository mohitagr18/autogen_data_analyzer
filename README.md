# AutoGen Data Analyzer 🤖

A multi-agent AI application built with AutoGen and Streamlit that performs real-time data analysis based on natural language commands.

## 🚀 Overview

This application leverages a team of AI agents to perform on-the-fly data analysis. Users can watch in real-time as the agents collaborate to **automatically write and execute Python code**, generating instant insights, plots, and full reports from any uploaded CSV file.

<!-- **[➡️ Live Demo Link (Add Your Deployed App Link Here)]** -->

## ✨ Key Features

* **Conversational Interface:** Interact with your data by asking questions in plain English.
* **Automated Code Generation:** AI agents write, display, and execute the necessary Python data analysis code.
* **Dynamic Workflows:** Intelligently handles both broad, open-ended questions (generating full reports) and specific queries (providing direct answers or plots).
* **Automated EDA Reports:** Generates comprehensive Exploratory Data Analysis (EDA) reports in markdown format for broad analysis tasks.
* **On-the-Fly Visualizations:** Creates and displays data visualizations like charts and heatmaps based on user requests.

## 🛠️ How It Works

The application uses a multi-agent architecture orchestrated by **Microsoft AutoGen**.

* **Frontend:** A user-friendly interface built with **Streamlit**.
* **Backend:** A team of collaborative AI agents powered by the **OpenAI API**.
* **The Agents:**
    * **`UserProxyAgent`**: Represents the human user in the chat, relaying requests to the agent team.
    * **`Data_Analyzer`**: The "planner" agent. It interprets the user's request, decides on an analysis strategy, and writes the Python code.
    * **`Python_Code_Executor`**: The "executor" agent. It runs the generated code within a secure **Docker** container and reports back the results or errors.

## 💻 Tech Stack

* **Python**
* **Frameworks:** Streamlit, AutoGen
* **AI:** OpenAI API (GPT-4)
* **Containerization:** Docker

## 📖 Usage

1.  Launch the application.
2.  Upload your CSV file using the file uploader.
3.  Type your question into the chat input box (e.g., "Analyze this data" or "Plot the sales distribution").
4.  Watch as the AI agents collaborate and generate the code.
5.  View the final report, plot, or answer directly in the app.

<!-- ## 📸 Screenshots

*(Add a screenshot or a GIF of your application in action here)*

![App Screenshot](placeholder.png) -->