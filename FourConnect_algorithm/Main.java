import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        Game board = new Game();

        System.out.println("1 player(1) or 2 players(2)");
        int numPlayers = in.nextInt();

        switch (numPlayers) {
            case 2 -> {
                board.printBoard();

                while (true) {
                    board = board.play(in.nextInt() - 1);

                    board.printBoard();

                    if (board.isGameOver()) {
                        board.verifyVictory();
                        break;
                    }
                }
            }
            case 1 -> {
                System.out.println("First player(1) or second player(2)");
                if (in.nextInt() == 2) board.player = 'X';

                System.out.println("Play VS: ");
                System.out.println("MinMax(1) | AlphaBeta(2) | MonteCarlo(3)");
                int ai = in.nextInt();

                board.printBoard();

                while (true) {
                    if (board.player == 'X') {
                        switch (ai) {
                            case 1 -> board = board.play(MinMax.MinMaxSearch(board));
                            case 2 -> board = board.play(AlphaBeta.AlphaBetaSearch(board));
                            case 3 -> board = board.play(MonteCarlo.monteCarloSearch(board));
                            default -> {}
                        }
                    }
                    else board = board.play(in.nextInt() - 1);

                    board.printBoard();

                    if (board.isGameOver()) {
                        board.verifyVictory();
                        break;
                    }
                }
            }
        }
        in.close();
    }
}