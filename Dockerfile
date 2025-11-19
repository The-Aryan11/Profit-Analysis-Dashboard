# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Install Python packages ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy the rest of the code ----------
COPY . .

# Streamlit listens on Vercel's port
EXPOSE 3000

# ---------- Run the dashboard ----------
CMD ["sh", "-c", "streamlit run app/profit_dashboard.py --server.port $PORT --server.address 0.0.0.0"]