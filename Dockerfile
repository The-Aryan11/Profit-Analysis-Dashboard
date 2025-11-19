# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Install Python packages ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy the rest of the code ----------
COPY . .

# ---------- Streamlit runs on port 8501 ----------
EXPOSE 8501

# ---------- Run the dashboard ----------
CMD ["streamlit", "run", "app/profit_dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]