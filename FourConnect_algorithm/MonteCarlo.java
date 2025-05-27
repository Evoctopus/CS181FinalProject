import java.lang.Math;
import java.util.PriorityQueue;

public class MonteCarlo {
    private static final int SIMULATIONS = 4000;

    private static final PriorityQueue<NodeMC> q = new PriorityQueue<>();

    public static int monteCarloSearch(Game board) {
        if (q.isEmpty()) {
            NodeMC rootNode = new NodeMC(board, null, -1);
            q.add(rootNode);
        }

        NodeMC nGen;
        NodeMC bestMove = null;
        NodeMC explored = selection();

        for (int i = 0; i < 7; i++) {
            if (explored.getChild(i) == null) {
                nGen = new NodeMC(explored.getGame().play(i), explored, i);
                explored.addChild(nGen, i);
            }
            else nGen = explored.getChild(i);

            for (int j = 0; j < SIMULATIONS; j++)
                simulation(nGen);

            if ((bestMove == null || bestMove.getUCB() <= nGen.getUCB()) && explored.getGame().isColumnNotFull(nGen.getMove()))
                bestMove = nGen;
        }

        assert bestMove != null;
        return bestMove.getMove();
    }

    private static NodeMC selection() {
        return q.peek();
    }

    private static void simulation(NodeMC board) {
        NodeMC cur = board;

        while (!cur.getGame().isGameOver()) {
            cur.updateTimesPassed();
            int randomMove = (int) (Math.random() * 7);

            if (cur.getGame().isColumnNotFull(randomMove)) {
                if (cur.getChild(randomMove) == null) {
                    NodeMC next = new NodeMC(cur.getGame().play(randomMove), cur, randomMove);
                    cur.addChild(next, randomMove);
                    cur = next;
                }
                else cur = cur.getChild(randomMove);

                if (!q.contains(cur)) q.add(cur);
            }
        }

        char winner = cur.getGame().getWinner();
        if (winner == 'X') backtrack(cur, winner);
        else if (winner == 'O') backtrack(cur, winner);
    }

    private static void backtrack(NodeMC board, char winner) {
        NodeMC cur = board;

        while (cur.getParent() != null) {
            if (winner == 'X') cur.updateTimesWon();
            else cur.updateTimesLost();
            cur = cur.getParent();
        }
    }
}