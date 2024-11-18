# Breakout-AI-Agent

```markdown
# AI Agent for Data Extraction

## Project Description
This project features an AI agent that extracts specific information from web search results based on user-defined queries. It allows users to upload a CSV file or connect a Google Sheet, choose the primary column for entity extraction, and input custom prompts for data retrieval. The agent uses a search API to retrieve information for each entity and processes the results with an LLM (Large Language Model) to extract structured data. The results are displayed in a simple, intuitive dashboard, where users can download the data as CSV or update their Google Sheets.

## Features
- **File Upload**: Upload CSV files or link Google Sheets.
- **Dynamic Query Input**: Input custom queries using placeholders like `{company}` for dynamic entity processing.
- **Automated Web Search**: Retrieve relevant data from web searches.
- **LLM Integration**: Parse and extract data from web search results using an LLM.
- **Display Results**: View and download the structured data in CSV format.
- **Google Sheets Integration**: Update Google Sheets with the extracted information.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-data-extraction-dashboard.git
   ```
2. Navigate into the project directory:
   ```bash
   cd ai-data-extraction-dashboard
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - `GOOGLE_SHEET_API_KEY`: API key for accessing Google Sheets.
   - `SERP_API_KEY`: API key for accessing the search service.
   - `LLM_API_KEY`: API key for accessing the LLM API (e.g., OpenAI, Groq).

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

1. Upload your CSV file or link a Google Sheet.
2. Select the column containing the entities (e.g., company names).
3. Enter a custom search query, e.g., "Get me the email address of {company}".
4. Click "Start" to run the search and retrieve data.
5. View the results in a table and download the data as CSV or update your Google Sheet.

## API Keys and Environment Variables
- `GOOGLE_SHEET_API_KEY`: Obtain from the [Google Cloud Console](https://console.cloud.google.com/).
- `SERP_API_KEY`: Sign up at [SerpAPI](https://serpapi.com/).
- `LLM_API_KEY`: Obtain from the [OpenAI API](https://platform.openai.com/) or [Groq](https://groq.com/).

## Optional Features
- **Advanced Query Templates**: Users can extract multiple fields in a single query.
- **Google Sheets Output Integration**: Option to write back results to the Google Sheet.
- **Error Handling**: The app includes robust error handling for failed API calls and unsuccessful queries.

## Acknowledgments
- [SerpAPI](https://serpapi.com/) for search data retrieval.
- [OpenAI](https://openai.com/) for LLM integration.
