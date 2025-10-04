# AI Video Insight
AI Video Insight is a Streamlit application that allows users to analyze and extract insights from YouTube videos using AI. Users can either summarize a video into key topics and notes or interactively chat with the video content.

🚀 Live Demo
Try the app here: https://ai-video-insight.streamlit.app/

## **Note:
This project relies on the YouTube API. Due to restrictions on cloud-hosted apps, API calls may be blocked when using the public Streamlit link. The app is deployed using [proxy servers](https://www.webshare.io/features/free-proxy), so there is approximately a 50% chance the app will work online. For best results, run the app locally or use a paid API plan.

## Features
* **Summarize Video**: Automatically extract important topics and generate summary notes from any YouTube video.
* **Chat with Video**: Interactively ask questions about the video content and get AI-powered answers.
* **Multi-language support**: Transcribes videos in various languages and provides summaries, even if the video is not in English.
* **Easy-to-use interface**: Streamlined sidebar input for video URL, language, and task selection.

## Getting Started

### Prerequisites
* Python 3.10+
* Google Gemini API Key
* Other dependencies listed in requirements.txt

### Installation
**Clone the repository**:

`git clone https://github.com/Shivani-781/AI-Video-Insight.git`

`cd AI-Video-Insight`

**Create a virtual environment (recommended)**:

`python3 -m venv .venv`

`source .venv/bin/activate`

**Install dependencies**:

`pip install -r requirements.txt`

**Set up your API key**:

Add your YouTube API key to the .env file:

`GOOGLE_API_KEY="YOUR_API_KEY"`

### Usage
* Run Locally: `streamlit run app.py`
* Open the URL displayed in your terminal (usually http://localhost:8501).
* Sidebar Inputs:
  + YouTube Video URL: Paste the video link you want to analyze.
  + Video Language Code: Specify the language code (e.g., en, hi, fr).
  + Select Task: Choose between “Summarize Video” or “Chat with Video”.
* Click **Start Processing** and wait for the AI to process the video.
* Outputs:
  +	Summarize Video: Displays important topics and summary notes.
  +	Chat with Video: Start a conversation about the video content. Ask questions, and the AI responds contextually.

### Limitations

**Cloud Deployment**:
The app may not work reliably on the public Streamlit cloud due to YouTube API restrictions. Proxy servers are used, but success is not guaranteed.

**Recommended**:
For full functionality, run the app locally with your own API key.
Alternatively, consider a paid API plan for higher reliability.
