import argparse
import base64
import json
import mimetypes
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from prompts import INVOICE_PROMPT, MEDICAL_PROMPT

load_dotenv()

OPENAI_PRICES_PER_1M = {
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50},
    "gpt-5.5": {"input": 5.00, "output": 30.00},
}


def encode_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def get_prompt(workflow: str) -> str:
    if workflow == "invoice":
        return INVOICE_PROMPT
    if workflow == "medical":
        return MEDICAL_PROMPT
    raise ValueError("workflow must be either 'invoice' or 'medical'")


def estimate_cost(model: str, usage) -> float | None:
    prices = OPENAI_PRICES_PER_1M.get(model)
    if not prices or not usage:
        return None

    input_tokens = getattr(usage, "input_tokens", 0) or 0
    output_tokens = getattr(usage, "output_tokens", 0) or 0

    return (
        input_tokens / 1_000_000 * prices["input"]
        + output_tokens / 1_000_000 * prices["output"]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to PDF or image file")
    parser.add_argument("--workflow", required=True, choices=["invoice", "medical"])
    parser.add_argument("--runs", type=int, default=1)
    args = parser.parse_args()

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

    file_path = Path(args.file)
    prompt = get_prompt(args.workflow)
    mime_type, _ = mimetypes.guess_type(file_path)

    results = []

    for run_idx in range(1, args.runs + 1):
        base64_data = encode_file(file_path)

        if file_path.suffix.lower() == ".pdf":
            document_block = {
                "type": "input_file",
                "filename": file_path.name,
                "file_data": f"data:application/pdf;base64,{base64_data}",
            }
        elif mime_type and mime_type.startswith("image/"):
            document_block = {
                "type": "input_image",
                "image_url": f"data:{mime_type};base64,{base64_data}",
            }
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        start = time.perf_counter()

        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": [
                        document_block,
                        {"type": "input_text", "text": prompt},
                    ],
                }
            ],
        )

        end = time.perf_counter()
        latency = end - start

        usage = getattr(response, "usage", None)
        cost = estimate_cost(model, usage)

        result = {
            "tool": "OpenAI API",
            "model": model,
            "document": file_path.name,
            "workflow": args.workflow,
            "run": run_idx,
            "latency_seconds": latency,
            "usage": usage.model_dump() if usage else None,
            "estimated_cost_usd": cost,
            "output": response.output_text,
        }

        results.append(result)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    output_path = Path("results") / f"openai_{file_path.stem}_{args.workflow}.json"
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()