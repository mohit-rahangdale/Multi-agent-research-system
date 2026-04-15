import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Research Pipeline",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Orange & Black Theme
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #FF6B00 0%, #FF8C00 50%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Agent cards */
    .agent-card {
        background: linear-gradient(135deg, #1f1f1f 0%, #2d2d2d 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #FF6B00;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .agent-card:hover {
        transform: translateY(-2px);
        transition: all 0.3s ease;
        box-shadow: 0 6px 12px rgba(255,107,0,0.2);
    }
    
    /* Report container */
    .report-container {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B00;
        margin: 1rem 0;
        color: #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Feedback container */
    .feedback-container {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF8C00;
        margin: 1rem 0;
        color: #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF8C00 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,107,0,0.4);
        background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: #FF8C00;
        border: 1px solid #FF6B00;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FFA500;
        box-shadow: 0 0 0 2px rgba(255,107,0,0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #e0e0e0;
        background-color: #2d2d2d;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B00 0%, #FF8C00 100%);
        color: white;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #1e1e1e;
        color: #FF8C00;
        border: 1px solid #FF6B00;
        border-radius: 8px;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a;
        color: #e0e0e0;
        border-radius: 0 0 8px 8px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #0a0a0a;
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #FF6B00;
    }
    
    .stMetric label {
        color: #FF8C00 !important;
        font-weight: bold;
    }
    
    .stMetric div {
        color: #FFA500 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF6B00 0%, #FF8C00 50%, #FFA500 100%);
    }
    
    /* Success message */
    .stAlert {
        background-color: #1e3a1e;
        border-left-color: #FF6B00;
        color: #FFA500;
    }
    
    /* Error message */
    .stAlert {
        background-color: #3a1e1e;
        border-left-color: #FF0000;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #FF6B00;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #FF8C00;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FF8C00 !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #b0b0b0 !important;
    }
    
    /* Markdown text */
    p, li, span {
        color: #e0e0e0;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF8C00 100%);
        color: white;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-left: 4px solid #FF6B00;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'pipeline_history' not in st.session_state:
        st.session_state.pipeline_history = []
    if 'current_run' not in st.session_state:
        st.session_state.current_run = None
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'show_history' not in st.session_state:
        st.session_state.show_history = False

def run_research_pipeline(topic: str, progress_placeholder, status_placeholder):
    """Run the research pipeline with progress updates"""
    
    state = {}
    
    # Step 1: Search Agent
    status_placeholder.markdown("### 🔍 Step 1: Search Agent is gathering information...")
    progress_placeholder.progress(10)
    time.sleep(0.5)
    
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content
    
    status_placeholder.markdown("✅ **Search Agent** completed!")
    progress_placeholder.progress(30)
    
    # Step 2: Reader Agent
    status_placeholder.markdown("### 📖 Step 2: Reader Agent is scraping top resources...")
    progress_placeholder.progress(40)
    time.sleep(0.5)
    
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    
    state['scraped_content'] = reader_result['messages'][-1].content
    status_placeholder.markdown("✅ **Reader Agent** completed!")
    progress_placeholder.progress(60)
    
    # Step 3: Writer Chain
    status_placeholder.markdown("### ✍️ Step 3: Writer is drafting the report...")
    progress_placeholder.progress(70)
    time.sleep(0.5)
    
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    
    status_placeholder.markdown("✅ **Writer** completed!")
    progress_placeholder.progress(85)
    
    # Step 4: Critic
    status_placeholder.markdown("### 🎯 Step 4: Critic is reviewing the report...")
    progress_placeholder.progress(90)
    time.sleep(0.5)
    
    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })
    
    progress_placeholder.progress(100)
    status_placeholder.markdown("✅ **Pipeline completed successfully!** 🎉")
    
    state["topic"] = topic
    state["timestamp"] = datetime.now()
    
    return state

def main():
    initialize_session_state()
    
    # Sidebar with Orange & Black theme
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="https://img.icons8.com/fluency/96/000000/artificial-intelligence.png" width="80" style="filter: drop-shadow(0 0 10px #FF6B00);">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🤖 Multi-Agent System")
        st.markdown("---")
        
        st.markdown("### 🔥 Agents in Pipeline:")
        
        agents_info = {
            "🔍 Search Agent": "Gathers recent and reliable information using web search",
            "📖 Reader Agent": "Scrapes and extracts detailed content from URLs",
            "✍️ Writer Agent": "Drafts comprehensive research reports",
            "🎯 Critic Agent": "Reviews reports and provides constructive feedback"
        }
        
        for agent, description in agents_info.items():
            with st.expander(agent):
                st.markdown(f'<span style="color: #FF8C00;">{description}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 History", use_container_width=True):
                st.session_state.show_history = not st.session_state.show_history
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.pipeline_history = []
                st.success("History cleared!")
        
        st.markdown("---")
        st.markdown("""
        <div class="info-box">
            <small>⚡ Powered by Multi-Agent AI System<br>
            🎨 Orange & Black Theme</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.markdown('<div class="main-header">🔥 Multi-Agent Research System</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input(
            "### 📝 Enter your research topic",
            placeholder="e.g., Climate change impacts on agriculture, Recent advances in quantum computing, etc.",
            key="topic_input"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_button = st.button("🚀 Run Pipeline", disabled=st.session_state.running or not topic, use_container_width=True)
    
    # Display current run
    if run_button and topic:
        st.session_state.running = True
        
        # Create placeholders for progress
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        results_placeholder = st.empty()
        
        try:
            # Run pipeline
            state = run_research_pipeline(topic, progress_placeholder, status_placeholder)
            
            # Display results
            with results_placeholder.container():
                st.markdown("---")
                st.markdown("## 📊 Pipeline Results")
                
                # Create tabs for different sections
                tab1, tab2, tab3, tab4 = st.tabs(["📄 Final Report", "💬 Critic Feedback", "🔍 Search Results", "📚 Scraped Content"])
                
                with tab1:
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.markdown(f"### 📝 Report on: {topic}")
                    st.markdown(state['report'])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Report (TXT)",
                        data=state['report'],
                        file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.markdown('<div class="feedback-container">', unsafe_allow_html=True)
                    st.markdown("### 🎯 Critic Review & Suggestions")
                    st.markdown(state['feedback'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab3:
                    with st.expander("🔍 View Search Results", expanded=False):
                        st.markdown(f'<div style="background-color: #1a1a1a; padding: 1rem; border-radius: 8px;">{state["search_results"]}</div>', unsafe_allow_html=True)
                
                with tab4:
                    with st.expander("📚 View Scraped Content", expanded=False):
                        st.markdown(f'<div style="background-color: #1a1a1a; padding: 1rem; border-radius: 8px;">{state["scraped_content"]}</div>', unsafe_allow_html=True)
            
            # Save to history
            st.session_state.pipeline_history.append({
                "topic": topic,
                "timestamp": state["timestamp"],
                "report": state['report'],
                "feedback": state['feedback']
            })
            
            st.session_state.current_run = state
            
            # Success message with custom styling
            st.balloons()
            st.success("✅ Research pipeline completed successfully! 🎉")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)
        
        finally:
            st.session_state.running = False
            progress_placeholder.empty()
            status_placeholder.empty()
    
    # History section
    if st.session_state.pipeline_history and st.session_state.show_history:
        st.markdown("---")
        st.markdown("## 📜 Pipeline History")
        
        for idx, item in enumerate(reversed(st.session_state.pipeline_history)):
            with st.expander(f"📌 {item['topic']} - {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**📄 Report Preview:**")
                    st.markdown(f'<div style="background-color: #1a1a1a; padding: 0.5rem; border-radius: 5px;">{item["report"][:300]}...</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown("**💬 Feedback Preview:**")
                    st.markdown(f'<div style="background-color: #1a1a1a; padding: 0.5rem; border-radius: 5px;">{item["feedback"][:200]}...</div>', unsafe_allow_html=True)
                
                if st.button(f"Load Report", key=f"load_{idx}"):
                    st.session_state.current_run = item
                    st.rerun()
    
    # Display metrics if there's history
    if st.session_state.pipeline_history:
        st.markdown("---")
        st.markdown("### 📊 System Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Total Reports", len(st.session_state.pipeline_history))
        with col2:
            unique_topics = len(set([h['topic'] for h in st.session_state.pipeline_history]))
            st.metric("🎯 Unique Topics", unique_topics)
        with col3:
            avg_length = sum(len(h['report']) for h in st.session_state.pipeline_history) / len(st.session_state.pipeline_history)
            st.metric("📏 Avg Report Length", f"{int(avg_length)} chars")

if __name__ == "__main__":
    main()