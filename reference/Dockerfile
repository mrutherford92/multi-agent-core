FROM python:3.13-slim

# Install GitHub CLI (gh) and Git
# This is required because our underlying agent_tools.py shells out to GitHub API via gh
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy python dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP application code (uhura_mcp.py and agent_tools.py)
COPY . .

# Assume Cloud Run injects PORT natively (usually 8080)
ENV PORT=8080
EXPOSE ${PORT}

# Run the FastMCP server securely
CMD ["sh", "-c", "python uhura_mcp.py --serve --port ${PORT}"]
