import streamlit as st
from main import extract_video_id, get_transcript, translate_transcript_to_english, get_important_topics, generate_notes, create_chunks, create_vector_store, rag_answer

# Sidebar configuration
with st.sidebar:
    st.title("📹 Video Insight")
    st.markdown("---")
    st.markdown("Analyze and extract insights from YouTube videos using AI.")
    st.markdown("### Input Details")

    youtube_url = st.text_input("YouTube Video URL", placeholder="https://youtu.be/YXfRsS8MzX4?si=sDIQQR3icos3lsr_")
    language = st.text_input("Video Language Code", placeholder="Eg: en, hi, fr, de, es, etc.", value="en")

    task_option = st.radio("Select Task:", ["Chat with Video", "Summarize Video"])

    submit_button = st.button("✨ Start Processing")
    st.markdown("---")


# Main content area
st.title("Video Insight Application")
st.markdown("Enter a YouTube Video URL and select a task from the sidebar to get started.")

if submit_button:
    if youtube_url and language:
        video_id = extract_video_id(youtube_url)
        if video_id:
            with st.spinner("Fetching transcript..."):
                full_transcript = get_transcript(video_id, language)
            if full_transcript and language != "en":
                with st.spinner("Translating transcript to English..."):
                    full_transcript = translate_transcript_to_english(full_transcript)
            if task_option == "Summarize Video":
                if full_transcript:
                    with st.spinner("Extracting important topics..."):
                        imp_topics = get_important_topics(full_transcript)
                        st.subheader("Important Topics")
                        st.write(imp_topics)

                    with st.spinner("Generating notes..."):
                        notes = generate_notes(full_transcript)
                        st.subheader("Summary Notes")
                        st.write(notes)

                    st.success("Summary generation completed!")

                else:
                    st.error("Transcript generation/translation failed.")
            
            if task_option == "Chat with Video":
                with st.spinner("Creating chunks and vector store...."):
                    chunks = create_chunks(full_transcript)
                    vectorstore = create_vector_store(chunks)
                    st.session_state.vector_store = vectorstore
                st.session_state.messages=[]
                st.success('Ready for chat! Ask your questions below.')

    else:
        st.error("Please enter both YouTube URL and Language Code.")

if task_option=="Chat with Video" and "vector_store" in st.session_state:
    st.divider()
    st.subheader("Chat with Video")

    # Display the entire history
    for message in st.session_state.get('messages',[]):
        with st.chat_message(message['role']):
            st.write(message['content'])

    # user_input
    prompt = st.chat_input("Ask me anything about the video.")
    if prompt:
        st.session_state.messages.append({'role':'user','content':prompt})
        with st.chat_message('user'):
            st.write(prompt)

        with st.chat_message('assistant'):
           response= rag_answer(prompt,st.session_state.vector_store)
           st.write(response)
        st.session_state.messages.append({'role': 'assistant', 'content':response})