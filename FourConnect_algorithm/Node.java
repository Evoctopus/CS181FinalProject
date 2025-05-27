public class Node implements Comparable<Node> {
    private int value;
    private final int col;
    private final double ucb;

    Node (int col) {
        this.value = 0;
        this.col = col;
        this.ucb = 0;
    }

    public int getMove() {
        return col;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    public double getUCB() {
        return this.ucb;
    }

    @Override
    public int compareTo(Node o) {
        return Double.compare(ucb, o.getUCB());
    }
}
    