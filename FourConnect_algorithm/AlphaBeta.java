class AlphaBeta {
    private static final int MAX_DEPTH = 7;

    public static int AlphaBetaSearch(Game state) {
        return maxSearch(state, 0, Integer.MIN_VALUE, Integer.MAX_VALUE).getMove();
    }

    private static Node maxSearch(Game state, int depth, int alpha, int beta) {
        if (state.isGameOver() || depth == MAX_DEPTH) {
            Node node = new Node(-1);
            node.setValue(state.value());
            return node;
        }

        int bestMove = -1;
        int maxValue = Integer.MIN_VALUE;

        for (int i = 0; i < 7; i++) {
            if (state.isColumnNotFull(i)) {
                Game child = state.play(i);
                if (child != state) {
                    Node minNode = minSearch(child, depth + 1, alpha, beta);
                    if (minNode.getValue() > maxValue) {
                        maxValue = minNode.getValue();
                        bestMove = i;
                    }
                    if (maxValue >= beta) {
                        break;
                    }
                    alpha = Math.max(alpha, maxValue);
                }
            }
        }

        Node result = new Node(bestMove);
        result.setValue(maxValue);
        return result;
    }

    private static Node minSearch(Game state, int depth, int alpha, int beta) {
        if (state.isGameOver() || depth == MAX_DEPTH) {
            Node node = new Node(-1);
            node.setValue(state.value());
            return node;
        }

        int bestMove = -1;
        int minValue = Integer.MAX_VALUE;

        for (int i = 0; i < 7; i++) {
            if (state.isColumnNotFull(i)) {
                Game child = state.play(i);
                if (child != state) {
                    Node maxNode = maxSearch(child, depth + 1, alpha, beta);
                    if (maxNode.getValue() < minValue) {
                        minValue = maxNode.getValue();
                        bestMove = i;
                    }
                    if (minValue <= alpha) {
                        break;
                    }
                    beta = Math.min(beta, minValue);
                }
            }
        }

        Node result = new Node(bestMove);
        result.setValue(minValue);
        return result;
    }
}