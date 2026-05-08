<div align="center">

# Pet Care Ai MCP

**Pet Care AI MCP Server - Pet Management Intelligence**

[![PyPI](https://img.shields.io/pypi/v/meok-pet-care-ai-mcp)](https://pypi.org/project/meok-pet-care-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Pet Care AI MCP Server - Pet Management Intelligence
Built by MEOK AI Labs | https://meok.ai

Feeding schedules, vaccination tracking, breed identification,
health symptom checking, and training recommendations.

## Tools

| Tool | Description |
|------|-------------|
| `generate_feeding_schedule` | Generate a tailored feeding schedule for a pet. |
| `track_vaccinations` | Track vaccination status and generate upcoming schedule. |
| `identify_breed` | Identify likely breed from physical and behavioral characteristics. |
| `check_health_symptoms` | Check pet health symptoms and get guidance on urgency and next steps. |
| `get_training_recommendations` | Get personalized training recommendations for a pet. |

## Installation

```bash
pip install meok-pet-care-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "pet-care-ai": {
      "command": "python",
      "args": ["-m", "meok_pet_care_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
