from typing import Union
from .agent_types import Agent1, Agent2, Agent3, Agent4, Agent5
from ..app.events.event_bus import EventBus


class AgentFactory:
    """
    Fábrica para crear instancias de agentes.

    Permite crear agentes por tipo sin hardcodear en application.py.
    """

    @staticmethod
    def create_agent(agent_type: Union[str, int], event_bus: EventBus):
        """
        Crea un agente del tipo especificado.

        Args:
            agent_type: Tipo de agente ('1', '2', '3', '4', '5' o int 1-5)
            event_bus: Bus de eventos para el agente

        Returns:
            Instancia del agente correspondiente

        Raises:
            ValueError: Si el tipo de agente no es válido
        """
        if isinstance(agent_type, int):
            agent_type = str(agent_type)

        if agent_type == '1':
            return Agent1(event_bus)
        elif agent_type == '2':
            return Agent2(event_bus)
        elif agent_type == '3':
            return Agent3(event_bus)
        elif agent_type == '4':
            return Agent4(event_bus)
        elif agent_type == '5':
            return Agent5(event_bus)
        else:
            raise ValueError(f"Tipo de agente desconocido: {agent_type}")
