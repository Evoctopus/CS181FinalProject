
public class NodeMC implements Comparable<NodeMC> {
    private final Game board;
    private final NodeMC parent;
    private final int col;
    private int timesWon;
    private float ucb;
    private int timesPassed;
    private NodeMC c1 = null, c2 = null, c3 = null, c4 = null, c5 = null, c6 = null, c0 = null;

    NodeMC (Game board, NodeMC parent, int col) {
        this.board = board;
        this.parent = parent;
        this.col = col;
        this.timesWon = 0;
        this.ucb = 0;
        this.timesPassed = 0;
    }

    public NodeMC getChild(int c) {
        return switch (c) {
            case 0 -> c0;
            case 1 -> c1;
            case 2 -> c2;
            case 3 -> c3;
            case 4 -> c4;
            case 5 -> c5;
            case 6 -> c6;
            default -> null;
        };
    }

    public void addChild(NodeMC child, int c) {
        switch (c) {
            case 0 -> c0 = child;
            case 1 -> c1 = child;
            case 2 -> c2 = child;
            case 3 -> c3 = child;
            case 4 -> c4 = child;
            case 5 -> c5 = child;
            case 6 -> c6 = child;
        }
    }

    public Game getGame() {
        return board;
    }

    public NodeMC getParent() {
        return parent;
    }


    public int getMove() {
        return col;
    }

    public double getUCB() {
        return this.ucb;
    }

    public void updateTimesWon() {
        this.timesWon++;
        updateUCB();
    }

    public void updateTimesLost() {
        this.timesWon--;
        updateUCB();
    }

    private void updateUCB() {
        this.ucb = (float) timesWon / (float) timesPassed;
    }

    public void updateTimesPassed() {
        this.timesPassed++;
        updateUCB();
    }

    @Override
    public int compareTo(NodeMC o) {
        if (ucb < o.getUCB()) return -1;
        if (ucb == o.getUCB()) return 0;
        return 1;
    }
}
