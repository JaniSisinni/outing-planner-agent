# 🌤️ Outing Planner Agent

An AI-powered agent that recommends personalized outing ideas based on your **budget**, **group size**, **current weather**, and **location** — all through a conversational web chat interface.

Built with **Claude (Anthropic)**, **OpenWeatherMap**, and **Google Maps API**.

---

## ✨ Features

- 💬 **Conversational Chat UI** — talk naturally about your budget and plans
- 🌦️ **Real-time Weather** — checks current conditions via OpenWeatherMap
- 📍 **Location-Aware** — finds nearby venues using Google Maps
- 💰 **Budget-Conscious** — filters ideas to fit your wallet
- 👥 **Group-Friendly** — scales suggestions to your group size
- 🎯 **3 Curated Ideas** — always returns exactly 3 ranked recommendations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              Web Chat UI (Flask)            │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│          Claude Agent (Orchestrator)        │
│     anthropic tool_use / function calling   │
└──────┬──────────────┬──────────────┬────────┘
       │              │              │
┌──────▼──────┐ ┌─────▼─────┐ ┌────▼────────┐
│   Weather   │ │   Maps    │ │   Budget    │
│    Tool     │ │   Tool    │ │   Parser    │
│OpenWeatherMap│ │Google Maps│ │  (internal) │
└─────────────┘ └───────────┘ └─────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/outing-planner-agent.git
cd outing-planner-agent
```

### 2. Set up environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API keys

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run the app

```bash
python src/app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🔑 Environment Variables

| Variable | Description | Where to get it |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API key | [console.anthropic.com](https://console.anthropic.com) |
| `OPENWEATHERMAP_API_KEY` | Weather data | [openweathermap.org/api](https://openweathermap.org/api) |
| `GOOGLE_MAPS_API_KEY` | Places & Maps | [console.cloud.google.com](https://console.cloud.google.com) |

---

## 📁 Project Structure

```
outing-planner-agent/
├── src/
│   ├── app.py                  # Flask app entry point
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── orchestrator.py     # Claude agent loop
│   │   └── prompts.py          # System prompts
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather_tool.py     # OpenWeatherMap integration
│   │   ├── maps_tool.py        # Google Maps Places integration
│   │   └── tool_registry.py    # Tool definitions for Claude
│   └── ui/
│       ├── templates/
│       │   └── index.html      # Chat interface
│       └── static/
│           ├── style.css
│           └── chat.js
├── tests/
│   ├── test_weather_tool.py
│   ├── test_maps_tool.py
│   └── test_agent.py
├── docs/
│   └── architecture.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

1. User describes their plans (e.g. *"I have $50, going out with 3 friends this evening"*)
2. Claude identifies **budget**, **group size**, and asks for or detects **location**
3. Agent calls **WeatherTool** → gets current conditions and forecast
4. Agent calls **MapsTool** → searches for relevant nearby places
5. Claude synthesizes everything and returns **3 ranked outing suggestions**
6. Each suggestion includes: venue name, estimated cost per person, weather suitability, and a map link

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM / Agent | Anthropic Claude (`claude-sonnet-4-20250514`) |
| Backend | Python 3.11+, Flask |
| Weather | OpenWeatherMap API |
| Location | Google Maps Places API |
| Frontend | HTML/CSS/Vanilla JS |
| Testing | pytest |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss what you'd like to change.
