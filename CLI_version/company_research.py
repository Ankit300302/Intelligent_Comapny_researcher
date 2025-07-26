import ollama
import requests
import time
from bs4 import BeautifulSoup
import json
import feedparser
from collections import defaultdict

class CompanyAgent:
    def __init__(self):
        # Use smaller models
        self.llm_model = "gemma:2b"  
        self.summary_model = "phi"   

        
        self.max_text_length = 1000  # Characters to process
        self.max_results = 3

        # Configuring rate limiting
        self.request_delay = 2

    def research_company(self, company_name):
        """Simplified research pipeline"""
        print(f"\n🔍 Researching {company_name} (lightweight mode)...")

        # for Getting basic info from Wikipedia
        print("📖 Getting Wikipedia summary...")
        wiki_summary = self._get_wikipedia_summary(company_name)

        # for finding official website
        print("🌐 Finding website...")
        website = self._find_official_website(company_name)

        # Generating compact summary
        print("🧠 Generating summary...")
        summary = self._generate_compact_summary(company_name, wiki_summary, website)

        # Extracting key people, products, location
        print("🧾 Extracting extra info...")
        extra_info = self._extract_additional_info(company_name, wiki_summary)

        # checking for recent news headlines
        print("📰 Checking news...")
        news = self._get_news_headlines(company_name)

        return {
            "company_name": company_name,
            "website": website,
            "summary": summary,
            "key_people": extra_info["key_people"],
            "products_services": extra_info["products_services"],
            "locations": extra_info["locations"],
            "recent_news": news
        }

    def _get_wikipedia_summary(self, company_name):
        """Getting simplified Wikipedia summary"""
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={company_name}&prop=extracts&exintro=True&explaintext=True"
            response = requests.get(url, timeout=10)
            pages = response.json().get('query', {}).get('pages', {})
            return next(iter(pages.values())).get('extract', '')[:self.max_text_length]
        except:
            return None

    def _find_official_website(self, company_name):
        """Finding website with multiple attempts"""
        try:
            # Trying direct .com approach 
            if self._validate_website(f"https://www.{company_name.lower().replace(' ', '')}.com"):
                return f"https://www.{company_name.lower().replace(' ', '')}.com"

            # Fallback to search
            time.sleep(self.request_delay)
            dd_response = requests.get(
                f"https://api.duckduckgo.com/?q={company_name}+official+site&format=json",
                timeout=10
            ).json()
            return dd_response.get('AbstractURL', '')
        except:
            return ''

    def _validate_website(self, url):
        """Quick website validation"""
        try:
            return requests.head(url, timeout=5, allow_redirects=True).status_code == 200
        except:
            return False

    def _generate_compact_summary(self, company_name, context, website):
        """Generating summary with LLM model"""
        prompt = f"""In one short paragraph (max 3 sentences), describe {company_name}.
        {f"Website: {website}" if website else ""}
        Context: {context[:500] if context else "No context available"}"""

        try:
            response = ollama.generate(
                model=self.llm_model,
                prompt=prompt,
                options={'num_predict': 100}  # Limit output size
            )
            return response['response']
        except:
            return "Summary unavailable"

    def _extract_additional_info(self, company_name, context):
        """Extracting key people, products/services, and global presence using compact prompts"""
        def ask_ollama(prompt):
            try:
                response = ollama.generate(
                    model=self.llm_model,
                    prompt=prompt,
                    options={'num_predict': 100}
                )
                return response['response'].strip()
            except:
                return "Information unavailable"

        info = {}
        if context:
            short_context = context[:800]

            info['key_people'] = ask_ollama(
                f"From the following context, list the key people (founders, CEO, leadership) of {company_name}:\n{short_context}"
            )

            info['products_services'] = ask_ollama(
                f"From the following context, summarize the main products or services offered by {company_name}:\n{short_context}"
            )

            info['locations'] = ask_ollama(
                f"From the following context, describe the global presence or headquarters locations of {company_name}:\n{short_context}"
            )
        else:
            info['key_people'] = "No context available"
            info['products_services'] = "No context available"
            info['locations'] = "No context available"

        return info

    def _get_news_headlines(self, company_name):
        """Get only news headlines"""
        try:
            feed = feedparser.parse(
                f"https://news.google.com/rss/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"
            )
            return [entry.title for entry in feed.entries[:self.max_results]]
        except:
            return []

    def save_report(self, report, filename):
        """Save simplified report"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved to {filename}")

if __name__ == "__main__":
    
    print("⏳ Downloading lightweight models...")
    try:
        ollama.pull("gemma:2b")
        ollama.pull("phi")
    except:
        print("⚠️ Couldn't download models. Using minimal mode.")

    # Initializing agent
    agent = CompanyAgent()

    # Company Input 
    companies = ["Motorola","Apple"]  

    for company in companies:
        try:
            report = agent.research_company(company)
            agent.save_report(report, f"{company}_report.json")

            # Printing brief output
            print(f"\n📋 {company} Summary:")
            print(report['summary'])
            if report['website']:
                print(f"🌐 Website: {report['website']}")
            print(f"👥 Key People: {report['key_people']}")
            print(f"📦 Products/Services: {report['products_services']}")
            print(f"🌍 Locations: {report['locations']}")
            if report['recent_news']:
                print("📰 Recent News:")
                for news in report['recent_news']:
                    print(f"- {news}")
        except Exception as e:
            print(f"⚠️ Failed to research {company}: {str(e)}")
