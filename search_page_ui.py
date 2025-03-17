import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="Search Engine",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .search-result {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .result-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .result-description {
        font-size: 1rem;
        color: #424242;
        margin-top: 10px;
    }
    .result-url {
        font-size: 0.9rem;
        color: #4CAF50;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Page title and description
st.title("🔍 Search Engine")
st.markdown("Enter your search query below to find relevant results.")

# Search bar
search_query = st.text_input("", placeholder="Type your search query here...")

# Function to make API call
def search_api(query):
    if not query:
        return []
    
    url = f"https://steveykyu.app.n8n.cloud/webhook/73551d63-6381-4a73-bfde-164e6e3ccf6d?query={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        return data.get("output", {}).get("output", [])
    except Exception as e:
        st.error(f"Error fetching search results: {e}")
        return []

# Process search when query is provided
if search_query:
    st.markdown("---")
    st.subheader("Search Results")
    
    # Show loading spinner while fetching results
    with st.spinner("Searching..."):
        search_results = search_api(search_query)
    
    # Display search results
    if search_results:
        N_cards_per_row = 3
        for n_row, result in enumerate(search_results):
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            
            # Display each result in its own card
            with cols[n_row % N_cards_per_row]:
                st.markdown(f"### {result.get('title', 'No Title')}")
                st.markdown(f"{result.get('description', 'No Description')}")
                if result.get('url'):
                    st.markdown(f"[Learn more]({result.get('url')})")

    else:
        st.info("No results found for your search query.")

# Footer
st.markdown("---")
st.markdown("Powered by Streamlit and custom API")