# Dependencies Reference

This file serves as a requirements.txt equivalent for the OpenResume API Wrapper.

## Python Dependencies (Core)

```
fastapi>=0.116.0
uvicorn>=0.35.0
pydantic>=2.11.0
email-validator>=2.2.0
reportlab>=4.4.0
requests>=2.31.0
```

## Installation Commands

### Using pip
```bash
pip install fastapi>=0.116.0 uvicorn>=0.35.0 pydantic>=2.11.0 email-validator>=2.2.0 reportlab>=4.4.0 requests>=2.31.0
```

### Using uv (recommended for better performance)
```bash
uv pip install fastapi uvicorn pydantic email-validator reportlab requests
```

### Using conda
```bash
conda install -c conda-forge fastapi uvicorn pydantic email-validator reportlab requests
```

## Node.js Dependencies (OpenResume Integration)

The OpenResume source requires Node.js dependencies managed by npm:

```bash
cd openresume-source
npm install
```

Key OpenResume dependencies (auto-installed):
- `@react-pdf/renderer` - React PDF generation engine
- `react` - React framework  
- `next` - Next.js framework
- `typescript` - TypeScript support

## Development Dependencies (Optional)

For testing and development:
```bash
pip install pytest httpx black isort
```

## System Requirements

- **Python**: 3.11 or higher
- **Node.js**: 18.0 or higher  
- **npm**: 8.0 or higher
- **Memory**: 512MB minimum (1GB recommended)
- **Disk**: 100MB for dependencies + 60MB for OpenResume source

## Verification

After installation, verify all dependencies:

```bash
# Check Python dependencies
python -c "import fastapi, uvicorn, pydantic, reportlab; print('Python deps OK')"

# Check Node.js availability
node --version && npm --version

# Check OpenResume setup
cd openresume-source && npm list @react-pdf/renderer
```

## Troubleshooting

### Common Issues

1. **Python version too old**: Upgrade to Python 3.11+
2. **Node.js missing**: Install Node.js 18+ from nodejs.org
3. **OpenResume npm install fails**: Delete `node_modules` and retry
4. **ReportLab font issues**: Install system fonts or use built-in Helvetica

### Platform-Specific Notes

- **Windows**: May need Visual Studio Build Tools for some dependencies
- **macOS**: Xcode Command Line Tools recommended
- **Linux**: Standard build tools usually sufficient