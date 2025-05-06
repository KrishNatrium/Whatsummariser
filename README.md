# WhatsApp Group Chat Summarizer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.0+-orange.svg)

A Python script that automatically summarizes WhatsApp group conversations by:
1. Accessing WhatsApp Web
2. Extracting messages from specified groups
3. Generating concise summaries using AI-powered text summarization

## Features

- 🚀 **Automatic Login** - Connects via WhatsApp Web with QR code
- 📊 **Message Extraction** - Retrieves specified number of messages
- ✨ **Smart Summarization** - Uses Sumy's LSA algorithm for key point extraction
- 📈 **Activity Analysis** - Shows top participants and message statistics
- 🔒 **Privacy Focused** - Runs locally without storing your messages

## Installation

1. Clone this repository:
```bash
git clone https://github.com/KrishNatrium/Whatsummariser.git
cd Whatsummariser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (first-time setup):
```bash
python -c "import nltk; nltk.download('punkt')"
```

## Usage

1. Run the script:
```bash
python whatsapp_summary.py
or
python newS.py
```

2. Follow the on-screen instructions:
   - Scan the QR code when prompted
   - Enter the exact group name
   - Specify number of messages to summarize

3. View your summary in the terminal!

## Example Output

```
WhatsApp Summarizer
------------------
Enter exact group name: Project Team
Number of messages to summarize: 50

✓ Group selected
Loaded 50/50 messages

📝 Summary: 
The team discussed the upcoming project deadline. Key tasks include completing the 
frontend by Friday and preparing documentation. Several members volunteered for 
specific components. The next meeting is scheduled for Thursday at 2PM.

👥 Top Participants:
- Alice (15 messages)
- Bob (12 messages)
- Carol (8 messages)
```

## Troubleshooting

**Common Issues:**
- `ChromeDriver` errors: Ensure you have Chrome installed and updated
- `NLTK data` errors: Run the NLTK download command again
- Group not found: Verify the exact group name including emojis/capitalization

## Requirements

- Python 3.8+
- Google Chrome browser
- Active WhatsApp account
- Stable internet connection

## License

MIT License - Free for personal and educational use

---

💡 **Tip**: For best results, summarize conversations with 50+ messages. The more input, the better the summary!
