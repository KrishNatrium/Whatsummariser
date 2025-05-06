import time
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


'''def summarize_messages(messages):
    """Generate a proper summary of the messages"""
    word_counts = defaultdict(int)
    senders = defaultdict(int)
    topics = set()

    for msg in messages:
        text = msg['text'].lower()
        senders[msg['sender']] += 1

        # Simple topic detection
        if any(word in text for word in ['test', 'exam', 'assignment']):
            topics.add('Academic Work')
        elif any(word in text for word in ['ppt', 'presentation']):
            topics.add('Presentations')
        elif any(word in text for word in ['project', 'product']):
            topics.add('Projects')

        for word in text.split():
            if len(word) > 3:  # Ignore short words
                word_counts[word] += 1

    # Get top 3 words
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        'total_messages': len(messages),
        'active_senders': dict(sorted(senders.items(), key=lambda x: x[1], reverse=True)),
        'main_topics': list(topics),
        'frequent_words': top_words
    }
'''


def summarize_messages(messages):
    """Returns a string summary of messages using Sumy"""
    if not messages:
        return "No messages to summarize"

    # Combine all messages into one text
    combined_text = " ".join(msg['text'] for msg in messages)

    # Setup Sumy
    parser = PlaintextParser.from_string(combined_text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    # Generate 3-sentence summary
    summary = summarizer(parser.document, 3)

    # Return as plain string
    return " ".join(str(sentence) for sentence in summary)

def main():
    driver = None
    try:
        # Use your working driver initialization

        group_name = input("Enter exact group name: ")
        n_messages = int(input("Number of messages to summarize: "))

        driver = webdriver.Chrome()
        driver.get('https://web.whatsapp.com')

        print("\nMANUAL STEPS:")
        print("1. Open WhatsApp Web in Chrome")
        print("2. Scan QR code")
        print("3. Wait for chats to load")
        input("4. Press Enter AFTER completing these steps...")

        # Search for group
        print(f"\nLocating {group_name}...")
        search_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.send_keys(group_name)
        time.sleep(2)

        # Select group
        group = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))
        )
        group.click()
        print("✓ Group selected")

        # Load messages
        print(f"\nLoading {n_messages} messages...")
        messages = []
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(messages) < n_messages:
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

            elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-pre-plain-text]')
            for el in elements[-n_messages:]:
                try:
                    meta = el.get_attribute('data-pre-plain-text')
                    sender = meta.split('] ')[1].split(':')[0]
                    text = el.find_element(By.CSS_SELECTOR, 'span.selectable-text').text
                    messages.append({'sender': sender, 'text': text})
                except:
                    continue

            # Remove duplicates
            messages = list({msg['text']: msg for msg in messages}.values())
            print(f"\rLoaded {len(messages)}/{n_messages}", end='')

            # Check if stuck
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Generate and display summary
        summary = summarize_messages(messages[-n_messages:])

        print(f"\n\nSUMMARY OF LAST {summary['total_messages']} MESSAGES:")
        print("\nMost Active Participants:")
        for sender, count in summary['active_senders'].items():
            print(f"- {sender}: {count} messages")

        print("\nMain Topics:")
        print("\n".join(f"- {topic}" for topic in summary['main_topics']) or "- No clear topics")

        print("\nFrequent Words:")
        for word, count in summary['frequent_words']:
            print(f"- '{word}' ({count}x)")

    except Exception as e:
        print(f"\nERROR: {str(e)}")
    finally:
        if driver:
            driver.quit()
        print("\nDone")


if __name__ == "__main__":
    print("WhatsApp Summarizer")
    print("------------------")
    main()