from app.payments import PagoTarjeta  # o PagoPayPal, PagoCrypto, etc.
from app.services import PedidoService
from app.cli import PedidoCLI


def main() -> None:
    metodo_pago = PagoTarjeta()
    service = PedidoService(metodo_pago)
    cli = PedidoCLI(service)
    cli.ejecutar_demo()


if __name__ == "__main__":
    main()
