
import java.util.stream.IntStream;

public class Main {
    public static void main(String[] args) {
        var S = new char[256];
        // IntStream.range(0, 256).forEach(i->S[i] = (char) i);
        // System.out.println(S);

        var K = "I AM THE KEY".toCharArray();

        int j = 0;
        for (int i=0;i<S.length;i++) {
            j = (j + S[i] + K[i % K.length]) % 256;
            var tmp = S[i];
            S[i] = S[j];
            S[j] = tmp;
        }

        S=generateKeyStream("I AM THE KEY");

        var text = "Something very important!";

        var cyphertext = encrypt(text, S);
        var plaintext = decrypt(cyphertext, S);

        System.out.println(cyphertext);
        System.out.println(plaintext);
    }

    private static char[] generateKeyStream(String key) {
        var S = new char[256];
        IntStream.range(0, 256).forEach(i->S[i] = (char) i);
        var K = key.toCharArray();
        int j = 0;
        for (int i=0;i<S.length;i++) {
            j = (j + S[i] + K[i % K.length]) % 256;
            var tmp = S[i];
            S[i] = S[j];
            S[j] = tmp;
        }
        return S;
    }

    private static char[] encrypt(String text, char[] keyStream) {
        var cyphertext = new char[text.length()];
        var plaintext = text.toCharArray();
        for(int i=0; i<cyphertext.length; i++) {
            var v = plaintext[i];
            var k = keyStream[i % keyStream.length];
            cyphertext[i] = (char) (v ^ k);
        }

        return cyphertext;
    }

    private static char[] decrypt(char[] cyphertext, char[] keyStream) {
        var plaintext = new char[cyphertext.length];
        for(int i=0; i<cyphertext.length; i++) {
            var v = cyphertext[i];
            var k = keyStream[i % keyStream.length];
            plaintext[i] = (char) (v ^ k);
        }

        return plaintext;
    }
}