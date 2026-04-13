# Pet Care AI MCP Server

**Pet Management Intelligence**

Built by [MEOK AI Labs](https://meok.ai)

---

An MCP server for pet owners and veterinary professionals. Generate feeding schedules, track vaccinations, identify breeds, check health symptoms, and get training recommendations for dogs and cats.

## Tools

| Tool | Description |
|------|-------------|
| `generate_feeding_schedule` | Generate calorie-calculated feeding schedules based on species, breed, weight, and activity |
| `track_vaccinations` | Track vaccination status with overdue alerts and upcoming schedule |
| `identify_breed` | Identify breed from physical and behavioral characteristics |
| `check_health_symptoms` | Check symptoms against veterinary database with urgency assessment |
| `get_training_recommendations` | Get personalized training plans for behavioral issues |

## Quick Start

```bash
pip install pet-care-ai-mcp
```

### Claude Desktop

```json
{
  "mcpServers": {
    "pet-care-ai": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "/path/to/pet-care-ai-mcp"
    }
  }
}
```

### Direct Usage

```bash
python server.py
```

## Rate Limits

| Tier | Requests/Hour |
|------|--------------|
| Free | 60 |
| Pro | 5,000 |

## License

MIT - see [LICENSE](LICENSE)

---

*Part of the MEOK AI Labs MCP Marketplace*
