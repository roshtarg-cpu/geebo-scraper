# 🔍 Geebo Scraper - AI-Powered Local Classifieds Extractor

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-00D4FF?style=flat-square)](https://apify.com/fervent_bus/geebo-scraper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![AI Agent Compatible](https://img.shields.io/badge/AI-Claude%20%7C%20ChatGPT%20%7C%20MCP-blueviolet?style=flat-square)](https://apify.com)

Extract structured data from **Geebo.com** classifieds with this powerful scraper. Built for developers, AI agents (Claude, ChatGPT), and automation workflows via **Apify MCP integration**.

---

## ✨ Features

- 🤖 **AI Agent Ready** - Works seamlessly with Claude, ChatGPT, and other AI agents via Apify MCP
- 🔄 **Full Category Coverage** - Jobs, housing, for-sale, services, community, gigs
- 🌍 **Location Filtering** - Target any city or metro area
- 🏷️ **Price Range Filters** - Set min/max price boundaries
- 📊 **Multiple Export Formats** - JSON, CSV, Excel, HTML
- ⚡ **Fast & Reliable** - Optimized browser automation with anti-detection
- 🛡️ **Proxy Support** - Residential proxies included for reliability
- 🔍 **Rich Data Fields** - Title, price, location, description, images, and more

---

## 🚀 Quick Start

### Via Apify Console
1. Go to [Apify Console](https://console.apify.com/actors/fervent_bus~geebo-scraper)
2. Configure input fields (category, location, max results)
3. Click **Run** and download results

### Via API (Python)
```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_TOKEN')

run = client.actor('fervent_bus/geebo-scraper').call(run_input={
    'category': 'jobs',
    'location': 'San Francisco',
    'maxResults': 50
})

# Fetch results
items = client.dataset(run['defaultDatasetId']).list_items().items
for item in items:
    print(f"{item['title']} - {item['price']}")
```

### Via API (JavaScript)
```javascript
const ApifyClient = require('apify-client');

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });

const run = await client.actor('fervent_bus/geebo-scraper').call({
    category: 'housing',
    location: 'Austin',
    maxResults: 50
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
items.forEach(item => console.log(item));
```

### Via cURL
```bash
curl -X POST https://api.apify.com/v2/acts/fervent_bus~geebo-scraper/runs \
  -H "Authorization: Bearer YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"category": "jobs", "location": "New York", "maxResults": 50}'
```

---

## 📥 Input Configuration

| Field | Type | Description | Required | Default |
|-------|------|-------------|----------|---------|
| `category` | String | Category to scrape (jobs, housing, for-sale, services, community, personals, gigs) | ❌ | jobs |
| `location` | String | City, state, or metro area to filter results | ❌ | New York |
| `minPrice` | Integer | Minimum price filter (0 for no limit) | ❌ | 0 |
| `maxPrice` | Integer | Maximum price filter (999999 for no limit) | ❌ | 999999 |
| `maxResults` | Integer | Maximum results to scrape (1-10000) | ❌ | 3 |
| `proxyConfiguration` | Object | Proxy settings (RESIDENTIAL group recommended) | ❌ | RESIDENTIAL |

---

## 📤 Output Structure

```json
[
  {
    "url": "https://www.geebo.com/new-york/jobs/details/123456",
    "title": "Software Engineer - Full Stack",
    "price": "$120,000",
    "currency": "USD",
    "location": "New York, NY",
    "description": "We are seeking a talented Full Stack Software Engineer...",
    "image": "https://www.geebo.com/images/listing/123456.jpg",
    "category": "jobs",
    "scrapedAt": "2026-09-26T10:30:00.000Z"
  }
]
```

### Field Descriptions

- **url**: Direct link to the listing page
- **title**: Listing title or job/item name
- **price**: Listed price (if applicable)
- **currency**: Price currency (usually USD)
- **location**: City, state, or full address
- **description**: Full listing description (truncated to 500 chars)
- **image**: Main listing image URL
- **category**: Category of the listing
- **scrapedAt**: ISO timestamp when data was collected

---

## 💡 Use Cases

### 🎯 Lead Generation
Extract job postings, service providers, and business contacts for sales outreach and recruitment.

### 📊 Market Research
Monitor pricing trends, inventory levels, and competitor activity across local markets.

### 🏠 Real Estate Tracking
Track housing and rental listings, price changes, and availability in your target markets.

### 💼 Job Aggregation
Build custom job boards by aggregating postings from multiple cities and categories.

### 🤖 AI Agent Workflows
Integrate with Claude Code, ChatGPT plugins, or custom AI agents via Apify MCP for automated data collection and analysis.

### 📈 Business Intelligence
Aggregate local market data for strategic decision-making and trend analysis across regions.

### 🛒 Price Monitoring
Set up automated price tracking for specific items or services across categories and locations.

---

## ❓ FAQ

### What categories can I scrape?
Jobs, housing, for-sale, services, community, personals, and gigs. Select via the `category` input field.

### Can I filter by location?
Yes! Use the `location` field to target any city, state, or metro area (e.g., "San Francisco", "Austin, TX").

### Does it handle pagination?
The scraper extracts up to your `maxResults` limit from the initial search results. For deeper pagination, increase `maxResults`.

### Can I use proxies?
Absolutely. We recommend using **RESIDENTIAL** proxy group (default) for best results. Configure via `proxyConfiguration` input.

### What export formats are supported?
JSON, CSV, Excel (XLSX), HTML, RSS, and XML. Download from Apify Console or fetch via API.

### Is it compatible with AI agents?
✅ **Yes!** This actor works with Claude Code, ChatGPT, and other AI agents through **Apify MCP integration**. Use it directly from your AI assistant.

### How often can I run it?
As often as you need! Runs are limited only by your Apify subscription plan.

### Does it bypass anti-bot protection?
Yes, we use Camoufox browser with fingerprinting, residential proxies, and adaptive strategies to handle detection systems.

---

## 💰 Pricing

| Event Type | Price | Description |
|------------|-------|-------------|
| 💵 **Per Result** | $0.005 | Each listing/item scraped |
| 🚀 **Actor Start** | $0.05 | One-time fee per run |

**Example:** Scraping 100 results = $0.05 (start) + $0.50 (100 × $0.005) = **$0.55 total**

Runs on Apify's usage-based pricing. Residential proxies and compute time included.

[View detailed pricing](https://apify.com/fervent_bus/geebo-scraper/pricing)

---

## 🔗 Links

- 🏠 [Actor Page](https://apify.com/fervent_bus/geebo-scraper)
- 📚 [Apify Documentation](https://docs.apify.com)
- 💬 [Support](https://console.apify.com/actors/fervent_bus~geebo-scraper/issues)
- 🐙 [GitHub Repository](https://github.com/roshtarg-cpu/geebo-scraper)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with ❤️ for developers and AI agents. Compatible with Claude, ChatGPT & AI automation via Apify MCP.**
