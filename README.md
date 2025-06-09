# Interview Status Chatbot

A professional HR assistant chatbot that provides job applicants with their application status and interview details.

## Overview

This application uses RAG (Retrieval Augmented Generation) to retrieve applicant information from a Google Sheet and generate personalized responses about interview status, dates, times, and locations. The chatbot provides a user-friendly interface for applicants to check their application status by simply entering their name and the position they applied for.

## Features

- Retrieves applicant data from a Google Sheet
- Stores and indexes data using Pinecone vector database
- Uses Groq LLM API for generating professional HR responses
- Provides a clean web interface using Chainlit
- Maintains privacy by only showing information relevant to the specific applicant

## Requirements

- Python 3.8+
- Pinecone API key
- Groq API key
- Google Sheet with applicant data (shared as CSV)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/abdullah-k18/interview-updates.git
   cd interview-updates
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys (see `.env.example` for reference)

## Usage

### Quick Start (No Google Sheet Setup Needed)

If you do not provide a `SHEET_URL` in your `.env`, the application will automatically load sample applicant data from the following public Google Sheet:

📄 [Sample Sheet](https://docs.google.com/spreadsheets/d/1-NcmknFNSDg2S7o6Pn4-oMw3EWL6gZGbShcb1QDNEeM/edit?gid=0#gid=0)

Just ensure your `.env` has:

```ini
PINECONE_API_KEY=your_pinecone_key
GROQ_API_KEY=your_groq_key
```

1. Run the application:
   ```
   chainlit run main.py
   ```
2. Open your browser and navigate to `http://localhost:8000`
3. Enter your name and position to check your application status

### Example Prompts for sample sheet

```commandline
My name is Abdullah and I have applied for AI Engineer position.
```

```commandline
My name is John and I have applied for Software Engineer position.
```

## Google Sheet Structure

The application expects a Google Sheet with the following columns:

| Column Name       | Description                                   |
|-------------------|-----------------------------------------------|
| Name              | Full name of the applicant                    |
| Position          | Job position applied for                      |
| Application Date  | Date when the application was submitted       |
| Application Status| Current status of the application             |
| Interview Status  | Status of the interview (scheduled/not selected) |
| Interview Date    | Date of the scheduled interview               |
| Interview Time    | Time of the scheduled interview               |
| Interview Mode    | Online or On-site                             |
| Address           | Zoom/Meet link or physical address            |

## How It Works

1. The application loads applicant data from a Google Sheet
2. Data is embedded and stored in a Pinecone vector database
3. When a user queries their status, the system:
   - Embeds the query
   - Searches for relevant matches in the vector database
   - Retrieves the applicant's information
   - Uses Groq LLM to generate a personalized response
   - Returns the information through the Chainlit interface

## Environment Variables

- `PINECONE_API_KEY`: Your Pinecone API key
- `GROQ_API_KEY`: Your Groq API key
- `SHEET_URL`: URL to your Google Sheet in CSV format

## License

[MIT License](https://github.com/abdullah-k18/interview-status-chatbot/blob/main/LICENSE)
