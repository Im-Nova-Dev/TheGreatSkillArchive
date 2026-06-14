# OpenTelemetry GenAI Conventions for ML Inference

Standard semantic attributes for LLM/ML inference requests. Use these in gateway/router/model-server instrumentation.

## Core Attributes (GenAI Semantic Conventions v1.2+)

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.operation.name` | string | Operation type | `chat`, `completions`, `embeddings`, `rerank` |
| `gen_ai.request.model` | string | Model identifier | `gpt-4o`, `llama-3.1-70b`, `text-embedding-3-large` |
| `gen_ai.request.max_tokens` | int | Max output tokens requested | `4096` |
| `gen_ai.request.temperature` | float | Sampling temperature | `0.7` |
| `gen_ai.request.top_p` | float | Nucleus sampling | `0.95` |
| `gen_ai.request.frequency_penalty` | float | Frequency penalty | `0.0` |
| `gen_ai.request.presence_penalty` | float | Presence penalty | `0.0` |
| `gen_ai.request.stop_sequences` | string[] | Stop sequences | `["\\n\\n", "END"]` |

## Usage Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.usage.input_tokens` | int | Prompt tokens (fresh) | `1250` |
| `gen_ai.usage.output_tokens` | int | Completion tokens | `380` |
| `gen_ai.usage.cache_read_tokens` | int | Cached prompt tokens | `800` |
| `gen_ai.usage.cache_write_tokens` | int | Tokens written to cache | `1250` |

## Custom Attribution Attributes (Non-standard, for Cost Attribution)

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `ml.cost.tenant_id` | string | Tenant/team/project identifier | `team-platform`, `customer-acme` |
| `ml.cost.workflow_id` | string | Workflow/use-case identifier | `rag-qa`, `code-gen`, `batch-embed` |
| `ml.cost.request_id` | string | Unique request correlation ID | `req_abc123xyz` |
| `ml.cost.gpu_ms` | int | GPU compute milliseconds | `450` |
| `ml.cost.gpu_count` | int | Number of GPUs used | `1` |
| `ml.cost.cache_hit` | boolean | Whether prompt hit KV cache | `true` |
| `ml.cost.streaming` | boolean | Whether response was streamed | `true` |
| `ml.cost.egress_bytes` | int | Network egress bytes | `2048` |

## Example OpenTelemetry Span (Python)

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer("ml-gateway")

def record_inference_span(model_id, tenant_id, workflow_id, usage, gpu_ms, cache_hit, streaming):
    with tracer.start_as_current_span("ml.inference", kind=trace.SpanKind.SERVER) as span:
        # GenAI standard
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.request.model", model_id)
        span.set_attribute("gen_ai.usage.input_tokens", usage.prompt_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", usage.completion_tokens)
        if usage.cached_tokens:
            span.set_attribute("gen_ai.usage.cache_read_tokens", usage.cached_tokens)

        # Custom attribution
        span.set_attribute("ml.cost.tenant_id", tenant_id)
        span.set_attribute("ml.cost.workflow_id", workflow_id)
        span.set_attribute("ml.cost.gpu_ms", gpu_ms)
        span.set_attribute("ml.cost.cache_hit", cache_hit)
        span.set_attribute("ml.cost.streaming", streaming)
        span.set_attribute("ml.cost.request_id", generate_request_id())

        span.set_status(Status(StatusCode.OK))
```

## Prometheus Metrics Mapping

```prometheus
# Direct cost counters (increment per request)
ml_inference_prompt_tokens_total{model,tenant,workflow} 1250
ml_inference_completion_tokens_total{model,tenant,workflow} 380
ml_inference_cached_tokens_total{model,tenant,workflow} 800
ml_inference_gpu_ms_total{model,tenant,workflow} 450
ml_inference_requests_total{model,tenant,workflow} 1
ml_inference_egress_bytes_total{model,tenant,workflow} 2048

# Derived cost gauges (updated by attribution job)
ml_cost_attributed_usd{model,tenant,workflow,cost_type="input"} 0.003125
ml_cost_attributed_usd{model,tenant,workflow,cost_type="output"} 0.0038
ml_cost_attributed_usd{model,tenant,workflow,cost_type="gpu_shared"} 0.012
ml_cost_attributed_usd{model,tenant,workflow,cost_type="network_shared"} 0.0001
```