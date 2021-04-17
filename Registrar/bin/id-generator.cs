using System;

public class IDGenerator
{
    static void Main (string[] args)
    {
        int level;

        try {
            level = int.Parse(args[0]);
        }
        catch (Exception Ex) {
            level = 0;
        }

        string[] chars = new string[62] {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"};

        Random rand = new Random();
        string id = "";
        int index;

        for (int xx = 0; xx < level; xx++) {
            for (int x = 0; x < 5; x++) {
                index = rand.Next(0, 61);
                id += chars[index];
            }
        }

        System.Console.WriteLine(id);
    }
}
