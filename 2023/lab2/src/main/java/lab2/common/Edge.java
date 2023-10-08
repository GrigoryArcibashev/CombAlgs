package lab2.common;

public class Edge {
    private static final double FLOATING_POINT_EPSILON = 1E-10;
    private final int v;
    private final int w;
    private final double capacity;
    private double flow;

    public Edge(int v, int w, double capacity) {
        if (v < 0) throw new IllegalArgumentException("Индекс вершины должен быть неотрицательным целым числом");
        if (w < 0) throw new IllegalArgumentException("Индекс вершины должен быть неотрицательным целым числом");
        if (!(capacity >= 0.0))
            throw new IllegalArgumentException("Пропускная способность ребра должна быть неотрицательной");
        this.v = v;
        this.w = w;
        this.capacity = capacity;
        this.flow = 0.0;
    }

    public int from() {
        return v;
    }

    public int to() {
        return w;
    }

    public double capacity() {
        return capacity;
    }

    public double flow() {
        return flow;
    }

    /**
     * Возвращает конечную точку ребра, которая отличается от заданной вершины
     *
     * @param vertex одна конечная точка ребра
     * @return конечная точка ребра, которая отличается от заданной вершины
     */
    public int other(int vertex) {
        if (vertex == v) return w;
        else if (vertex == w) return v;
        else throw new IllegalArgumentException("Недопустимое ребро");
    }

    /**
     * Возвращает остаточную пропускную способность ребра в направлении
     * к заданной вершине {@code vertex}.
     *
     * @param vertex одна конечная точка ребра
     * @return остаточная пропускная способность ребра в направлении к данной вершине:
     * если {@code vertex} является хвостовой вершиной (получилось прямое ребро vw),
     * остаточная емкость равна {@code capacity() - flow()};
     * если {@code vertex} является головной вершиной (получилось обратное ребро wv),
     * то остаточная емкость равна {@code flow()}.
     */
    public double residualCapacityTo(int vertex) {
        if (vertex == v) return flow;                   // обратное ребро
        else if (vertex == w) return capacity - flow;   // прямое ребро
        else throw new IllegalArgumentException("Недопустимое ребро");
    }

    /**
     * Увеличивает поток по ребру в направлении к заданной вершине:
     * если {@code vertex} является хвостовой вершиной (получилось прямое ребро vw),
     * это увеличивает поток на ребре на {@code delta};
     * если {@code vertex} является головной вершиной (получилось обратное ребро wv),
     * это уменьшает поток на ребре на {@code delta}.
     *
     * @param vertex одна конечная точка ребра
     * @param delta  величина, на которую можно увеличить поток
     */
    public void addResidualFlowTo(int vertex, double delta) {
        if (!(delta >= 0.0)) throw new IllegalArgumentException("delta должна быть неотрицательной");

        if (vertex == v) flow -= delta;         // обратное ребро
        else if (vertex == w) flow += delta;    // прямое ребро
        else throw new IllegalArgumentException("Недопустимое ребро");

        // округление потока до 0 или пропускной способности
        if (Math.abs(flow) <= FLOATING_POINT_EPSILON)
            flow = 0;
        if (Math.abs(flow - capacity) <= FLOATING_POINT_EPSILON)
            flow = capacity;

        if (!(flow >= 0.0)) throw new IllegalArgumentException("Поток отрицательный");
        if (!(flow <= capacity)) throw new IllegalArgumentException("Поток превышает пропускную способность");
    }

    public String toString() {
        return v + "->" + w + " " + flow + "/" + capacity;
    }
}
