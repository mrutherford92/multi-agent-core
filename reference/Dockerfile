FROM python:3.13-slim

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
