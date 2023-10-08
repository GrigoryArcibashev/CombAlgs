package lab2;

import lab2.common.Edge;
import lab2.common.Network;

import java.util.ArrayDeque;
import java.util.Queue;

public class FordFulkerson {
    private Edge[] edgeTo;      // edgeTo[v] = послежднее ребро в кратчайшем s->v пути
    private double value;       // текущее значение максимального потока

    /**
     * Вычисляет максимальный поток в сети {@code G}
     * из вершины {@code s} в вершину {@code t}.
     *
     * @param G сеть с заданным на ней потоком
     * @param s исток
     * @param t сток
     */
    public FordFulkerson(Network G, int s, int t) {
        value = 0;
        // Пока существует f-дополняющая (s,t)-цепь
        while (hasAugmentingPath(G, s, t)) {

            // Вычисление инкремента величины потока (min{delta(e): e принадлежит f-доп. (s,t)-цепи})
            double delta = Double.POSITIVE_INFINITY;
            for (int v = t; v != s; v = edgeTo[v].other(v))
                delta = Math.min(delta, edgeTo[v].residualCapacityTo(v));

            // Увеличение потока
            for (int v = t; v != s; v = edgeTo[v].other(v))
                edgeTo[v].addResidualFlowTo(v, delta);
            value += delta;
        }
    }

    /**
     * Возвращает значение максимального потока.
     *
     * @return значение максимального потока
     */
    public int value() {
        return (int) Math.round(value);
    }

    // Нахождение f-дополняющей (s,t)-цепи в остаточной сети с помощью ПВШ
    private boolean hasAugmentingPath(Network G, int s, int t) {
        edgeTo = new Edge[G.vertexCount()];               // Известен ли путь к этой вершине?
        // marked[v] = принадлежит ли s->v путь остаточному графу?
        boolean[] marked = new boolean[G.vertexCount()];  // Последнее ребро в пути

        // ПВШ
        Queue<Integer> queue = new ArrayDeque<>();
        queue.add(s);       // Занесение источника в очередь
        marked[s] = true;   // и его пометка
        while (!queue.isEmpty() && !marked[t]) {
            int v = queue.remove();
            for (Edge e : G.adj(v)) {
                int w = e.other(v);
                // Для каждого ребра к непомеченным вершинам (в остаточной сети) выполнить:
                if (e.residualCapacityTo(w) > 0 && !marked[w]) {
                    edgeTo[w] = e;      // Сохранение последнего ребра в пути
                    marked[w] = true;   // Пометка w, т.к. путь неизвестен
                    queue.add(w);       // и занесение его в очередь
                }
            }
        }
        // Есть ли f-дополняющая (s,t)-цепь?
        return marked[t];
    }
}