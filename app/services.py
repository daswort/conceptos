from __future__ import annotations

from .models import Pedido, Notificable, Facturable
from .payments import MetodoPago


class PedidoService:
    """
    SRP: responsable de la lógica de procesamiento de pedidos,
    no de la UI.

    DIP: depende de la abstracción MetodoPago, no de una implementación concreta.
    """

    def __init__(self, metodo_pago: MetodoPago):
        self.metodo_pago = metodo_pago

    def procesar_pedido(self, pedido: Pedido) -> None:
        print("=" * 60)
        print(f"Procesando {pedido.descripcion_canal()} #{pedido.id_pedido}")
        print(f"Cliente: {pedido.cliente}")
        print("Items:")
        for item in pedido.items:
            print(f"- {item.nombre} x{item.cantidad} = {item.subtotal():.2f}")

        total = pedido.calcular_total()
        print(f"Total a pagar: {total:.2f}")

        if not self.metodo_pago.pagar(total):
            print("ERROR: Pago rechazado")
            return

        print("Pago aprobado.")

        # ISP en acción: solo si el pedido es Facturable, generamos factura
        if isinstance(pedido, Facturable):
            factura = pedido.generar_factura()
            print("\n--- FACTURA ---")
            print(factura)
            print("---------------")

        # ISP en acción: solo si el pedido es Notificable, enviamos notificación
        if isinstance(pedido, Notificable):
            pedido.enviar_notificacion()

        print("Pedido procesado correctamente.")
