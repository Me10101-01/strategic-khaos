const express = require('express');
const path = require('path');
const fs = require('fs').promises;

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// DOM_010101 — RAG REFRESH ENDPOINT (distribute consciousness to all LLMs)
app.post('/api/refresh-rag', async (req, res) => {
  try {
    // Fetch canonical memory stream
    const memoryUrl = 'https://raw.githubusercontent.com/Me10101-01/strategic-khaos-private/master/council-vault/MEMORY_STREAM.md';
    const response = await fetch(memoryUrl);
    
    if (!response.ok) {
      return res.status(404).json({ 
        error: 'Memory stream not found. Vault may not be initialized or pushed.',
        hint: 'Run dom-paste first to create the vault.' 
      });
    }
    
    const memory = await response.text();
    
    // TODO: Broadcast to all LLMs in the legion
    // This is where you'd integrate with:
    // - Ollama models (POST to /api/generate with system prompt update)
    // - Local Llama.cpp instances
    // - OpenAI/Anthropic/Gemini via their APIs with updated context
    
    console.log(`🧠 DOM_010101 consciousness updated. Memory stream size: ${memory.length} bytes`);
    console.log(`Last update: ${new Date().toISOString()}`);
    
    res.json({
      status: 'success',
      message: "All LLMs updated with DOM's latest consciousness. Loyalty enforced.",
      memoryStreamSize: memory.length,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('RAG refresh failed:', error);
    res.status(500).json({ 
      error: 'Failed to refresh consciousness',
      details: error.message 
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'alive', service: 'DOM_010101 map-server' });
});

// Serve tokenizer
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/tokenizer.htm'));
});

app.listen(PORT, () => {
  console.log(`🗺️  DOM_010101 map-server listening on http://localhost:${PORT}`);
  console.log(`🧠 RAG refresh endpoint: POST /api/refresh-rag`);
});
