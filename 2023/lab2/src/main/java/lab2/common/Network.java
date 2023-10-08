package lab2.common;


import java.util.LinkedList;

public class Network {
    private final int vertexCount;
    private final LinkedList<Edge>[] edgesByVertex;

    /**
     * Инициализирует пустую (без рёбер) потоковую сеть с {@code vertexCount} вершинами.
     *
     * @param vertexCount количество вершин
     */
    public Network(int vertexCount) {
        if (vertexCount < 0)
            throw new IllegalArgumentException("Количество вершин в графе должно быть неотрицательным");
        this.vertexCount = vertexCount;
        edgesByVertex = new LinkedList[vertexCount];
        for (int v = 0; v < vertexCount; v++)
            edgesByVertex[v] = new LinkedList<>();
    }


    /**
     * Возвращает количество вершин в графе.
     *
     * @return количество вершин в графе
     */
    public int vertexCount() {
        return vertexCount;
    }

    /**
     * Добавляет ребро {@code e} в сеть.
     *
     * @param e ребро
     */
    public void addEdge(Edge e) {
        int v = e.from();
        int w = e.to();
        edgesByVertex[v].addFirst(e);
        edgesByVertex[w].addFirst(e);
    }

    /**
     * Возвращает рёбра, инцидентные вершине {@code v}.
     *
     * @param v вершина
     * @return рёбра, инцидентные вершине {@code v}
     */
    public Iterable<Edge> adj(int v) {
        return edgesByVertex[v];
    }

    public Iterable<Edge> edges() {
        LinkedList<Edge> list = new LinkedList<>();
        for (int v = 0; v < vertexCount; v++)
            for (Edge e : adj(v))
                if (e.to() != v)
                    list.add(e);
        return list;
    }
}