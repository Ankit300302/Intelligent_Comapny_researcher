# agent.py
import ollama
import requests
import time
import feedparser
import json

class CompanyAgent:
    def __init__(self):
        self.llm_model = "gemma:2b"
        self.summary_model = "phi"
        self.max_text_length = 1000
        self.max_results = 3
        self.request_delay = 2

    def research_company(self, company_name):
        wiki_summary = self._get_wikipedia_summary(company_name)
        website = self._find_official_website(company_name)
        summary = self._generate_compact_summary(company_name, wiki_summary, website)
        extra_info = self._extract_additional_info(company_name, wiki_summary)
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
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={company_name}&prop=extracts&exintro=True&explaintext=True"
            response = requests.get(url, timeout=10)
            pages = response.json().get('query', {}).get('pages', {})
            return next(iter(pages.values())).get('extract', '')[:self.max_text_length]
        except:
            return None

    def _find_official_website(self, company_name):
        try:
            if self._validate_website(f"https://www.{company_name.lower().replace(' ', '')}.com"):
                return f"https://www.{company_name.lower().replace(' ', '')}.com"
            time.sleep(self.request_delay)
            dd_response = requests.get(
                f"https://api.duckduckgo.com/?q={company_name}+official+site&format=json",
                timeout=10
            ).json()
            return dd_response.get('AbstractURL', '')
        except:
            return ''

    def _validate_website(self, url):
        try:
            return requests.head(url, timeout=5, allow_redirects=True).status_code == 200
        except:
            return False

    def _generate_compact_summary(self, company_name, context, website):
        prompt = f"""In one short paragraph (max 3 sentences), describe {company_name}.
        {f"Website: {website}" if website else ""}
        Context: {context[:500] if context else "No context available"}"""

        try:
            response = ollama.generate(
                model=self.llm_model,
                prompt=prompt,
                options={'num_predict': 100}
            )
            return response['response']
        except:
            return "Summary unavailable"

    def _extract_additional_info(self, company_name, context):
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
        try:
            feed = feedparser.parse(
                f"https://news.google.com/rss/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"
            )
            return [entry.title for entry in feed.entries[:self.max_results]]
        except:
            return []

