class MinMax {
    private static final int MAX_DEPTH = 7;

    public static int MinMaxSearch(Game board) {
        return maxSearch(board, 0).getMove();
    }

    private static Node maxSearch(Game board, int depth) {
        if (board.isGameOver() || depth == MAX_DEPTH) {
            Node node = new Node(-1);
            node.setValue(board.value());
            return node;
        }

        int bestMove = -1;
        int maxValue = Integer.MIN_VALUE;

        boolean anyMovePossible = false;

        for (int i = 0; i < 7; i++) {
            if (board.isColumnNotFull(i)) {
                anyMovePossible = true;
                Game nGen = board.play(i);
                if (nGen != board) {
                    Node minNode = minSearch(nGen, depth + 1);
                    if (minNode.getValue() > maxValue) {
                        maxValue = minNode.getValue();
                        bestMove = i;
                    }
                }
            }
        }
        if (!anyMovePossible) {
            Node node = new Node(-1);
            node.setValue(0);
            return node;
        }

        Node result = new Node(bestMove);
        result.setValue(maxValue);
        return result;
    }

    private static Node minSearch(Game board, int depth) {
        if (board.isGameOver() || depth == MAX_DEPTH) {
            Node node = new Node(-1);
            node.setValue(board.value());
            return node;
        }

        int bestMove = -1;
        int minValue = Integer.MAX_VALUE;

        for (int i = 0; i < 7; i++) {
            if (board.isColumnNotFull(i)) {
                Game nGen = board.play(i);
                if (nGen != board) {
                    Node maxNode = maxSearch(nGen, depth + 1);
                    if (maxNode.getValue() < minValue) {
                        minValue = maxNode.getValue();
                        bestMove = i;
                    }
                }
            }
        }

        Node result = new Node(bestMove);
        result.setValue(minValue);
        return result;
    }
}
