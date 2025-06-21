# Interview Status Chatbot

A professional HR assistant chatbot that provides job applicants with their application status and interview details.

## Overview

This application uses RAG (Retrieval Augmented Generation) to retrieve applicant information from a CSV file and generate personalized responses about interview status, dates, times, and locations. The chatbot provides a user-friendly interface for applicants to check their application status by simply entering their name and the position they applied for.

## Features

- Retrieves applicant data from a CSV file
- Stores and indexes data using Pinecone vector database
- Uses Groq LLM API for generating professional HR responses
- Provides a clean web interface using Chainlit
- Maintains privacy by only showing information relevant to the specific applicant

## Requirements

- Python 3.8+
- Pinecone API key
- Groq API key
- CSV file

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

Just ensure your `.env` has:

```ini
PINECONE_API_KEY=your_pinecone_key
GROQ_API_KEY=your_groq_key
```

1. Add the CSV file to the root of project named `applications.csv`
OR 
Create a dummy CSV file using `faker` library:
   ```
   python import_fake_data.py
   ```

2. Run the application:
   ```
   chainlit run main.py
   ```
3. Open your browser and navigate to `http://localhost:8000`
4. Enter your name and position to check your application status

### Prompt Structure

```commandline
My name is {name} and I have applied for {role} position.
```

## Custom CSV file Structure

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

1. The application loads applicant data from a CSV file
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

## License

[MIT License](https://github.com/abdullah-k18/interview-status-chatbot/blob/main/LICENSE)
