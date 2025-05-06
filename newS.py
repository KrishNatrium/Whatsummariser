from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import nltk
nltk.download('punkt_tab')
# Sumy imports with error handling
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    import nltk
    nltk.download('punkt', quiet=True)  # Download required tokenizer data
except ImportError:
    print("Error: Required packages not installed. Run: pip install sumy nltk")
    exit(1)

def get_summary(messages):
    """Generate text summary using Sumy"""
    if not messages:
        return "No messages to summarize"
    
    combined_text = " ".join(msg['text'] for msg in messages)
    try:
        parser = PlaintextParser.from_string(combined_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)  # Get 3-sentence summary
        return " ".join(str(s) for s in summary)
    except Exception as e:
        return f"Summary error: {str(e)}"

def main():
    try:
        group_name = input("Enter exact group name: ")
        n_messages = int(input("Number of messages to summarize: "))
        driver = webdriver.Chrome()
        driver.get('https://web.whatsapp.com')
        print("\nMANUAL STEPS:")
        print("1. Open WhatsApp Web in Chrome")
        print("2. Scan QR code with your phone")
        print("3. Wait until all chats appear")
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
            
            messages = list({msg['text']: msg for msg in messages}.values())
            print(f"\rLoaded {len(messages)}/{n_messages}", end='')
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Generate and show summary
        print("\n\n" + get_summary(messages[-n_messages:]))

    except Exception as e:
        print(f"\nERROR: {str(e)}")
    finally:
        driver.quit()
        print("\nDone")

if __name__ == "__main__":
    print("WhatsApp Summarizer")
    print("------------------")
    main()