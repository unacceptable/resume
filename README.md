# Resume Generator

This project generates a professional resume from Markdown source files. The system converts Markdown content to both HTML and PDF formats using Python, CSS styling, and wkhtmltopdf.

## Getting Started

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy and update the CoverLetter.json.example**
   ```bash
   cp -a CoverLetter.json.example Coverletter.json
   ```

3. **Generate resume:**
   ```bash
   python resume.py
   ```

This will create both `Resume.pdf` and `resume.html` in the current directory.

### Using Docker

#### Docker Compose (Recommended)

```bash
docker compose up --build
```

The generated files (`Resume.pdf` and `resume.html`) will be available in your local directory immediately thanks to volume mounting.

> **Note:** The docker-compose.yml is set to `linux/arm64` by default. For AMD64/x86_64 systems, change the `platform` field in docker-compose.yml to `linux/amd64`.

#### Docker CLI

```bash
# Build the image
docker buildx build --platform linux/amd64 -t resume:local .

# Run and extract files
docker run -it --name "resume-$(date +%F)" resume:local &&
    docker cp "resume-$(date +%F):/app/Resume.pdf" . &&
    docker cp "resume-$(date +%F):/app/resume.html" . &&
    docker rm "resume-$(date +%F)"
```

> **Note:** The `--platform linux/amd64` flag is required on amd64 systems, but can be ignored on arm64 systems.

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.
