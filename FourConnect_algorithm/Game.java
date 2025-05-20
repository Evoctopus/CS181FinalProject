public class Game {
    public char[][] game = new char[6][7];
    public char player;
    public char winner;

    public Game() {
        for (int i = 0; i < 6; i++)
            for (int j = 0; j < 7; j++)
                game[i][j] = ' ';

        this.player = 'O';
    }

    public void myToString() {
        int k = 6;
        for (int i = 0; i < 6; i++) {
            System.out.println("--+---+---+---+---+---+---+---+");
            System.out.print((k - i) + " ");
            for (int j = 0; j < 7; j++)
                System.out.print("| " + game[i][j] + " ");
            System.out.print("|");
            System.out.println();
        }
        System.out.println("--+---+---+---+---+---+---+---+");
    }

    public char playerSwitcher() {
        if (this.player == 'O') return 'X';
        return 'O';
    }

    private boolean notOutBounds(int x, int y) {
        return y >= 0 && y <= 6 && x <= 5 && x >= 0;
    }

    public boolean isColumnNotFull(int column) {
        return game[0][column] == ' ';
    }

    public Game play(int a) {
        Game p = new Game();

        for (int i = 0; i < 6; i++) {
            if (notOutBounds(i, a))
                System.arraycopy(this.game[i], 0, p.game[i], 0, 7);
            else return this;
        }

        for (int i = 0; i < 6; i++) {
            if (p.game[i][a] != ' ') {
                if (i == 0) return p;
                p.game[i - 1][a] = player;
                break;
            }
            if (i == 5) {
                p.game[i][a] = player;
                break;
            }
        }
        p.player = playerSwitcher();
        return p;
    }

    public boolean isGameOver() {
        if (this.value() >= 512) {
            this.winner = 'X';
            return true;
        }
        else if (this.value() <= -512) {
            this.winner = 'O';
            return true;
        }

        boolean isDraw = true;
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 7; j++) {
                if (game[i][j] == ' ') {
                    isDraw = false;
                    break;
                }
            }
            if (!isDraw) break;
        }

        if (isDraw) {
            this.winner = 'D';
            return true;
        }
        return false;
    }

    public char getWinner() {
        return this.winner;
    }


    public int value() {
        int total = 0;

        for (int i = 0; i < 6; i++)
            for (int j = 0; j < 7; j++)
                total += vertical(i, j) + horizontal(i, j) + leftDir(i, j) + rightDir(i, j);

        return total;
    }

    private int checkLine(int row, int col, int rowDelta, int colDelta) {
        int points = 0;
        char cur = game[row][col];

        for (int i = 0; i < 4; i++) {
            int newRow = row + rowDelta * i;
            int newCol = col + colDelta * i;

            if (!notOutBounds(newRow, newCol)) return 0;

            if (cur == ' ' && game[newRow][newCol] != ' ') cur = game[newRow][newCol];

            if (game[newRow][newCol] == cur && cur != ' ') points++;

            else if (game[newRow][newCol] != cur && cur != ' ' && game[newRow][newCol] != ' ')
                points = -3;
        }

        return parity(points, cur);
    }

    private int vertical(int a, int b) {
        if (a > 2) return checkLine(a, b, -1, 0);

        return 0;
    }

    private int horizontal(int a, int b) {
        if (b < 4) return checkLine(a, b, 0, 1);

        return 0;
    }

    private int rightDir(int a, int b) {
        if (a > 3 && b < 4) return checkLine(a, b, -1, 1);

        return 0;
    }

    private int leftDir(int a, int b) {
        if (a > 3 && b > 2) return checkLine(a, b, -1, -1);

        return 0;
    }

    private int parity(int points, char cur) {
        if (points <= 0) return 0;

        else if (cur == 'O') {
            if (points == 2) return -10;
            else if (points == 3) return -50;
            else if (points == 1) return -1;
            return -10000;
        }

        if (points == 2) return 10;
        else if (points == 3) return 50;
        else if (points == 1) return 1;
        return 1000;
    }

    public void printBoard() {
        System.out.println();
        this.myToString();
        System.out.println("  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n");
        System.out.println("Points: " + this.value());
        System.out.println();
    }

    public void verifyVictory() {
        char winner = this.getWinner();
        if (winner == 'X')
            System.out.println("X wins with: " + this.value());
        else if (winner == 'O')
            System.out.println("O wins with: " + this.value());
        else
            System.out.println("Draw with: " + this.value());
    }
}
