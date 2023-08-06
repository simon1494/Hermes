from screeninfo import get_monitors


class VentanaBase:
    @staticmethod
    def centrar_ventana(window_width, window_heigth):
        monitores = get_monitors()
        if monitores:
            primer_monitor = monitores[0]
            screen_width = primer_monitor.width
            screen_heigth = primer_monitor.height
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_heigth / 2 - window_heigth / 2)
        return f"{window_width}x{window_heigth}+{center_x}+{center_y}"
