import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        anni = self._model.listaAnni
        forme = self._model.listaForma

        for a in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))

    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert("Inserire un anno")
            return
        else:
            anno = self._view.ddyear.value

        if self._view.ddshape.value is None:
            self._view.create_alert("Inserire una forma")
            return
        else:
            forma = self._view.ddshape.value

        self._model.buildGraph(forma, anno)
        nN, nE = self._model.getGraphSize()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nN} nodi e {nE} archi"))
        self._model.getAdiacenti()
        adiacenze = self._model.adiacenti
        for i in adiacenze:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {i[0].id}, somma pesi sugli archi = {i[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        if self._model.graph is None:
            self._view.create_alert("Creare il grafo")
            return

        bestPath, bestWeight = self._model.getBestPath()
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo {bestWeight}"))
        for n in range(len(bestPath)-1):
            v0 = bestPath[n]
            v1 = bestPath[n+1]
            self._view.txtOut2.controls.append(ft.Text(f"{v0.id} --> {v1.id}: weight {self._model.getWeight(v0,v1)}  distance: {self._model.calcolaDistanzaSingola(v0,v1)}"))
        self._view.update_page()
