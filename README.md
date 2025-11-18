# ThoughtStream: Intelligent Context-Aware Note-Taking Daemon

🚀 **Intelligent context-aware note-taking daemon for developers with local LLM integration (Ollama/Llama 3.2)**

Captures your dev/research workflow ethically: terminal commands, IDE files, browser tabs, voluntary clipboard/hotkeys. Segments sessions via git/pwd. Powers natural-language recall with local Ollama for zero-cloud embeddings & queries. Exports to Obsidian, suggests git commits. <15MB RAM, E2E privacy.

## 🌟 Key Features

### Smart Capture
- **Terminal Integration**: PTY proxy captures all commands and output
- **IDE Monitoring**: VSCode/JetBrains file tracking
- **Browser Activity**: Tab titles via xdotool
- **Voluntary Clipboard**: Manual capture on demand
- **Global Hotkeys**: Super+Shift+N for quick notes

### Local LLM Integration
- **Embeddings**: `nomic-embed-text` via Ollama (384-dim vectors)
- **Queries**: `llama3.2:3b` for semantic reranking & generation
- **Hybrid Search**: FTS5 + cosine similarity via `sqlite-vss`
- **Zero-Cloud**: All processing happens locally

### Intelligence
- **Session Detection**: Automatic context switching via git/pwd
- **Natural Language Recall**: Ask "what was I debugging with Redis last Thursday?"
- **Git Commit Suggestions**: Auto-generated from recent activity
- **Timeline Visualization**: Activity heatmap and context flow

### Privacy First
- **No Background Keylogging**: Opt-in capture only
- **Blacklist Support**: Exclude sensitive apps/directories
- **Encryption**: Age/GPG encryption at rest
- **Retention Policies**: Configurable data lifecycle
- **Audit Trail**: Full transparency of captured data

## 📦 Installation

### Prerequisites

```bash
# Ubuntu 22.04+, Python 3.10+
sudo apt install git curl xdotool evdev

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull required models
ollama pull nomic-embed-text llama3.2:3b
```

### One-Click Install

```bash
git clone https://github.com/kwizzlesurp10-ctrl/thoughtstream.git
cd thoughtstream
./scripts/install.sh
```

The installer will:
1. Create virtual environment
2. Install all dependencies
3. Setup systemd user service
4. Create config directory
5. Start the daemon

### Manual Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Copy config
mkdir -p ~/.config/thoughtstream
cp config.yaml.example ~/.config/thoughtstream/config.yaml

# Start daemon
thoughtstream daemon
```

## 🎯 Usage

### CLI Commands

```bash
# Start daemon (auto-starts via systemd)
systemctl --user start thoughtstream

# Natural language recall
thoughtstream recall "yesterday's postgres debug"
thoughtstream recall "API integration notes from last week"

# Visual timeline
thoughtstream timeline 24  # Last 24 hours

# Export to Obsidian/Notion
thoughtstream export obsidian

# View statistics
thoughtstream stats
```

### Quick Notes Hotkey

Press `Super+Shift+N` anywhere to capture clipboard content as a quick note.

### Configuration

Edit `~/.config/thoughtstream/config.yaml`:

```yaml
database:
  path: ~/.local/share/thoughtstream/thoughtstream.db
  retention_days: 30

llm:
  provider: ollama
  embedding_model: nomic-embed-text
  query_model: llama3.2:3b
  host: http://localhost:11434
  hybrid_search: true

capture:
  blacklist_apps: [firefox:password, chrome:banking]
  blacklist_dirs: [/etc, /var]
  poll_interval: 5

privacy:
  encrypt: false
  retention_policy: keep_all_except_blacklist

export:
  obsidian_vault: ~/Obsidian/Notes
```

## 🏗️ Architecture

```
thoughtstream/
├── daemon.py              # Async core daemon
├── db.py                  # SQLite + VSS + Ollama
├── intelligence.py        # Session logic + NL search
├── config.py              # YAML configuration
├── crypto.py              # Age encryption
└── capture/
    ├── terminal.py        # PTY proxy for commands
    ├── clipboard.py       # Pyperclip hook
    ├── hotkeys.py         # Pynput global hotkeys
    ├── vscode.py          # IDE file polling
    └── browser.py         # xdotool tab titles
```

## 🔧 Technical Details

### Dependencies
- **Python 3.10+**: Async/await support
- **SQLite + sqlite-vss**: Vector search extension
- **Ollama**: Local LLM inference
- **pynput**: Global hotkey capture
- **pyperclip**: Clipboard monitoring
- **Rich**: Terminal UI
- **Typer**: CLI framework

### Performance
- **Idle RAM**: <15MB
- **Query Time**: <50ms (FTS5 + vector hybrid)
- **Embedding Speed**: ~100 tokens/sec on CPU
- **Storage**: ~1MB per 1000 entries

## 🎭 Use Cases

- **ADHD Developers**: Context switching between multiple projects
- **Researchers**: Processing large amounts of information
- **Technical Writers**: Documenting workflows
- **Students**: Note-taking across multiple sources
- **Anyone**: Scattered thinking patterns and memory augmentation

## 🛡️ Privacy & Ethics

ThoughtStream is designed with privacy as the foundation:

✅ **Opt-in Only**: No background keylogging of GUI apps
✅ **Local Processing**: All LLM inference happens on your machine
✅ **Transparent**: Full audit trail of what's captured
✅ **Configurable**: Blacklist any app or directory
✅ **Encrypted**: Optional end-to-end encryption
✅ **Deletable**: Full control over data retention

### What ThoughtStream DOES NOT Do
- ❌ Global keystroke logging
- ❌ Password manager monitoring
- ❌ Banking app capture
- ❌ Cloud data transmission
- ❌ Hidden background processes

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Ollama**: Local LLM inference engine
- **sqlite-vss**: Vector similarity search
- **Grok AI**: Implementation assistance
- **xAI**: Project inspiration

## 📚 Documentation

For detailed documentation, see:
- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🚀 Roadmap

- [ ] Web UI dashboard
- [ ] Mobile companion app
- [ ] Obsidian plugin
- [ ] VSCode extension
- [ ] Git integration improvements
- [ ] Multi-language support
- [ ] Advanced analytics

---

**Built with Machiavellian precision: Capture chaos, reclaim genius. No cloud overlords.**

*ThoughtStream - Your context-aware memory augmentation system*
