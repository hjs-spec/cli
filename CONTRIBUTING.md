# Contributing to HJS CLI

Thank you for your interest in contributing to **HJS CLI**, the command-line interface for the HJS protocol! We welcome contributions from everyone, whether you're fixing a bug, improving documentation, or proposing new features.

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold its standards. Reports can be sent to [signal@humanjudgment.org](mailto:signal@humanjudgment.org).

## Ways to Contribute

### 📝 Issues
Report bugs, suggest improvements, or ask questions via [GitHub Issues](https://github.com/hjs-protocol/cli/issues).

| Issue Type | Guidelines |
|------------|------------|
| **Bug reports** | Include steps to reproduce, expected behavior, and actual behavior |
| **Feature suggestions** | Explain the use case and alignment with HJS core primitives |
| **Questions** | Use issues for technical questions about the CLI |

### 🔧 Pull Requests
Submit code changes, fixes, or improvements.

1. **Fork** the repository
2. **Create a branch** (`git checkout -b feature/your-feature`)
3. **Make your changes**, following our guidelines
4. **Write tests** for new functionality
5. **Run linting** (`npm run lint` if available)
6. **Commit with clear messages** (see [Conventional Commits](https://www.conventionalcommits.org/))
7. **Push to your fork** and submit a Pull Request

### 💬 Discussions
Join the conversation on [GitHub Discussions](https://github.com/hjs-protocol/cli/discussions) or reach out via [signal@humanjudgment.org](mailto:signal@humanjudgment.org).

## Development Setup

### Prerequisites

- Node.js 18 or higher
- npm (comes with Node.js)
- Git

### Local Setup

```bash
# Clone the repository
git clone https://github.com/hjs-protocol/cli.git
cd cli

# Install dependencies
npm install

# Link the CLI locally
npm link

# Test the installation
hjs --help
