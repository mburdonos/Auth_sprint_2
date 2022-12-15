from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from core.config import configs


def configure_tracer() -> None:
    resource = Resource(attributes={SERVICE_NAME: configs.project_name})
    jaeger_exporter = JaegerExporter(
        agent_host_name=configs.jaeger_host, agent_port=configs.jaeger_port
    )

    provider = TracerProvider(resource=resource)
    jaeger_processor = BatchSpanProcessor(jaeger_exporter)

    provider.add_span_processor(jaeger_processor)
    trace.set_tracer_provider(provider)
