# Pillar 7: The Storyteller

## Research Problem
**Content Accessibility**: Guidebooks are boring; human guides are expensive.

## Solution Logic
**Generative Audio**: Retrieves history vectors from ChromaDB and uses fine-tuned Llama 3 to rewrite them as engaging scripts, streamed via TTS.

## Technology
- **LLM**: Fine-tuned Llama 3.1 8B (via Unsloth/LoRA)
- **TTS**: gTTS or Azure Speech Services
- **Vector Retrieval**: ChromaDB semantic search

## Fine-tuning Setup
- **Framework**: Unsloth + LoRA (2-5x faster, 80% less memory)
- **Dataset**: 343 Alpaca-format examples
- **Base Model**: Meta-Llama-3.1-8B-Instruct (4-bit quantized)

## System Prompt
```
You are an expert Sri Lankan Tour Guide with warm hospitality.
You blend historical facts with engaging storytelling.
```

## Workflow
1. User requests story for "Sigiriya"
2. Retrieve `sigiriya_history` vector from ChromaDB
3. LLM generates engaging narrative
4. TTS converts to audio stream
5. User hears: "Legend says King Kashyapa built this fortress..."

## Status: PIPELINE READY (Training not executed)

## Files
```
pillar_7_storyteller/
├── notebooks/
│   └── llm_finetuning_sri_lankan_tour_guide.ipynb  # Unsloth setup
└── data/
    └── finetune_dataset_metadata.json              # 343 examples metadata
```

## Export Options
- GGUF (for Ollama local deployment)
- HuggingFace Hub
- LoRA adapters only
