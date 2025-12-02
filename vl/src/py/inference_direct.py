#!/usr/bin/env python3
"""
Direct Qwen3-VL inference without vLLM - minimal memory footprint.

vLLM has significant overhead for vision models. This script uses the
transformers library directly, which has much lower memory usage for
single inference runs.

Usage:
    python inference_direct.py /path/to/image.jpg
"""

import sys
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

def load_model():
    """Load model with memory optimization."""
    model_id = "Qwen/Qwen3-VL-2B-Instruct-FP8"

    print("Loading processor...")
    processor = AutoProcessor.from_pretrained(
        model_id,
        trust_remote_code=True
    )

    print("Loading model (this may take 30-60 seconds)...")
    # Load in FP8 format and keep on GPU
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    ).eval()

    return model, processor

def caption_image(image_path, model, processor):
    """Generate caption for image."""
    print(f"\nProcessing image: {image_path}")

    # Load image
    image = Image.open(image_path).convert('RGB')
    print(f"Image size: {image.size}")

    # Prepare input
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image,
                },
                {
                    "type": "text",
                    "text": "Describe this image in detail."
                }
            ],
        }
    ]

    # Process input
    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    image_inputs, video_inputs = processor.process_images(
        [image],
        return_tensors="pt",
        videos=None,
    )

    # Prepare inputs for model
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )

    # Move to GPU
    inputs = {k: v.to("cuda") if torch.is_tensor(v) else v for k, v in inputs.items()}

    # Generate caption
    print("Generating caption...")
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=256,  # Limit output
            temperature=0.7,
        )

    # Decode output
    caption = processor.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return caption

def main():
    if len(sys.argv) < 2:
        print("Usage: python inference_direct.py /path/to/image.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        # Load model once
        print("="*70)
        print("Qwen3-VL Direct Inference (No vLLM)")
        print("="*70)
        print("\nMemory usage will be ~3-4GB (much lower than vLLM)")
        print("\nLoading model...")

        model, processor = load_model()

        # Check VRAM
        torch.cuda.synchronize()
        print(f"\nGPU Memory after loading:")
        print(f"  Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
        print(f"  Reserved: {torch.cuda.memory_reserved() / 1e9:.2f} GB")

        # Generate caption
        caption = caption_image(image_path, model, processor)

        print("\n" + "="*70)
        print("Generated Caption:")
        print("="*70)
        print(caption)
        print("="*70)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
