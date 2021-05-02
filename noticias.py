import sys
import os
import feedparser
from datetime import datetime
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib
from gi.repository.WebKit2 import WebView, Settings


UI_FILE = "noticias.glade"
CSS_FILE = "estilos.css"


class GUI:
    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)

        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_path(CSS_FILE)
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.builder.connect_signals(self)

        self.etiqueta = self.builder.get_object("label1")
        GLib.timeout_add_seconds(20, self.timer)

        self.fuente = 'http://www.20minutos.es/rss'
        self.seleccion = self.builder.get_object("rb20min")
        
        self.liststore = Gtk.ListStore(str)
        self.cell = Gtk.CellRendererText()
        self.col = Gtk.TreeViewColumn("Titular", self.cell, text=0)
        self.col.set_resizable(False)

        window = self.builder.get_object('window1')
        window.show_all()

    def on_window1_show(self, window):
        self.seleccion.set_active(True)
        
        d = feedparser.parse(self.fuente)
        treeview = self.builder.get_object('tv1')
        treeview.set_model(self.liststore)
        treeview.append_column(self.col)
        for i in d['entries']:
            self.liststore.append([i['title']])
        web = self.builder.get_object("webview1")
        web.load_html("No ha seleccionado ninguna noticia")

    def on_window1_destroy(self, window):
        Gtk.main_quit()

    def timer(self):
        ahora = datetime.now()
        actual = ahora.strftime('Hoy es %d/%m/%Y y son las %H:%Mh')
        self.etiqueta.set_text(actual)
        return True

    def llenar_treeview(self):
        self.liststore.clear()
        d = feedparser.parse(self.fuente)
        treeview = self.builder.get_object('tv1')
        treeview.set_model(self.liststore)
        treeview.append_column(self.col)
        for i in d['entries']:
            self.liststore.append([i['title']])

    def on_rb20min_toggled(self, radiobutton):
        self.fuente = 'http://www.20minutos.es/rss'
        self.llenar_treeview()

    def on_rbMarca_toggled(self, radiobutton):
        self.fuente = 'http://estaticos.marca.com/rss/portada.xml'
        self.llenar_treeview()

    def on_rbMuy_toggled(self, radiobutton):
        self.fuente = 'https://www.muyinteresante.es/rss'
        self.llenar_treeview()

    def on_rbMundo_toggled(self, radiobutton):
        self.fuente = 'http://rss.elmundo.es/rss/descarga.htm?data2=13'
        self.llenar_treeview()

    def on_rbPeriodico_toggled(self, radiobutton):
        self.fuente = 'https://www.elperiodico.com/es/rss/rss_portada.xml'
        self.llenar_treeview()

    def on_rbAs_toggled(self, radiobutton):
        self.fuente = 'https://as.com/rss/tags/ultimas_noticias.xml'
        self.llenar_treeview()

    def on_rbPais_toggled(self, radiobutton):
        self.fuente = 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada'
        self.llenar_treeview()

    def on_rbInvest_toggled(self, radiobutton):
        self.fuente = 'https://www.investigacionyciencia.es/rss/noticias'
        self.llenar_treeview()

    def on_rbAbc_toggled(self, radiobutton):
        self.fuente = 'https://www.abc.es/rss/feeds/abcPortada.xml'
        self.llenar_treeview()

    def on_rbConfidencial_toggled(self, radiobutton):
        self.fuente = 'https://rss.elconfidencial.com/tags/otros/cine-7354/'
        self.llenar_treeview()

    def on_rbConfidencialEco_toggled(self, radiobutton):
        self.fuente = 'https://rss.elconfidencial.com/economia/'
        self.llenar_treeview()

    def on_rbConfidencialTec_toggled(self, radiobutton):
        self.fuente = 'https://rss.elconfidencial.com/tecnologia/'
        self.llenar_treeview()

    def on_rbEuropaCul_toggled(self, radiobutton):
        self.fuente = 'https://www.europapress.es/rss/rss.aspx?ch=00126'
        self.llenar_treeview()

    def on_rbEuropaSoc_toggled(self, radiobutton):
        self.fuente = 'https://www.europapress.es/rss/rss.aspx?ch=00073'
        self.llenar_treeview()

    def on_tv1_cursor_changed(self, treeview):
        path, _ = treeview.get_cursor()
        if path is not None:
            indices = path.get_indices()
            d = feedparser.parse(self.fuente)
            variable = d['entries'][indices[0]]['summary']
            web = self.builder.get_object("webview1")
            web.load_html(variable)
            


def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
