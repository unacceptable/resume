# Robert's Resume

Hey team! I guess if you found this you're interested in how I am generating my
resume.

The 30k foot overview is that I store my resume as Markdown, then using python
and some css, render a PDF based on the contents.

## Rendering Resume

### install requirements

```bash
pip install -r requirements.txt
```

### run render script

```bash
python resume.py
```

### render with Docker

```bash
docker build -t resume:local .
```

```bash
docker run -it --name "resume-$(date +%F)" resume:local &&
    docker cp "resume-$(date +%F):/app/Resume.pdf" . &&
    docker cp "resume-$(date +%F):/app/resume.html" .
```
